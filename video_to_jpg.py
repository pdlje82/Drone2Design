import cv2
from exif import Image
from PIL import Image as PILImage
import math
import srt_parser
import piexif


def rad2dms(rad_angle):
    deg_angle = math.degrees(rad_angle)
    is_positive = deg_angle >= 0
    deg_angle = abs(deg_angle)
    minutes, seconds = divmod(deg_angle * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    degrees = degrees if is_positive else -degrees
    return degrees, minutes, seconds

def rad2dm(rad_angle):
    deg_angle = math.degrees(rad_angle)
    is_positive = deg_angle >= 0
    deg_angle = abs(deg_angle)
    degrees, minutes = divmod(deg_angle * 60, 60)
    degrees = degrees if is_positive else -degrees
    return degrees, minutes


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


def save_img(save_path, exif_img):
    mod_img = open(save_path, 'wb')
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
    if not exif_img.has_exif:
        print('ERROR: Image has no EXIF tags!!')
    if lon[0] < 0:
        lon = lon[0] * -1., lon[1]  # , lon[2]
        exif_img.gps_longitude_ref = 'W'
    else:
        exif_img.gps_longitude_ref = 'E'
    if lat[0] < 0:
        lat = lat[0] * -1., lat[1]  # , lat[2]
        exif_img.gps_latitude_ref = 'S'
    else:
        exif_img.gps_latitude_ref = 'N'
    exif_img.gps_longitude = lon
    exif_img.gps_latitude = lat
    print('lat: {} {}, \nlon: {} {}'.format(exif_img.gps_latitude_ref,
                                            exif_img.gps_latitude,
                                            exif_img.gps_longitude_ref,
                                            exif_img.gps_longitude))
    return exif_img


def set_exif_bytes(img_path):
    gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
               piexif.GPSIFD.GPSLatitudeRef: 'N',
               piexif.GPSIFD.GPSLongitudeRef: 'W',
               piexif.GPSIFD.GPSLatitude: (1, 0),
               piexif.GPSIFD.GPSLongitude: (1, 0),
               }
    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)
    im = PILImage.open(img_path)
    im.save(img_path, exif=exif_bytes)



def write_imgs(vid_path, save_path, gps_srt_path):
    count = 1
    vidcap = cv2.VideoCapture(vid_path)
    # Create srt dictionary with gps data for each frame
    srt_dict = srt_parser.frame_to_coordinates_dict(gps_srt_path)
    # Read first frame from video
    success, image = vidcap.read()
    if success:
        print('success reading 1st frame')
    while success:
        img_path = save_path + 'frame{}.jpg'.format(count)
        cv2.imwrite(img_path, image)     # save frame as JPEG file
        set_exif_bytes(img_path)
        exif_img = open_img(img_path)  # open the saved image to write exif data
        # Read gps data from srt_dict and convert to DMS
        print('Read gps data from srt_dict and convert to DMS...')
        latitude = float(srt_dict[str(count)]['lat'])
        longitude = float(srt_dict[str(count)]['lon'])
        latitude = rad2dm(latitude)
        longitude = rad2dm(longitude)
        # Write gps data to image
        exif_img_mod = write_exif_gps_data(exif_img, latitude, longitude)
        # Save image to disk
        save_img(img_path, exif_img_mod)
        count += 1
        success, image = vidcap.read()
        print('\nRead new frame, number {}: '.format(count))
        if count >= 5:
            break

# -----------------------------------------------------------------------------------------------------------


# Set paths for video and video-srt with gps data
video_path = './data/input/DJI_0007.MP4'  # path to DJI input video
# img_path = './data/input/gps_test_img.jpg'
save_img_path = './data/output/'
srt_path = './data/input/DJI_0007.SRT'


write_imgs(video_path, save_img_path, srt_path)


