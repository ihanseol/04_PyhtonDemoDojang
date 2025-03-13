import requests
from urllib.parse import urlencode
import json
from typing import Optional, Callable, Dict, Any, List, Union

# Constants
STATUS = {
    "OK": "OK",
    "ERROR": "ERROR",
    "ZERO_RESULT": "ZERO_RESULT"
}

SORT_BY = {
    "ACCURACY": "accuracy",
    "DISTANCE": "distance"
}

COORDS = {
    "TM": "TM",
    "WGS84": "WGS84",
    "WTM": "WTM",
    "CONGNAMUL": "CONGNAMUL",
    "WCONGNAMUL": "WCONGNAMUL"
}

ANALYZE_TYPE = {
    "SIMILAR": "similar",
    "EXACT": "exact"
}

# Configuration (replace with your actual API key)
APP_KEY = "here"  # Set your Kakao API key
APP_VERSION = "1.0"  # Example version, adjust as needed
DOMAIN = "https://dapi.kakao.com"
URL = {
    "GEO": f"{DOMAIN}/v2/local/geo/",
    "SEARCH": f"{DOMAIN}/v2/local/search/"
}

ERROR_MESSAGE = {
    "MISSING_ARGUMENTS": "매개변수가 누락되었습니다: ",
    "APIKEY_REQUIRED": "Daum Maps API를 위한 apikey가 존재하지 않습니다: apikey가 필요합니다.",
    "NOT_FOUND_NAMESPACE": "daum.maps 네임스페이스를 찾을 수 없습니다: Daum Maps Javascript Open API를 먼저 로드하십시오."
}

# Headers
KA_HEADER_STRING = f"sdk/{APP_VERSION} os/python lang/en device/python origin/http://localhost"
AUTH_HEADER_STRING = f"KakaoAK {APP_KEY}"


# Utility Functions
class Util:
    @staticmethod
    def extend(target: Dict, *sources: Dict) -> Dict:
        for source in sources:
            if source:
                target.update(source)
        return target

    @staticmethod
    def update(target: Dict, *sources: Dict) -> Dict:
        for source in sources:
            if source:
                for key, value in source.items():
                    if key in target:
                        target[key] = value
        return target

    @staticmethod
    def serialize(params: Dict) -> str:
        return urlencode({k: v for k, v in params.items() if v is not None})

    @staticmethod
    def to_lat_lng(coords) -> Dict:
        # Placeholder for coordinate conversion; assumes coords is a dict with 'x' and 'y'
        return coords


# Ajax-like HTTP Request Function
def ajax(url: str, params: Dict, oncomplete: Callable, onerror: Callable) -> None:
    headers = {
        "KA": KA_HEADER_STRING,
        "Authorization": AUTH_HEADER_STRING
    }
    try:
        response = requests.get(f"{url}?{Util.serialize(params)}", headers=headers)
        response.raise_for_status()
        oncomplete(response.json())
    except requests.RequestException:
        onerror()


# Request Factory
def request_factory(url: str, default_params: Dict, callback: Callable) -> Callable:
    def request(options: Dict = {}):
        params = Util.update(default_params.copy(), options)
        ajax(url, params,
             lambda data: callback(data, params),
             lambda: callback(None, None))

    return request


# Specific API Request Functions
def address_search(query: str, callback: Callable) -> Callable:
    return request_factory(
        f"{URL['SEARCH']}address.json",
        {"query": query, "page": 1, "size": 10, "analyze_type": None},
        callback
    )


def coord2regioncode(x: float, y: float, callback: Callable) -> Callable:
    return request_factory(
        f"{URL['GEO']}coord2regioncode.json",
        {"x": x, "y": y, "input_coord": None, "output_coord": None},
        callback
    )


def coord2address(x: float, y: float, callback: Callable) -> Callable:
    return request_factory(
        f"{URL['GEO']}coord2address.json",
        {"x": x, "y": y, "input_coord": None},
        callback
    )


def transcoord(x: float, y: float, callback: Callable) -> Callable:
    return request_factory(
        f"{URL['GEO']}transcoord.json",
        {"x": x, "y": y, "input_coord": None, "output_coord": None},
        callback
    )


def keyword_search(query: str, callback: Callable) -> Callable:
    return request_factory(
        f"{URL['SEARCH']}keyword.json",
        {"query": query, "category_group_code": None, "x": None, "y": None,
         "radius": None, "rect": None, "page": 1, "size": 15, "sort": None},
        callback
    )


