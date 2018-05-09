from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageColor
from colour import Color
import sys

def textify(text, filename):
    image = Image.open(filename)
    width, height = image.size

    bottom_padding = int(height / 5)
    colors = [
        Color("red"), 
        Color("orange"), 
        Color("yellow"),
        Color("green"),
        Color("blue"),
        Color("indigo"), 
        Color("violet")
    ]

    chunk_width = int(width / 5)

    gradient_buffer = []

    for x in range(len(colors) - 2):
        gradient_buffer = gradient_buffer + list(colors[x].range_to(
            colors[x + 1], chunk_width
            ))
    
    if (len(gradient_buffer) < width):
        diff = width - len(gradient_buffer)
        extense = [gradient_buffer[len(gradient_buffer) - 1]] * diff
        gradient_buffer = gradient_buffer + extense

    x_height = height + bottom_padding
    expanded = Image.new('RGBA', (width, x_height))
    draw = ImageDraw.Draw(expanded)

    for i in range(width):
        posx = (i, 0) # y is ALWAYS 0
        posy = (i, x_height)

        rgb = ImageColor.getrgb(gradient_buffer[i].get_hex())
        
        draw.line([posx, posy], fill=rgb, width=1)

    expanded.paste(image)
    image.close()
    fontsize = 1
    font = ImageFont.truetype("Comic_Sans_MS.ttf", fontsize)

    goal = width / 2

    while(font.getsize(text)[0] < goal):
        fontsize += 1
        font = ImageFont.truetype("Comic_Sans_MS.ttf", fontsize)

    font_width, _ = font.getsize(text)
    posx = (width / 2) - (font_width / 2)
    posy = height

    draw.text((posx, posy), text, font=font)

    return expanded
    

def rainbowify(image, output="test.png"):

    if image.format == "GIF":
        image = image.convert("RGB")

    rainbow = Image.open("assets/rainbow.jpg")

    rainbow = ImageOps.fit(rainbow, (image.size)).convert(image.mode)
    blended = Image.blend(image, rainbow, 0.5)
    blended.save(output)

