from PIL import Image, ImageDraw, ImageFont


async def create_demot(user_photo, user_text_frst, user_text_sec):


    demotivator = Image.new('RGB', (1000, 1000), color='black')
    draw = ImageDraw.Draw(demotivator)
    draw.rectangle((170, 70, 830, 730), fill='black', outline=(255, 255, 255), width=3)

    photo = Image.open(user_photo)  # your_pict.png - your picture
    resize_photo = photo.resize((620, 620))

    new_x, new_y = resize_photo.size
    bs_x, bs_y = demotivator.size

    x1 = (bs_x - new_x) // 2
    y1 = ((bs_y - new_y) // 2) - 100
    demotivator.paste(resize_photo, (x1, y1))

    # --- TEXT-1 ---

    text_first = user_text_frst

    font = ImageFont.truetype('/usr/share/fonts/TTF/OpenSans-Light.ttf', size=70)

    text_width_1, text_height_1 = draw.textsize(text_first, font=font)
    x2 = (demotivator.width - text_width_1) // 2
    y2 = 760
    draw.text((x2, y2), text_first, font=font, fill=(255, 255, 255))

    # --- TEXT-2 ---

    text_second = user_text_sec

    font = ImageFont.truetype('/usr/share/fonts/TTF/OpenSans-Light.ttf', size=35)

    text_width_2, text_height_2 = draw.textsize(text_second, font=font)
    new_x2 = (demotivator.width - text_width_2) // 2
    new_y2 = 880
    draw.text((new_x2, new_y2), text_second, font=font, fill=(255, 255, 255))

    demotivator.save('demotivator.png')