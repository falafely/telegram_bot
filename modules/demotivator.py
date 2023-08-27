from PIL import Image, ImageDraw, ImageFont


async def create_demot(user_photo, user_text):

    demotivator = Image.new('RGB', (1000, 1000), color='black')
    draw = ImageDraw.Draw(demotivator)
    draw.rectangle((170, 170, 830, 830), fill='black', outline=(255, 255, 255), width=3)

    photo = Image.open(user_photo)  # replace picture
    resize_photo = photo.resize((600, 600))

    new_x, new_y = resize_photo.size
    bs_x, bs_y = demotivator.size
    a = (bs_x - new_x) // 2
    b = (bs_y - new_y) // 2
    demotivator.paste(resize_photo, (a, b))

    text = user_text

    font = ImageFont.truetype('/usr/share/fonts/TTF/AkaashNormal.ttf', size=50)  # replace font

    text_width, text_height = draw.textsize(text, font=font)
    x = (demotivator.width - text_width) // 2
    y = 900
    draw.text((x, y), text, font=font, fill=(255, 255, 255))  # replace coordinates

    demotivator.save('demotivator.jpg')
