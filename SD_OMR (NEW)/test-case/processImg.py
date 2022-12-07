from PIL import Image


# - Blur.png
# - BlurAndSmall.png
# - Graded_OMR.png
# - MixBlur_Half.png
# - MixBlur_Half_2.png
# - MixSymbol.png
# - MixSymbol2.png
# - all.png
# - all_2.png

testImg = "all_2.png"

im = Image.open(testImg)
x, y = im.size

qrcode = Image.open("qrcode.png")
qrcode = qrcode.resize((100, 100))
image = Image.new("RGB", (x, y), (255, 255, 255))
image.paste(im, (0, 0))
print(im.size)
print(x)
print(y)
image.paste(qrcode, (550,40))

#image.show()
image.save("omr/"+testImg)