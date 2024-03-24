from PIL import Image

FACTOR  = 5

img_path = r"d:\05_Send\screenshot_s.jpg"
img = Image.open(img_path)     # puts our image to the buffer of the PIL.Image object

width, height = img.size
asp_rat = width/height

# Enter new width (in pixels)
new_width = width * FACTOR

# Enter new height (in pixels)
new_height = height * FACTOR

new_rat = new_width/new_height

if (new_rat == asp_rat):
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# adjusts the height to match the width
# NOTE: if you want to adjust the width to the height, instead ->
# uncomment the second line (new_width) and comment the first one (new_height)
else:
    new_height = round(new_width / asp_rat)
    #new_width = round(new_height * asp_rat)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# usage: resize((x,y), resample)
# resample filter -> PIL.Image.BILINEAR, PIL.Image.NEAREST (default), PIL.Image.BICUBIC, etc..
# https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.Image.resize

# Enter the name under which you would like to save the new image
img.save("outputname.png")


