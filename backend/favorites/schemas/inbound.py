from ninja import Schema, Field
from typing import Optional


class FavoriteListQueryIn(Schema):
    """찜 목록 조회 쿼리 스키마"""
    # @paginate 데코레이터가 page, limit을 자동으로 처리하므로 제거
    pass
