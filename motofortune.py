#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, ImageColor
import sys
import os


SCREENSIZE = (1600, 900)


def put_text_in_box(draw, text, topleft, botright):
  # iteratively decrease font size until it fits
  # text is already assumed to have newlines and formatting
  fontsize = 68
  height = botright[1] - topleft[1]
  width = botright[0] - topleft[0]
  txtcolor = ImageColor.getrgb("white")
  while fontsize > 10:
    font = ImageFont.truetype("/usr/fonts/ttf/times.ttf", size=fontsize)
    assert font
    (x,y) = draw.multiline_textsize(text, font=font)
    if x > width or y > height:
      fontsize -= 4
    else:
      # time to center
      xslack = width - x
      yslack = height - y
      topcoord = (topleft[0]+int(xslack / 2), topleft[1] + int(yslack / 2))
      draw.multiline_text(topcoord, text, txtcolor, font)
      return
  print("could not fit %s into given box" % text)
  raise ValueError
      

def render(quote, idx, outdir):
  img = Image.new("RGB", SCREENSIZE)  # default to black background
  draw = ImageDraw.Draw(img)  # jesus who named these functions?
  put_text_in_box(draw, "%s" % quote, (100, 100), (1500, 800))
  img.save(os.path.join(outdir, "%d.jpg" % idx))



def main():
  if len(sys.argv) < 3:
    print("usage: %s path/to/quotes path/to/outdir" % sys.argv[0])
    exit(1)

  assert os.path.isfile(sys.argv[1])
  assert os.path.isdir(sys.argv[2])

  lines = open(sys.argv[1]).read().split("\n")
  quote = ""
  count = 0
  for i in range(len(lines)):
    if lines[i].rstrip() == "%":
      try:
        render(quote.rstrip(), count, sys.argv[2])
        count += 1
      except ValueError:
        pass
      quote = ""
    else:
      quote += lines[i]+"\n"


  


if __name__ == "__main__":
  main()

