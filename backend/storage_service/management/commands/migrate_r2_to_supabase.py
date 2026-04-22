"""
R2 → Supabase Storage 마이그레이션 커맨드

사용법:
  # 1) 파일 마이그레이션 (R2 → Supabase)
  python manage.py migrate_r2_to_supabase files \
    --r2-access-key=... --r2-secret-key=... --r2-bucket=... \
    --r2-endpoint=... --batch-size=100

  # 2) DB URL 일괄 변경
  python manage.py migrate_r2_to_supabase db \
    --old-base-url="https://pub-xxx.r2.dev" \
    --new-base-url="https://xxx.supabase.co/storage/v1/object/public/mpz-assets" \
    --dry-run

  # 3) 마이그레이션 상태 확인
  python manage.py migrate_r2_to_supabase status \
    --r2-access-key=... --r2-secret-key=... --r2-bucket=... --r2-endpoint=...
"""
import time
import mimetypes
from django.core.management.base import BaseCommand
from django.db import connection


# 바이트 시그니처 → Content-Type 매핑
MAGIC_BYTES = [
    (b'\x89PNG\r\n\x1a\n', 'image/png'),
    (b'\xff\xd8\xff', 'image/jpeg'),
    (b'GIF87a', 'image/gif'),
    (b'GIF89a', 'image/gif'),
    (b'RIFF', 'image/webp'),  # RIFF....WEBP
    (b'BM', 'image/bmp'),
    (b'<svg', 'image/svg+xml'),
]


def detect_content_type(key: str, data: bytes) -> str:
    """파일 키와 바이트 시그니처로 Content-Type 결정"""
    # 1) 확장자로 추론
    ct, _ = mimetypes.guess_type(key)
    if ct and ct != 'application/octet-stream':
        return ct

    # 2) 바이트 시그니처
    for sig, mime in MAGIC_BYTES:
        if data[:len(sig)] == sig:
            if mime == 'image/webp' and len(data) >= 12:
                if data[8:12] != b'WEBP':
                    continue
            return mime

    return 'application/octet-stream'


# DB URL 변경 대상 테이블/필드
URL_FIELDS = [
    ('animal_images', 'image_url'),
    ('banners', 'image_url'),
    ('centers', 'image_url'),
    ('post_images', 'image_url'),
    ('user', 'image'),
    ('adoption_contracts', 'user_signature_url'),
    ('adoption_contracts', 'center_signature_url'),
]


