from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class ImageMetaData(object):
    """
    Extract the exif data from any image. Data includes GPS coordinates,
    Focal Length, Manufacture, and more.
    """
    exif_data = None
    image = None

    def __init__(self, img_path):
        self.image = Image.open(img_path)
        # print(self.image._getexif())
        self.get_exif_data()
        super(ImageMetaData, self).__init__()

    def get_exif_data(self):
        """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
        exif_data = {}
        info = self.image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        self.exif_data = exif_data
        return exif_data

    @staticmethod
    def get_if_exist(data, key):
        if key in data:
            return data[key]
        return None

    @staticmethod
    def convert_to_degress(value):

        """Helper function to convert the GPS coordinates
        stored in the EXIF to degress in float format"""

        d = value[0]
        m = value[1]
        s = value[2]

        return d + (m / 60.0) + (s / 3600.0)

    def get_lat_lng(self):
        """
            Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
        """
        lat = None
        lng = None
        exif_data = self.get_exif_data()
        # print(exif_data)
        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            gps_latitude = self.get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = self.get_if_exist(gps_info, 'GPSLatitudeRef')
            gps_longitude = self.get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = self.get_if_exist(gps_info, 'GPSLongitudeRef')
            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self.convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":
                    lat = 0 - lat
                lng = self.convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    lng = 0 - lng
        return lat, lng


path_name = 'c:/Users/minhwasoo/Downloads/20230928_175232.jpg'

meta_data = ImageMetaData(path_name)
latlng = meta_data.get_lat_lng()
print(latlng)
exif_data = meta_data.get_exif_data()
print(exif_data)
