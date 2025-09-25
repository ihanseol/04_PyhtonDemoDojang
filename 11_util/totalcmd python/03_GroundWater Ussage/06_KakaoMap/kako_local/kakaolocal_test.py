import asyncio
from mcp_kakao_local.kakao_local_client import KakaoLocalClient
from mcp_kakao_local.models import CategoryGroupCode, Coordinate, LocationSortOption


# This is the main function to run our example
async def main():
    # Create our robot helper
    client = KakaoLocalClient()

    # Let’s find pizza shops near a spot in Seoul
    center = Coordinate(latitude="37.5665", longitude="126.9780")  # Convert to strings
    keyword = "pizza"  # We want pizza shops
    radius = 1000  # Look within 1 kilometer

    # Ask the robot to search for pizza shops
    search_result = await client.search_by_keyword(
        keyword=keyword,
        category_group_code=CategoryGroupCode.FD6,  # FD6 is for food places
        center=center,
        radius=radius,
        size=5,  # Get 5 results
        sort_option=LocationSortOption.DISTANCE  # Sort by closest
    )

    # Print the names of the pizza shops we found
    print("Pizza shops found:")
    for place in search_result.documents:
        print(f"- {place.place_name} (Distance: {place.distance}m)")

    # If we found at least one place, let’s get details about the first one
    if search_result.documents:
        place_id = search_result.documents[0].id  # Get the ID of the first place
        details = await client.get_place_details(place_id)
        print("\nDetails for", details.basicInfo.placenamefull)
        print("Address:", details.basicInfo.address)
        print("Phone:", details.basicInfo.phonenum)


# Run the example
if __name__ == "__main__":
    asyncio.run(main())
