import cv2
from PIL import Image as PILImage
import math
import srt_parser
import piexif
from fractions import Fraction

# def transform_crs(lon, lat, crs='4326'):
#     """ CRS 4326 --> WGS 84 -- WGS84 - World Geodetic System 1984, used in GPS
#     Coordinate system: Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree """

#     print(lon_deg, lat_deg)
#     crs = pyproj.CRS.from_epsg(crs)
#     wgs84 = pyproj.Transformer.from_crs(crs.geodetic_crs, crs)
#     x1, y1 = wgs84.transform(lon_deg, lat_deg)
#     print(x1, y1)
#     return x1, y1



def set_exif_bytes(img_path, latitude, longitude):
    if latitude < 0:
        latitude *= -1.
        latitude_ref = 'S'
    else:
        latitude_ref = 'N'
    if longitude < 0:
        longitude *= -1.
        longitude_ref = 'W'
    else:
        longitude_ref = 'E'

    print('lat: {} {}, \nlon: {} {}'.format(latitude_ref,
                                            latitude,
                                            longitude_ref,
                                            longitude))

    fract_latitude = Fraction(str(round(latitude, 8)))
    fract_longitude = Fraction(str(round(longitude, 8)))
    print(fract_latitude.numerator, fract_latitude.denominator),
    print(fract_longitude.numerator, fract_longitude.denominator)
    gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 2, 0, 0),
               piexif.GPSIFD.GPSLatitudeRef: latitude_ref,
               piexif.GPSIFD.GPSLongitudeRef: longitude_ref,
               piexif.GPSIFD.GPSLatitude: [fract_latitude.numerator, fract_latitude.denominator],
               piexif.GPSIFD.GPSLongitude: [fract_longitude.numerator, fract_longitude.denominator],
               }

    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)
    im = PILImage.open(img_path)
    im.save(img_path, exif=exif_bytes)


def write_imgs(vid_path, save_path, gps_srt_path, frequ):
    count = 1
    vidcap = cv2.VideoCapture(vid_path)
    # Create srt dictionary with gps data for each frame
    srt_dict = srt_parser.frame_to_coordinates_dict(gps_srt_path)
    # Read first frame from video
    success, image = vidcap.read()
    if success:
        print('success reading 1st frame')
    while success:
        print(count % frequ)
        if count % frequ == 1:
            img_path = save_path + 'frame{}.jpg'.format(count)
            cv2.imwrite(img_path, image)     # save frame as JPEG file
            # Read gps data from srt_dict and convert to DMS
            print('Read gps data from srt_dict and convert to DD...')
            latitude = float(srt_dict[str(count)]['lat'])
            longitude = float(srt_dict[str(count)]['lon'])
            latitude = math.degrees(latitude)  # convert from rad to deg
            longitude = math.degrees(longitude)  # convert from rad to deg
            # Write gps data to image
            set_exif_bytes(img_path, latitude, longitude)
            success, image = vidcap.read()
        count += 1
        print('\nRead new frame, number {}: '.format(count))
        # if count >= 202:
        #     break

def read_exif(path):
    exif_dict = piexif.load(path)
    for ifd_name in exif_dict:
        print("\n{0} IFD:".format(ifd_name))
        for key in exif_dict[ifd_name]:
            try:
                print(key, exif_dict[ifd_name][key][:10])
            except:
                print(key, exif_dict[ifd_name][key])


# -----------------------------------------------------------------------------------------------------------


# Set paths for video and video-srt with gps data
video_path = './data/input/DJI_0007.MP4'  # path to DJI input video
# img_path = './data/input/gps_test_img.jpg'
save_img_path = './data/output/'
srt_path = './data/input/DJI_0007.SRT'


write_imgs(video_path, save_img_path, srt_path, frequ=10)

# read_exif('./data/output/frame1.jpg')


