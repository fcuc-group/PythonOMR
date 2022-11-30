# QR Code
from pyzbar.pyzbar import decode
from PIL import Image

decocdeQR = decode(Image.open("20221129-163604.png"))       #change path
# print(decocdeQR[0].data.decode('ascii'))
studentDetails = decocdeQR[0].data.decode('ascii')
print(studentDetails)