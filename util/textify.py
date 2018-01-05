from PIL import ImageFont, ImageDraw, Image

def textify(text, filename, output, position=(0,0)):
    rainbowed = Image.open(filename)
    draw = ImageDraw.Draw(rainbowed)
    font = ImageFont.truetype("Comic_Sans_MS.ttf", 48)

    draw.text(position, text, font=font)

    rainbowed.save(output)