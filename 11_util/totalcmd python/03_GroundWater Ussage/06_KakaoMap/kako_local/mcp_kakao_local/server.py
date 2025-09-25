from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp_kakao_local.kakao_local_client import KakaoLocalClient
from mcp_kakao_local.models import (
  AddressResponse,
  CategoryGroupCode,
  Coordinate,
  LocationSearchResponse,
)
from pydantic import Field

load_dotenv()

kakao_local_client = KakaoLocalClient()

INSTRUCTIONS = """
Kakao Local MCP provides tools for retrieving location information within South Korea.
Availalble tools are listed in <tools> and recsources are listed in <resources>. You must follow all <rules>.

<tools>
- find_coordinates: Finds the coordinates of a given [address]. The response contains a list of [document],
  each of which includes the matched address ([address_name]), longitude ([x]), and latitude ([y]).
- search_by_keyword: Searches for places related to the keyword. Users can provide [category_group_code],
  [center_coordinate], and [radius_from_center] to narrow down the search results.
- search_by_category: Searches for places with matching category group code.
- get_place: Fetches details for a place such as name, address, reviews, photos and etc. The [place_id] parameter corresponds to a document ID from the location search results.
</tools>

<resources>
- resource://category_group_code: Returns all category group codes supported by Kakao Local API
</resources>

<rules>
- If the response contains [meta], which is the metadata of a result, you can get paging information from response.
  [is_end] is a boolean value indicating whether a returned page is the last one. If a user wants to get more results,
  you can call the same tool with an increased [page], if supported, unless the last result is the last page.
- When making consecutive calls to the same MCP tool, wait for a random duration selected between 0 ms and 50ms and
  use exponential backoff between calls.
- [category_group_code] must be one of [CategoryGroupCode] names (available in <resources>). Values of [CategoryGroupCode] are descriptions, which cannot be used in <tools>.
</rules>
""".strip()

mcp = FastMCP("mcp_kakao_local", instructions=INSTRUCTIONS)


@mcp.tool(description="Find coordinates of a given address")
async def find_coordinates(
  address: str = Field(description="address to search for", min_length=1),
  page: int = Field(1, description="page number of result", ge=1),
) -> AddressResponse:
  """
  Returns:
    AddressResponse: An object containing metadata and a list of addresses
  """
  try:
    response = await kakao_local_client.find_coordinates(address, page=page)
    if len(response.documents) == 0:
      return {"success": False, "error": "No coordinates found. Check if the address is correct."}

    return response
  except Exception as ex:
    return {"success": False, "error": str(ex)}


@mcp.tool(description="Searches for places related to the keyword")
async def search_by_keyword(
  keyword: str = Field(description="keyword used to search for places", min_length=1),
  category_group_code: CategoryGroupCode | None = Field(
    None, description="category used for filtering results (CategoryGroupCode resource)"
  ),
  center_coordinate: Coordinate | None = Field(
    None, description="longitude and latitude of a center"
  ),
  radius_from_center: int | None = Field(
    None, description="search radius from the center in meters", gt=0
  ),
  page: int = Field(1, description="page number of result", ge=1),
) -> LocationSearchResponse:
  """
  Returns:
    LocationSearchResponse: An object containing metadata and a list of places.
  """
  if center_coordinate:
    assert radius_from_center is not None
  if radius_from_center:
    assert center_coordinate is not None

  try:
    return await kakao_local_client.search_by_keyword(
      keyword,
      category_group_code,
      center_coordinate,
      radius_from_center,
      page=page,
    )
  except Exception as ex:
    return {"success": False, "error": str(ex)}


@mcp.tool(description="Searches for places with matching category group code")
async def search_by_category(
  category_group_code: CategoryGroupCode = Field(
    description="category used to search for places (CategoryGroupCode resource)"
  ),
  center_coordinate: Coordinate = Field(description="longitude and latitude of a center"),
  radius_from_center: int = Field(description="search radius from the center in meters", gt=0),
  page: int = Field(1, description="page number of result", ge=1),
) -> LocationSearchResponse:
  """
  Returns:
    LocationSearchResponse: An object containing metadata and a list of places.
  """
  try:
    return await kakao_local_client.search_by_category(
      category_group_code,
      center_coordinate,
      radius_from_center,
      page=page,
    )
  except Exception as ex:
    return {"success": False, "error": str(ex)}


@mcp.tool(description="Fetches details for a place such as name, address, reviews, photos and etc")
async def get_place(
  place_id: int = Field(
    description="ID of a place, which is document ID in location search results", ge=1
  ),
) -> dict:
  """
  Returns:
    PlaceDetailResponse: An object containing details of the place
  """
  try:
    return await kakao_local_client.get_place_details(place_id)
  except Exception as ex:
    return {"success": False, "error": str(ex)}


@mcp.resource(
  uri="resource://category_group_code",
  name="CategoryGroupCode",
  description="Get all category group codes",
)
def get_category_group_code() -> dict:
  return {c.name: c.value for c in CategoryGroupCode}
