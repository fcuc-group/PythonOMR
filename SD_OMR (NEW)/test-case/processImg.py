from PIL import Image


# - Blur.png
# - BlurAndSmall.png
# - Graded_OMR.png
# - MixBlur_Half.png
# - MixBlur_Half_2.png
# - MixSymbol.png
# - MixSymbol2.png
# - All.png
# - all_2.png

testImg = "All.png"

im = Image.open(testImg)
x, y = im.size

qrcode = Image.open("qrcode.png")
qrcode = qrcode.resize((250, 250))
image = Image.new("RGB", (x, y), (255, 255, 255))
image.paste(im, (0, 0))
image.paste(qrcode, (1200, 70))

image.show()
# image.save("omr/"+testImg)