def category_search(category_group_code: str, callback: Callable) -> Callable:
    return request_factory(
        f"{URL['SEARCH']}category.json",
        {"category_group_code": category_group_code, "x": None, "y": None,
         "radius": None, "rect": None, "page": 1, "size": 15, "sort": None},
        callback
    )


# Pagination Class
class Pagination:
    def __init__(self, meta: Dict, params: Dict, request: Callable):
        self.total_count = int(meta["pageable_count"])
        self.per_page = params["size"]
        self.current = params["page"]
        self.last = (self.total_count + self.per_page - 1) // self.per_page
        self.has_next_page = self.current < self.last
        self.has_prev_page = self.current > 1 and self.current <= self.last
        self.first = 1
        self._request = request

    def next_page(self):
        if self.has_next_page:
            self._request({"page": self.current + 1})

    def prev_page(self):
        if self.has_prev_page:
            self._request({"page": self.current - 1})

    def goto_page(self, page: int):
        if page > 0 and page <= self.last and page != self.current:
            self._request({"page": page})

    def goto_first(self):
        self._request({"page": 1})

    def goto_last(self):
        self._request({"page": self.last})


# Geocoder Class
class Geocoder:
    def address_search(self, query: str, callback: Callable, options: Dict = {}):
        def cb(data, params):
            if data:
                documents = data["documents"]
                status = STATUS["ZERO_RESULT"] if len(documents) == 0 else STATUS["OK"]
                callback(documents, status, Pagination(data["meta"], params, request))
            else:
                callback(None, STATUS["ERROR"], None)

        request = address_search(query, cb)
        request(options)

    def coord2regioncode(self, x: float, y: float, callback: Callable, options: Dict = {}):
        def cb(data, _):
            if data:
                callback(data["documents"], STATUS["OK"])
            else:
                callback(None, STATUS["ERROR"])

        request = coord2regioncode(x, y, cb)
        request(options)

    def coord2address(self, x: float, y: float, callback: Callable, options: Dict = {}):
        def cb(data, _):
            if data:
                documents = data["documents"]
                status = STATUS["ZERO_RESULT"] if len(documents) == 0 else STATUS["OK"]
                callback(documents, status)
            else:
                callback(None, STATUS["ERROR"])

        request = coord2address(x, y, cb)
        request(options)

    def transcoord(self, x: float, y: float, callback: Callable, options: Dict = {}):
        def cb(data, _):
            if data:
                documents = data["documents"]
                status = STATUS["ZERO_RESULT"] if len(documents) == 0 else STATUS["OK"]
                callback(documents, status)
            else:
                callback(None, STATUS["ERROR"])

        request = transcoord(x, y, cb)
        request(options)


# Places Class
class Places:
    def __init__(self, map_obj=None):
        self.map = map_obj

    def set_map(self, map_obj):
        self.map = map_obj

    def keyword_search(self, query: str, callback: Callable, options: Dict = {}):
        def cb(data, params):
            if data:
                documents = data["documents"]
                status = STATUS["ZERO_RESULT"] if len(documents) == 0 else STATUS["OK"]
                callback(documents, status, Pagination(data["meta"], params, request))
            else:
                callback(None, STATUS["ERROR"], None)

        # Placeholder for map-related logic (e.g., bounds, center)
        request = keyword_search(query, cb)
        request(options)

    def category_search(self, category_group_code: str, callback: Callable, options: Dict = {}):
        def cb(data, params):
            if data:
                documents = data["documents"]
                status = STATUS["ZERO_RESULT"] if len(documents) == 0 else STATUS["OK"]
                callback(documents, status, Pagination(data["meta"], params, request))
            else:
                callback(None, STATUS["ERROR"], None)

        # Placeholder for map-related logic (e.g., bounds, center)
        request = category_search(category_group_code, cb)
        request(options)


# Example Usage
if __name__ == "__main__":
    geocoder = Geocoder()


    def print_results(documents, status, pagination=None):
        print(f"Status: {status}")
        if documents:
            print("Documents:", documents)
        if pagination:
            print(f"Total Count: {pagination.total_count}, Current Page: {pagination.current}")


    # Example address search
    geocoder.address_search("서울시 강남구", print_results)
