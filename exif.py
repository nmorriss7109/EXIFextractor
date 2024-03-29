#-*- coding: utf-8 -*-
try:
    import os
    import math
    import PIL
    import PIL.Image as PILimage
    from PIL import ImageDraw, ImageFont, ImageEnhance
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError as err:
    exit(err)

class Worker(object):
    def __init__(self, img):
        self.img = img
        self.get_exif_data()
        self.lat = self.get_lat()
        self.lon = self.get_lon()
        self.date =self.get_date_time()
        super(Worker, self).__init__()

    @staticmethod
    def get_if_exist(data, key):
        if key in data:
            return data[key]
        return None

    @staticmethod
    def convert_to_degress(value):
        """Helper function to convert the GPS coordinates
        stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)
        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    @staticmethod
    def convert_to_DegMinSec(value):
        deg = math.floor(int(value))
        value = abs(60*(value - deg))
        min = math.floor(int(value))
        value = 60*(value - min)
        sec = math.floor(value)
        output = str(int(deg)) + '° ' + str(int(min)) + '\' ' + str(sec) + '\"'
        return output

    def get_exif_data(self):
        """Returns a dictionary from the exif data of an PIL Image item. Also
        converts the GPS Tags"""
        exif_data = {}
        info = self.img._getexif()
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
        # return exif_data

    def get_lat(self):
        """Returns the latitude and longitude, if available, from the
        provided exif_data (obtained through get_exif_data above)"""
        # print(exif_data)
        if 'GPSInfo' in self.exif_data:
            gps_info = self.exif_data["GPSInfo"]
            gps_latitude = self.get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = self.get_if_exist(gps_info, 'GPSLatitudeRef')
            if gps_latitude and gps_latitude_ref:
                lat = self.convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":
                    lat = 0 - lat
                #lat = str("{lat:.{5}f}")
                return self.convert_to_DegMinSec(lat)
        else:
            return None

    def get_lon(self):
        """Returns the latitude and longitude, if available, from the
        provided exif_data (obtained through get_exif_data above)"""
        # print(exif_data)
        if 'GPSInfo' in self.exif_data:
            gps_info = self.exif_data["GPSInfo"]
            gps_longitude = self.get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = self.get_if_exist(gps_info, 'GPSLongitudeRef')
            if gps_longitude and gps_longitude_ref:
                lon = self.convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                	lon = 0 - lon
                #lon = str("{lon:.{5}f}")
                return self.convert_to_DegMinSec(lon)
        else:
            return None

    def get_date_time(self):
        if 'DateTime' in self.exif_data:
            date_and_time = self.exif_data['DateTime']
            return date_and_time


def main():
    date = image.date
    print(date)

directory = 'images/'

if __name__ == '__main__':
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                img = PILimage.open(directory + filename)
                image = Worker(img)
                lat = image.lat
                lon = image.lon
                date = image.date
                print("Filename:  " + filename)
                print("Date:      " + date)
                if (lon != None and lat != None):
                    print("Latitiude: " + lat)
                    print("Longitude: " + lon)
                else:
                    print("Latitiude: Not Found")
                    print("Longitude: Not Found")
                    
                print
                continue
            else:
                continue


    except Exception as e:
        print(e)
