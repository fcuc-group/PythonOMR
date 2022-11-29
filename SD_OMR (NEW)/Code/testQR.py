# QR Code
from pyzbar.pyzbar import decode
from PIL import Image

decocdeQR = decode(Image.open("../Code/form_qr.png"))       #change path
# print(decocdeQR[0].data.decode('ascii'))
studentDetails = decocdeQR[0].data.decode('ascii')
print(studentDetails)