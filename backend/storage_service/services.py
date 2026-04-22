import logging
import base64
import boto3
from botocore.client import Config
from typing import Union

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BytesLike = Union[bytes, bytearray]

def _decode_base64_maybe_dataurl(s: str) -> bytes:
    """
    'data:image/png;base64,...' 또는 순수 Base64 모두 지원.
    공백/개행 제거 및 padding 보정 포함.
    """
    raw = (s or "").strip()
    if raw.startswith("data:") and "," in raw:
        raw = raw.split(",", 1)[1]
    raw = "".join(raw.split())
    missing = (-len(raw)) % 4
    if missing:
        raw += "=" * missing
    return base64.b64decode(raw, validate=False)


class StorageClient:
    """
    Supabase Storage 클라이언트 (S3 호환)
    필요 ENV:
      STORAGE_ACCESS_KEY, STORAGE_SECRET_KEY, STORAGE_BUCKET,
      STORAGE_ENDPOINT, STORAGE_PUBLIC_BASE_URL, STORAGE_REGION
    """
    def __init__(self):
        from django.conf import settings

        self.access_key = getattr(settings, 'STORAGE_ACCESS_KEY', '')
        self.secret_key = getattr(settings, 'STORAGE_SECRET_KEY', '')
        self.bucket = getattr(settings, 'STORAGE_BUCKET', '')
        self.endpoint = getattr(settings, 'STORAGE_ENDPOINT', '')
        self.public_base_url = getattr(settings, 'STORAGE_PUBLIC_BASE_URL', '')
        self.region = getattr(settings, 'STORAGE_REGION', 'ap-northeast-2')

        if not all([self.access_key, self.secret_key, self.bucket, self.endpoint, self.public_base_url]):
            raise ValueError(
                "Storage 환경변수(STORAGE_ACCESS_KEY, STORAGE_SECRET_KEY, "
                "STORAGE_BUCKET, STORAGE_ENDPOINT, STORAGE_PUBLIC_BASE_URL)가 모두 필요합니다."
            )

        self.client = boto3.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint,
            config=Config(signature_version="s3v4"),
            region_name=self.region,
        )

    def _ensure_bytes(self, data: Union[str, BytesLike, memoryview]) -> BytesLike:
        if isinstance(data, (bytes, bytearray)):
            return data
        if isinstance(data, memoryview):
            return data.tobytes()
        if isinstance(data, str):
            return _decode_base64_maybe_dataurl(data)
        raise TypeError(f"upload_file(data): unsupported type {type(data)}")

    def upload_file(self, key: str, data: Union[str, BytesLike, memoryview], content_type: str = "application/octet-stream"):
        blob = self._ensure_bytes(data)
        if not content_type:
            content_type = "application/octet-stream"

        resp = self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=blob,
            ContentType=content_type,
        )
        logger.info(f"[Storage] 업로드 성공 key={key} len={len(blob)} ct={content_type}")

        public_url = f"{self.public_base_url}/{key}"

        return {
            'url': public_url,
            'key': key,
            'size': len(blob),
            'content_type': content_type,
            'response': resp
        }

    def download_file(self, key: str) -> bytes:
        resp = self.client.get_object(Bucket=self.bucket, Key=key)
        data = resp["Body"].read()
        logger.info(f"[Storage] 다운로드 성공 key={key} len={len(data)}")
        return data

    def delete_file(self, key: str):
        resp = self.client.delete_object(Bucket=self.bucket, Key=key)
        logger.info(f"[Storage] 삭제 성공 key={key}")
        return resp
