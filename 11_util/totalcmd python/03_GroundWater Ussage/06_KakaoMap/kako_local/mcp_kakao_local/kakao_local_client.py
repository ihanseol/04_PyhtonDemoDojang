import httpx
import os

from mcp_kakao_local.models import (
    AddressResponse,
    CategoryGroupCode,
    Coordinate,
    LocationSortOption,
    LocationSearchResponse,
    PlaceDetailResponse,
)
from typing import Any


class KakaoLocalClient:
    BASE_URL = "https://dapi.kakao.com/v2/local"

    def __init__(self):
        rest_api_key = os.getenv("REST_API_KEY")
        if not rest_api_key:
            raise AuthError("missing REST API key")

        self.headers = {
            "Authorization": f"KakaoAK {rest_api_key}",
            "accept": "application/json",
            "content-type": "application/json",
        }

    async def find_coordinates(self, address: str, page: int = 1, size: int = 10) -> AddressResponse:
        """https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord"""
        path = f"{self.BASE_URL}/search/address"
        params = {
            "query": address,
            "page": page,
            "size": size,
        }
        response_json = await self._get(path, params)
        return AddressResponse(**response_json)

    async def search_by_keyword(
            self,
            keyword: str,
            category_group_code: CategoryGroupCode | None,
            center: Coordinate | None,
            radius: int | None,
            page: int = 1,
            size: int = 10,
            sort_option: LocationSortOption = LocationSortOption.ACCURACY,
    ) -> LocationSearchResponse:
        """https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-keyword"""
        path = f"{self.BASE_URL}/search/keyword"
        params = {
            "query": keyword,
            "category_group_code": category_group_code.name if category_group_code else None,
            "x": center.longitude if center else None,
            "y": center.latitude if center else None,
            "radius": radius if radius else None,
            "page": page,
            "size": size,
            "sort": sort_option.value,
        }
        response_json = await self._get(path, {k: v for k, v in params.items() if v is not None})
        return LocationSearchResponse(**response_json)

    async def search_by_category(
            self,
            category_group_code: CategoryGroupCode,
            center: Coordinate,
            radius: int,
            page: int = 1,
            size: int = 10,
            sort_option: LocationSortOption = LocationSortOption.ACCURACY,
    ) -> LocationSearchResponse:
        """https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-category"""
        path = f"{self.BASE_URL}/search/category"
        params = {
            "category_group_code": category_group_code.name,
            "x": center.longitude,
            "y": center.latitude,
            "radius": radius,
            "page": page,
            "size": size,
            "sort": sort_option.value,
        }
        response_json = await self._get(path, params)
        return LocationSearchResponse(**response_json)

    async def get_place_details(self, place_id: int) -> PlaceDetailResponse:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Dnt": "1",
            "Origin": "https://place.map.kakao.com",
            "Referer": "https://place.map.kakao.com/",
            "Pf": "web",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        }
        async with httpx.AsyncClient(headers=headers, http2=True) as client:
            response = await client.get(f"https://place-api.map.kakao.com/places/panel3/{place_id}")
            try:
                response_json = response.raise_for_status().json()
                return PlaceDetailResponse(**response_json)
            except httpx.HTTPError as exc:
                self._handle_response_status(response.status_code, exc)

    async def _get(self, path: str, params: dict[str, Any]) -> dict:
        async with httpx.AsyncClient(headers=self.headers, http2=True) as client:
            response = await client.get(path, params=params)

            try:
                return response.raise_for_status().json()
            except httpx.HTTPError as exc:
                self._handle_response_status(response.status_code, exc)

    def _handle_response_status(self, http_status_code: int, http_error: httpx.HTTPError):
        error_str = str(http_error)
        if http_status_code == 400:
            raise BadRequestError(error_str)
        if http_status_code == 401:
            raise AuthError(error_str)
        if http_status_code == 420:
            raise RateLimitError(error_str)
        if http_status_code != 200:
            raise KakaoClientError(
                f"Unexpected error [status_code={http_status_code}, error={error_str}]"
            )


class KakaoClientError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BadRequestError(KakaoClientError):
    def __init__(self, message):
        super().__init__(f"Bad request: {message}")


class AuthError(KakaoClientError):
    def __init__(self, message):
        super().__init__(f"Auth error: {message}")


class RateLimitError(KakaoClientError):
    def __init__(self, message):
        super().__init__(f"Rate limited: {message}")