class Command(BaseCommand):
    help = 'R2 → Supabase Storage 마이그레이션'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='subcommand')

        # files 서브커맨드
        files_parser = subparsers.add_parser('files', help='R2 파일을 Supabase로 복사')
        files_parser.add_argument('--r2-access-key', required=True)
        files_parser.add_argument('--r2-secret-key', required=True)
        files_parser.add_argument('--r2-bucket', required=True)
        files_parser.add_argument('--r2-endpoint', required=True)
        files_parser.add_argument('--batch-size', type=int, default=100)
        files_parser.add_argument('--prefix', default='', help='특정 폴더만 마이그레이션 (예: public-data/)')
        files_parser.add_argument('--dry-run', action='store_true', help='실제 업로드 없이 시뮬레이션')
        files_parser.add_argument('--resume-from', default='', help='이 키 이후부터 재개')

        # db 서브커맨드
        db_parser = subparsers.add_parser('db', help='DB에서 R2 URL을 Supabase URL로 변경')
        db_parser.add_argument('--old-base-url', required=True, help='R2 public base URL')
        db_parser.add_argument('--new-base-url', required=True, help='Supabase public base URL')
        db_parser.add_argument('--dry-run', action='store_true')

        # status 서브커맨드
        status_parser = subparsers.add_parser('status', help='R2와 Supabase의 파일 수 비교')
        status_parser.add_argument('--r2-access-key', required=True)
        status_parser.add_argument('--r2-secret-key', required=True)
        status_parser.add_argument('--r2-bucket', required=True)
        status_parser.add_argument('--r2-endpoint', required=True)

    def handle(self, *args, **options):
        subcommand = options.get('subcommand')
        if subcommand == 'files':
            self._migrate_files(options)
        elif subcommand == 'db':
            self._migrate_db_urls(options)
        elif subcommand == 'status':
            self._check_status(options)
        else:
            self.stderr.write('서브커맨드를 지정하세요: files, db, status')

    def _get_r2_client(self, options):
        import boto3
        from botocore.client import Config
        return boto3.client(
            's3',
            aws_access_key_id=options['r2_access_key'],
            aws_secret_access_key=options['r2_secret_key'],
            endpoint_url=options['r2_endpoint'],
            config=Config(signature_version='s3v4'),
            region_name='auto',
        )

    def _get_supabase_client(self):
        from storage_service.services import StorageClient
        return StorageClient()

    def _list_all_keys(self, client, bucket, prefix=''):
        """R2 버킷의 모든 키를 페이지네이션으로 조회"""
        keys = []
        continuation_token = None
        while True:
            kwargs = {'Bucket': bucket, 'MaxKeys': 1000}
            if prefix:
                kwargs['Prefix'] = prefix
            if continuation_token:
                kwargs['ContinuationToken'] = continuation_token

            resp = client.list_objects_v2(**kwargs)
            for obj in resp.get('Contents', []):
                keys.append({'key': obj['Key'], 'size': obj.get('Size', 0)})

            if resp.get('IsTruncated'):
                continuation_token = resp['NextContinuationToken']
            else:
                break
        return keys

    def _migrate_files(self, options):
        r2 = self._get_r2_client(options)
        supabase = self._get_supabase_client()
        bucket = options['r2_bucket']
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        resume_from = options['resume_from']
        prefix = options.get('prefix', '')

        self.stdout.write(f'R2 버킷 스캔 중... (prefix={prefix or "전체"})')
        all_keys = self._list_all_keys(r2, bucket, prefix)
        total = len(all_keys)
        self.stdout.write(f'총 {total}개 파일 발견')

        if resume_from:
            skip_idx = next((i for i, k in enumerate(all_keys) if k['key'] == resume_from), -1)
            if skip_idx >= 0:
                all_keys = all_keys[skip_idx + 1:]
                self.stdout.write(f'  → {resume_from} 이후부터 재개 ({len(all_keys)}개 남음)')

        success = 0
        failed = 0
        skipped = 0
        total_bytes = 0
        start_time = time.time()

        for i, obj in enumerate(all_keys):
            key = obj['key']

            if dry_run:
                self.stdout.write(f'  [DRY-RUN] {i+1}/{len(all_keys)} {key} ({obj["size"]:,} bytes)')
                success += 1
                continue

            try:
                # R2에서 다운로드
                resp = r2.get_object(Bucket=bucket, Key=key)
                data = resp['Body'].read()

                # Content-Type 결정
                ct = detect_content_type(key, data)

                # Supabase에 업로드
                supabase.upload_file(key=key, data=data, content_type=ct)

                success += 1
                total_bytes += len(data)

                if (i + 1) % batch_size == 0:
                    elapsed = time.time() - start_time
                    rate = success / elapsed if elapsed > 0 else 0
                    self.stdout.write(
                        f'  [{i+1}/{len(all_keys)}] 성공={success} 실패={failed} '
                        f'({total_bytes / 1024 / 1024:.1f} MB, {rate:.1f} files/s)'
                    )

            except Exception as e:
                failed += 1
                self.stderr.write(f'  [ERROR] {key}: {e}')

        elapsed = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(
            f'\n완료! 성공={success} 실패={failed} 스킵={skipped} '
            f'총 {total_bytes / 1024 / 1024:.1f} MB / {elapsed:.0f}초'
        ))

        if failed > 0:
            self.stderr.write(self.style.WARNING(
                f'⚠️ {failed}개 파일 실패. --resume-from 옵션으로 재시도하세요.'
            ))

    def _migrate_db_urls(self, options):
        old_base = options['old_base_url'].rstrip('/')
        new_base = options['new_base_url'].rstrip('/')
        dry_run = options['dry_run']

        self.stdout.write(f'DB URL 변환: {old_base} → {new_base}')

        with connection.cursor() as cursor:
            for table, field in URL_FIELDS:
                # 영향 받는 행 수 확인
                cursor.execute(
                    f'SELECT COUNT(*) FROM "{table}" WHERE "{field}" LIKE %s',
                    [f'{old_base}%']
                )
                count = cursor.fetchone()[0]

                if count == 0:
                    self.stdout.write(f'  {table}.{field}: 변경 대상 없음')
                    continue

                if dry_run:
                    self.stdout.write(f'  [DRY-RUN] {table}.{field}: {count}개 행 변경 예정')
                    # 샘플 출력
                    cursor.execute(
                        f'SELECT "{field}" FROM "{table}" WHERE "{field}" LIKE %s LIMIT 3',
                        [f'{old_base}%']
                    )
                    for row in cursor.fetchall():
                        old_url = row[0]
                        new_url = old_url.replace(old_base, new_base, 1)
                        self.stdout.write(f'    {old_url[:80]}...')
                        self.stdout.write(f'    → {new_url[:80]}...')
                else:
                    cursor.execute(
                        f'UPDATE "{table}" SET "{field}" = REPLACE("{field}", %s, %s) '
                        f'WHERE "{field}" LIKE %s',
                        [old_base, new_base, f'{old_base}%']
                    )
                    self.stdout.write(self.style.SUCCESS(f'  {table}.{field}: {count}개 행 변경 완료'))

        if dry_run:
            self.stdout.write('\n--dry-run 모드. 실제 변경 없음.')
        else:
            self.stdout.write(self.style.SUCCESS('\nDB URL 변환 완료!'))

    def _check_status(self, options):
        r2 = self._get_r2_client(options)
        bucket = options['r2_bucket']

        self.stdout.write('R2 버킷 스캔 중...')
        r2_keys = self._list_all_keys(r2, bucket)
        r2_total_size = sum(k['size'] for k in r2_keys)

        self.stdout.write(f'\n=== R2 현황 ===')
        self.stdout.write(f'  파일 수: {len(r2_keys):,}')
        self.stdout.write(f'  총 용량: {r2_total_size / 1024 / 1024:.1f} MB')

        # 폴더별 통계
        folders = {}
        for k in r2_keys:
            folder = k['key'].split('/')[0] if '/' in k['key'] else '(root)'
            if folder not in folders:
                folders[folder] = {'count': 0, 'size': 0}
            folders[folder]['count'] += 1
            folders[folder]['size'] += k['size']

        self.stdout.write(f'\n  폴더별:')
        for folder, stats in sorted(folders.items(), key=lambda x: -x[1]['count']):
            self.stdout.write(
                f'    {folder}: {stats["count"]:,}개 ({stats["size"] / 1024 / 1024:.1f} MB)'
            )

        # Supabase 현황
        try:
            supabase = self._get_supabase_client()
            sb_keys = self._list_all_keys(supabase.client, supabase.bucket)
            sb_total_size = sum(k['size'] for k in sb_keys)
            self.stdout.write(f'\n=== Supabase 현황 ===')
            self.stdout.write(f'  파일 수: {len(sb_keys):,}')
            self.stdout.write(f'  총 용량: {sb_total_size / 1024 / 1024:.1f} MB')

            migrated = len(set(k['key'] for k in sb_keys) & set(k['key'] for k in r2_keys))
            self.stdout.write(f'\n=== 진행률 ===')
            self.stdout.write(f'  마이그레이션 완료: {migrated:,} / {len(r2_keys):,} ({migrated/len(r2_keys)*100:.1f}%)')
        except Exception as e:
            self.stdout.write(f'\nSupabase 조회 실패: {e}')
