import piexif
from PIL import Image as PILImage
from fractions import Fraction

gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           piexif.GPSIFD.GPSLatitudeRef: 'N',
           piexif.GPSIFD.GPSLongitudeRef: 'W',
           piexif.GPSIFD.GPSLatitude: (37429289, 1000000),
           piexif.GPSIFD.GPSLongitude: (122138162, 1000000),
           }

exif_dict = {"GPS": gps_ifd}
exif_bytes = piexif.dump(exif_dict)
im = PILImage.open('./data/output/frame1.jpg')
im.save("out.jpg", exif=exif_bytes)


print(37429289. / 1000000)
print(122138162. / 1000000)

f = Fraction(str(37.429289))
print(f.numerator, f.denominator)

