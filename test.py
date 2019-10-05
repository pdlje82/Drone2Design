import piexif
from PIL import Image as PILImage
from exif import Image
import math

gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           piexif.GPSIFD.GPSLatitudeRef: 'N',
           piexif.GPSIFD.GPSLongitudeRef: 'W',
           piexif.GPSIFD.GPSLatitude: (1, 0),
           piexif.GPSIFD.GPSLongitude: (1, 0),
           }

exif_dict = {"GPS": gps_ifd}
exif_bytes = piexif.dump(exif_dict)
im = PILImage.open('./data/output/frame1.jpg')
im.save("out.jpg", exif=exif_bytes)


def open_img(img_path):
    img = open(img_path, 'rb')
    exif_img = Image(img)
    return exif_img


def read_exif_data(exif_img):
    if exif_img.has_exif:
        exif_list = dir(exif_img)
        gps_entries = [e for e in exif_list if 'gps' in e]
        print('\n')
        for e in gps_entries:
            print(e)
            print(getattr(exif_img, e))
        print('\n')


def rad2dm(rad_angle):
    deg_angle = math.degrees(rad_angle)
    is_positive = deg_angle >= 0
    deg_angle = abs(deg_angle)
    degrees, minutes = divmod(deg_angle * 60, 60)
    degrees = degrees if is_positive else -degrees
    return degrees, minutes

print(rad2dm(1.123))


print(divmod(math.degrees(1.123) * 60, 60))






