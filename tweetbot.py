import datetime
import os

from numpy.lib.nanfunctions import _replace_nan
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qmeshi.settings')

from PIL import Image, ImageDraw, ImageFont
import tweepy
import django
django.setup()

from qmeshi_app.models import Menu, Cafeteria


dir = os.path.dirname(os.path.abspath(__file__))
media_dir = os.path.join(dir, 'media/tweetbot')
ttfont_name = os.path.join(dir, 'azukiP.ttf')
font_size = 36
canvas_size = (900, 1200)
background_rgb = (255, 255, 255)
text_rgb = (0, 0, 0)

CK = os.environ['TWITTER_CK']
CS = os.environ['TWITTER_CS']
AT = os.environ['TWITTER_AT']
AS = os.environ['TWITTER_AS']
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

today = datetime.date.today()


def create_menu(names, _replace=('', '')):
    menu_str = ''
    for name in names:
        cafeteria = Cafeteria.objects.get(short_name=name)
        menues = Menu.objects.filter(start_date__lte=today, end_date__gte=today, cafeteria=cafeteria)
        menu_str += f'【{cafeteria.name}】\n\n'
        menu_items = [ (f'（{menu.period}）\n' if menu.period!='' else '') + menu.item.name for menu in menues ]
        menu_str += '\n'.join(menu_items) if len(menu_items) > 0 else 'メニューが公開されていません'
        menu_str += '\n\n'
    return menu_str


def create_image(name, menu_str):
    img  = Image.new('RGB', canvas_size, background_rgb)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(ttfont_name, font_size)
    text_top_left = (canvas_size[0]//12, canvas_size[1]//12)
    draw.text(text_top_left, menu_str, fill=text_rgb, font=font)
    img.save(os.path.join(media_dir, f'{name}.jpg'))
    return os.path.join(media_dir, f'{name}.jpg')

# 画像生成
images = []
images.append(create_image('main', create_menu(['daily', 'main'], _replace=('・', '\n・'))))
images.append(create_image('center', create_menu(['quasis', 'dining'])))
images.append(create_image('west', create_menu(['rishoku', 'ajiya', 'ecafe', 'rantan'])))
images.append(create_image('bigdora', create_menu(['dora'])))

# ツイート
media_ids = []
weekdays = ['月', '火', '水' , '木', '金', '土', '日']
text = f'{today.strftime("%Y/%m/%d")} ({weekdays[today.weekday()]}) のメニュー' 
for filename in images:
    res = api.media_upload(filename)
    media_ids.append(res.media_id)
_ = api.update_status(status=text, media_ids=media_ids)

print('finished.')