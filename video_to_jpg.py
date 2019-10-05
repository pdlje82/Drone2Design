import cv2
from exif import Image
import math
import pyproj
import numpy as np


def write_imgs():
    vidcap = cv2.VideoCapture('./data/input/DJI_0007.MP4')
    success, image = vidcap.read()
    print(success, image)
    count = 0
    while success:
        cv2.imwrite("./data/output/frame%d.jpg" % count, image)     # save frame as JPEG file
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1


def rad2dms(rad_angle):
    deg_angle = math.degrees(rad_angle)
    is_positive = deg_angle >= 0
    deg_angle = abs(deg_angle)
    minutes, seconds = divmod(deg_angle * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    degrees = degrees if is_positive else -degrees
    return degrees, minutes, seconds


# def transform_crs(lon, lat, crs='4326'):
#     """ CRS 4326 --> WGS 84 -- WGS84 - World Geodetic System 1984, used in GPS
#     Coordinate system: Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree """

#     print(lon_deg, lat_deg)
#     crs = pyproj.CRS.from_epsg(crs)
#     wgs84 = pyproj.Transformer.from_crs(crs.geodetic_crs, crs)
#     x1, y1 = wgs84.transform(lon_deg, lat_deg)
#     print(x1, y1)
#     return x1, y1


def open_img(img_path):
    img = open(img_path, 'rb')
    exif_img = Image(img)
    return exif_img

def save_img(save_img_path):
    mod_img = open(save_img_path, 'wb')
    mod_img.write(exif_img.get_file())


def read_exif_data(exif_img):
    if exif_img.has_exif:
        exif_list = dir(exif_img)
        gps_entries = [e for e in exif_list if 'gps' in e]
        print('\n')
        for e in gps_entries:
            print(e)
            print(getattr(exif_img, e))
        print('\n')

def write_exif_gps_data(exif_img, lat, lon):
    if lon[0] < 0:
        lon = lon[0] * -1., lon[1], lon[2]
        exif_img.gps_longitude_ref = 'W'
    else:
        exif_img.gps_longitude_ref = 'E'
    if lat[0] < 0:
        lat = lat[0] * -1., lat[1], lat[2]
        exif_img.gps_latitude_ref = 'S'
    else:
        exif_img.gps_latitude_ref = 'N'
    exif_img.gps_longitude = lon
    exif_img.gps_latitude = lat

# -----------------------------------------------------------------------------------------------------------

img_path = './data/output/gps_test_img.jpg'
save_img_path = './data/input/gps_test_img_modified.jpg'
exif_img = open_img(img_path)
read_exif_data(exif_img)


longitude = -0.041806
latitude = 0.645039

# pos_lon, pos_lat = transform_crs(longitude, latitude)

pos_lon1 = rad2dms(longitude)
pos_lat1 = rad2dms(latitude)

print('\nlongitude = {}, \nlatitude = {}'.format(pos_lon1, pos_lat1))

write_exif_gps_data(exif_img, pos_lat1, pos_lon1)

read_exif_data(exif_img)

save_img(save_img_path)



