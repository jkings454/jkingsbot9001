from PIL import Image, ImageOps
import sys

def rainbowify(image, output="test.png"):

    if image.format == "GIF":
        image = image.convert("RGB")

    rainbow = Image.open("assets/rainbow.jpg")

    rainbow = ImageOps.fit(rainbow, (image.size)).convert(image.mode)
    blended = Image.blend(image, rainbow, 0.5)
    blended.save(output)

if __name__ == "__main__":
    img = Image.open(sys.argv[1])
    rainbowify(img)
