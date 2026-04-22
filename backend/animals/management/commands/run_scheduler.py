"""
공공데이터 동기화 스케줄러

cron 대신 Python으로 스케줄 관리. worker 컨테이너에서 실행.
- 매일 03:00 KST: incremental (어제~오늘)
- 매주 일요일 04:00 KST: status_sync (상태만)
- 매월 1일 05:00 KST: full (전체, 최근 90일)
"""
import time
import subprocess
import sys
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone


def kst_now():
    """현재 KST 시간"""
    from datetime import timedelta
    return datetime.utcnow() + timedelta(hours=9)


class Command(BaseCommand):
    help = '공공데이터 동기화 스케줄러 (worker 컨테이너용)'

    def handle(self, *args, **options):
        self.stdout.write('[scheduler] 스케줄러 시작')
        self.stdout.write('[scheduler] 매일 03:00 KST incremental')
        self.stdout.write('[scheduler] 매주 일 04:00 KST status_sync')
        self.stdout.write('[scheduler] 매월 1일 05:00 KST full')

        last_daily = None
        last_weekly = None
        last_monthly = None

        while True:
            now = kst_now()
            today = now.strftime('%Y-%m-%d')
            weekday = now.weekday()  # 0=월, 6=일
            day = now.day
            hour = now.hour
            minute = now.minute

            # 매일 03:00 KST — incremental
            if hour == 3 and minute < 5 and last_daily != today:
                last_daily = today
                self._run_sync('incremental', '--days', '2')

            # 매주 일요일 04:00 KST — status_sync
            if weekday == 6 and hour == 4 and minute < 5 and last_weekly != today:
                last_weekly = today
                self._run_sync('status_sync')

            # 매월 1일 05:00 KST — full
            if day == 1 and hour == 5 and minute < 5 and last_monthly != today:
                last_monthly = today
                self._run_sync('full', '--days', '90')

            time.sleep(60)  # 1분마다 체크

    def _run_sync(self, strategy, *extra_args):
        self.stdout.write(f'[scheduler] {strategy} 동기화 시작')
        cmd = [
            sys.executable, 'manage.py', 'sync_public_data',
            '--strategy', strategy,
            *extra_args,
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
            self.stdout.write(result.stdout)
            if result.stderr:
                self.stderr.write(result.stderr)
            if result.returncode == 0:
                self.stdout.write(f'[scheduler] {strategy} 동기화 완료')
            else:
                self.stderr.write(f'[scheduler] {strategy} 동기화 실패 (exit={result.returncode})')
        except subprocess.TimeoutExpired:
            self.stderr.write(f'[scheduler] {strategy} 동기화 타임아웃 (2시간)')
        except Exception as e:
            self.stderr.write(f'[scheduler] {strategy} 동기화 에러: {e}')
