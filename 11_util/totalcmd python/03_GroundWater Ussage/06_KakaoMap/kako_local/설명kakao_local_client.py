# We need some tools to talk to the internet and use files
import httpx  # This is like a phone to call the internet
import os  # This helps us find secrets in our computer

# These are special boxes that hold information about places and locations
from mcp_kakao_local.models import (
    AddressResponse,  # A box for address answers
    CategoryGroupCode,  # A box for types of places (like restaurants or parks)
    Coordinate,  # A box for map points (like X and Y on a treasure map)
    LocationSortOption,  # A box to decide how to sort places (like closest first)
    LocationSearchResponse,  # A box for search answers
    PlaceDetailResponse,  # A box for details about one place
)
from typing import Any  # This helps us say "anything" can go in some boxes


# This is our main helper class to talk to Kakao's map service
class KakaoLocalClient:
    # This is the address where we send our questions to Kakao
    BASE_URL = "https://dapi.kakao.com/v2/local"

    # When we create our helper, we need a secret key
    def __init__(self):
        # Look for the secret key in our computer
        # rest_api_key = os.getenv("REST_API_KEY")
        rest_api_key = os.getenv("REST_API_KEY")

        # If we can't find the key, we say "Oh no! We need a key!"
        if not rest_api_key:
            rest_api_key="bb159a41d2eb8d5acb71e0ef1dde4d16"
            # raise AuthError("missing REST API key")

        # We prepare a note with our key to send with our questions
        self.headers = {
            "Authorization": f"KakaoAK {rest_api_key}",  # Our secret key note
            "accept": "application/json",  # We want answers in a special format
            "content-type": "application/json",  # We send questions in that format too
        }

    # This function finds map points (X, Y) for an address, like finding where a house is
    async def find_coordinates(self, address: str, page: int = 1, size: int = 10) -> AddressResponse:
        """This helps us find map points for an address"""
        # We make the address to ask Kakao about
        path = f"{self.BASE_URL}/search/address"
        # We write down what we want to ask
        params = {
            "query": address,  # The address we want to find
            "page": page,  # Which page of answers we wantpip install pip-review
            "size": size,  # How many answers we want on one page
        }
        # We send the question and get an answer
        response_json = await self._get(path, params)
        # We put the answer in a special box and return it
        return AddressResponse(**response_json)

    # This function searches for places using a word, like "pizza" or "park"
    async def search_by_keyword(
            self,
            keyword: str,  # The word we search for
            category_group_code: CategoryGroupCode | None,  # What kind of place (optional)
            center: Coordinate | None,  # Center of the map (optional)
            radius: int | None,  # How far to look around (optional)
            page: int = 1,  # Which page of answers
            size: int = 10,  # How many answers per page
            sort_option: LocationSortOption = LocationSortOption.ACCURACY,  # How to sort answers
    ) -> LocationSearchResponse:
        """This helps us find places by a word, like finding pizza shops"""
        # We make the address to ask Kakao about
        path = f"{self.BASE_URL}/search/keyword"
        # We write down what we want to ask
        params = {
            "query": keyword,  # The word we’re searching
            "category_group_code": category_group_code.name if category_group_code else None,  # Kind of place
            "x": center.longitude if center else None,  # Map X point
            "y": center.latitude if center else None,  # Map Y point
            "radius": radius if radius else None,  # How far to look
            "page": page,  # Which page of answers
            "size": size,  # How many answers per page
            "sort": sort_option.value,  # How to sort answers
        }
        # We only send the parts that have something in them
        response_json = await self._get(path, {k: v for k, v in params.items() if v is not None})
        # We put the answer in a special box and return it
        return LocationSearchResponse(**response_json)

    # This function searches for places by type, like all restaurants near a point
    async def search_by_category(
            self,
            category_group_code: CategoryGroupCode,  # What kind of place
            center: Coordinate,  # Center of the map
            radius: int,  # How far to look
            page: int = 1,  # Which page of answers
            size: int = 10,  # How many answers per page
            sort_option: LocationSortOption = LocationSortOption.ACCURACY,  # How to sort answers
    ) -> LocationSearchResponse:
        """This helps us find places by type, like all parks nearby"""
        # We make the address to ask Kakao about
        path = f"{self.BASE_URL}/search/category"
        # We write down what we want to ask
        params = {
            "category_group_code": category_group_code.name,  # Kind of place
            "x": center.longitude,  # Map X point
            "y": center.latitude,  # Map Y point
            "radius": radius,  # How far to look
            "page": page,  # Which page of answers
            "size": size,  # How many answers per page
            "sort": sort_option.value,  # How to sort answers
        }
        # We send the question and get an answer
        response_json = await self._get(path, params)
        # We put the answer in a special box and return it
        return LocationSearchResponse(**response_json)

    # This function gets details about one specific place
    async def get_place_details(self, place_id: int) -> PlaceDetailResponse:
        # We prepare a special note for this question
        headers = {
            "Accept": "application/json, text/plain, */*",  # We accept different answer formats
            "Accept-Encoding": "gzip, deflate, br",  # How to pack the answer
            "Accept-Language": "en-US,en;q=0.9",  # We prefer English answers
            "Connection": "keep-alive",  # Keep the phone line open
            "Dnt": "1",  # Don’t track us
            "Origin": "https://place.map.kakao.com",  # Where we’re calling from
            "Referer": "https://place.map.kakao.com/",  # Our website address
            "Pf": "web",  # We’re calling from a website
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            # Our browser name
        }
        # We use a special phone to call Kakao
        async with httpx.AsyncClient(headers=headers, http2=True) as client:
            # We ask about a specific place
            response = await client.get(f"https://place-api.map.kakao.com/places/panel3/{place_id}")
            try:
                # We check if the answer is good and put it in a box
                response_json = response.raise_for_status().json()
                return PlaceDetailResponse(**response_json)
            except httpx.HTTPError as exc:
                # If something goes wrong, we check what happened
                self._handle_response_status(response.status_code, exc)

    # This is a helper function to send questions to Kakao
    async def _get(self, path: str, params: dict[str, Any]) -> dict:
        # We use our phone to call Kakao with our note
        async with httpx.AsyncClient(headers=self.headers, http2=True) as client:
            # We send the question
            response = await client.get(path, params=params)
            try:
                # We check if the answer is good and return it
                return response.raise_for_status().json()
            except httpx.HTTPError as exc:
                # If something goes wrong, we check what happened
                self._handle_response_status(response.status_code, exc)

    # This function checks if something went wrong with Kakao’s answer
    def _handle_response_status(self, http_status_code: int, http_error: httpx.HTTPError):
        error_str = str(http_error)  # What went wrong
        if http_status_code == 400:  # Bad question
            raise BadRequestError(error_str)
        if http_status_code == 401:  # Wrong secret key
            raise AuthError(error_str)
        if http_status_code == 420:  # Asked too many questions
            raise RateLimitError(error_str)
        if http_status_code != 200:  # Other problems
            raise KakaoClientError(
                f"Unexpected error [status_code={http_status_code}, error={error_str}]"
            )


# These are special error messages we use when something goes wrong
class KakaoClientError(Exception):
    def __init__(self, message: str):
        self.message = message  # Save the error message
        super().__init__(self.message)  # Tell everyone what went wrong


class BadRequestError(KakaoClientError):
    def __init__(self, message):
        super().__init__(f"Bad request: {message}")  # Say the question was bad


class AuthError(KakaoClientError):
    def __init__(self, message):
        super().__init__(f"Auth error: {message}")  # Say the secret key was wrong


class RateLimitError(KakaoClientError):
    def __init__(self, message):
        super().__init__(f"Rate limited: {message}")  # Say we asked too much
