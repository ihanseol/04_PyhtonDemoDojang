from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal


class Coordinate(BaseModel):
    longitude: str
    latitude: str


class LocationSortOption(Enum):
    DISTANCE = "distance"
    ACCURACY = "accuracy"


class CategoryGroupCode(Enum):
    MT1 = "대형마트 (Large Mart, Grocery Store)"
    CS2 = "편의점 (Convenience Store)"
    PS3 = "어린이집, 유치원 (Daycare, Kindergarten)"
    SC4 = "학교 (School)"
    AC5 = "학원 (Academy/Private Institute)"
    PK6 = "주차장 (Parking Lot)"
    OL7 = "주유소, 충전소 (Gas Station, Charging Station)"
    SW8 = "지하철역 (Subway Station)"
    BK9 = "은행 (Bank)"
    CT1 = "문화시설 (Cultural Facility)"
    AG2 = "중개업소 (Agency, e.g. Real Estate)"
    PO3 = "공공기관 (Public Institution)"
    AT4 = "관광명소 (Tourist Attraction)"
    AD5 = "숙박 (Accommodation)"
    FD6 = "음식점 (Restaurant)"
    CE7 = "카페 (Cafe)"
    HP8 = "병원 (Hospital)"
    PM9 = "약국 (Pharmacy)"


class SameName(BaseModel):
    region: list[str] = Field(
        description="List of regions searched from the query. Example: the region list corresponding to 'Jungang-ro' in 'Jungang-ro restaurants'"
    )
    keyword: str = Field(
        description="Keyword excluding region information from the query. Example: 'restaurants' from 'Jungang-ro restaurants'"
    )
    selected_region: str = Field(description="The region information currently used in the search")


class Meta(BaseModel):
    total_count: int = Field(description="Number of documents found for the search results", ge=0)
    pageable_count: int = Field(description="Number of documents allowed in a page", ge=0, le=45)
    is_end: bool = Field(
        description="Whether the current page is the last page. If false, increase the page value in the next request to fetch the next page"
    )
    same_name: SameName | None = Field(
        None, description="Region and keyword analysis information of the query"
    )


class PlaceDocument(BaseModel):
    id: str = Field(description="Place ID")
    place_name: str = Field(description="Place name or business name")
    category_name: str = Field(description="Category name")
    category_group_code: str = Field(description="Category group code (see CategoryGroupCode)")
    category_group_name: str = Field(description="Category group name")
    phone: str = Field(description="Phone number")
    address_name: str = Field(description="Land-lot address (지번 주소)")
    road_address_name: str = Field(description="Street address")
    x: str = Field(description="longitude")
    y: str = Field(description="latitude")
    place_url: str = Field(description="Place detail page URL")
    distance: str | None = Field(
        None,
        description="Distance from the center coordinate in meters (non-null only when x and y parameters are provided in a request)",
    )


class AddressDocument(BaseModel):
    address_name: str = Field(description="street address or land-lot address (지번 주소)")
    address_type: Literal["REGION", "ROAD", "REGION_ADDR", "ROAD_ADDR"] = Field(
        description="type of address"
    )
    x: str = Field(description="longitude")
    y: str = Field(description="latitude")
    address: dict = Field(description="details of land-lot address (지번 주소)")
    road_address: dict = Field(description="details of street address")


class LocationSearchResponse(BaseModel):
    meta: Meta = Field(description="Response metadata")
    documents: list[PlaceDocument] = Field(description="List of places")


class AddressResponse(BaseModel):
    meta: Meta = Field(description="Response metadata")
    documents: list[AddressDocument] = Field(description="List of addresses")


class PlaceSummary(BaseModel):
    confirm_id: int = Field(description="ID of the place")
    name: str = Field(description="Name of the place")
    category: dict = Field(description="Category names of the place")
    point: dict = Field(description="Lon (longitude) and lat (latitude) of the place")
    address: dict = Field(description="Contains road (street) address and jibun (land-lot) address")


class PlaceDetailResponse(BaseModel):
    menu: dict = Field({}, description="Menus if the place has menus")
    summary: PlaceSummary = Field(description="Summary of the place")
    business_hours: dict = Field(description="Details of business hours")
    photos: dict = Field(description="Contains counts (metadata) and photos of the place")
    blog_review: dict = Field(description="Review of the place in blogs")
    kakaomap_review: dict = Field(description="Review of the place on Kakap Map (optional)")
    find_way: dict = Field(description="Transit information nearby the place")
    place_add_info: dict = Field(description="Additional information of the place")
