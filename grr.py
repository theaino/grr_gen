from PIL import Image, ImageFont, ImageDraw
from sys import argv
from urllib import request
import io


grr = Image.open("grr.png")
spacewidth, spaceheight = grr.width, int(grr.height / 3)

other = ""

if argv[1].startswith("http://") or argv[1].startswith("https://"):
    with request.urlopen(argv[1]) as i:
        other = io.BytesIO(i.read())
    other = Image.open(other)
else:
    font = ImageFont.truetype("grr.ttf", 500)
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bbox = draw.textbbox((0, 0), argv[1], font=font)
    other = Image.new("RGB", (bbox[2], bbox[3]), (255, 255, 255))
    draw = ImageDraw.Draw(other)
    draw.text((0, 0), argv[1], fill=(0, 0, 0), font=font)


padding = spaceheight // 5

if spacewidth / spaceheight > other.width / other.height:
    other = other.resize((int(other.width / other.height * spaceheight) - padding, spaceheight - padding))
else:
    other = other.resize((spacewidth - padding, int(other.height / other.width * spacewidth) - padding))

dst = Image.new("RGB", (grr.width, grr.height + spaceheight))
dst.paste(grr, (0, spaceheight))

dst.paste(Image.new("RGB", (spacewidth, spaceheight), (255, 255, 255)))

dst.paste(other, ((spacewidth - other.width) // 2, (spaceheight - other.height) // 2))

dst.save("out.png")
