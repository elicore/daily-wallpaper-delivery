# %%
import datetime
import requests
import json

SPOTLIGHT_URL = ('https://arc.msn.com/v3/Delivery/Placement?'
        'pid=209567'  # Public subscription ID for Windows lockscreens. Do not change this value
        '&fmt=json'  # Output format, e.g. json
        # '&rafb=0'  # Purpose currently unknown, optional
        '&ua=WindowsShellClient%2F0'  # Client user agent string
        '&cdm=1'  # Purpose currently unknown, cdm=1
        '&disphorzres=2560'  # Screen width in pixels (9999)
        '&dispvertres=1440'  # Screen height in pixels (9999)
        # '&lo=80217'  # Purpose currently unknown, optional
        '&pl={locale}'  # Locale, e.g. en-US
        '&lc={locale}'  # Language, e.g. en-US
        '&ctry=us'  # Country, e.g. us
        # '&time={time}'  # Time, e.g. 2017-12-31T23:59:59Z
        )

CAPTION_TEMPLATE = (
    '<b>{image_title}</b>\n'
    '{image_description}\n'
    '\n<u>{item_title}</u>\n'
    '\n<a href="{cta_url}">{cta_text}</a> '
    '(<a href="{item_url}">{item_copyright_text}</a>)\n'
)

## SAMPLE
# {'image_fullscreen_001_landscape': {'t': 'img', 'w': '1920', 'h': '1080',
#   'u': 'https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE4U03H?ver=0771',
#   'sha256': '3yN6hn6s3jitsoeSrmSZGblGJeXrKO5tBxFOzkP5ljg=',
#   'fileSize': '1800490'},
#  'image_fullscreen_001_portrait': {'t': 'img', 'w': '1080', 'h': '1920',
#   'u': 'https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE4TPBi?ver=feb1',
#   'sha256': '3HhZv36LIZCBYPs2soQkzC1NSGFoJM+/z77iqDLXAu8=',
#   'fileSize': '1657127'},
#  'hs2_title_text': {'t': 'txt', 'tx': 'Gray seals call Germany’s Helgoland Island home for the winter'},
#  'hs2_icon': {'t': 'txt', 'tx': '\ue774'},
#  'hs2_hover_text': {'t': 'txt', 'tx': 'Even though gray seals can be found all over the North Atlantic Ocean, this small island off the Northern coast of Germany is a popular location for them to birth pups in winter.'},
#  'hs2_cta_text': {'t': 'txt', 'tx': 'See more gray seals on Helgoland Island'},
#  'hs2_destination_url': {'t': 'url', 'u': 'Microsoft-edge:https://www.bing.com/search?q=gray+seals+Helgoland&form=M401ZL&OCID=M401ZL'},
#   ...
#  'title_text': {'t': 'txt', 'tx': 'Helgoland, Schleswig-Holstein, Germany'},
#  'copyright_text': {'t': 'txt', 'tx': '© Stefan Huwiler / ImageBROKER / Offset'},
#  'title_destination_url': {'t': 'url',  'u': 'Microsoft-edge:https://www.bing.com/search?q=gray+seal&form=M401PI&OCID=M401PI'
#   },
#  'image_fullscreen_002_landscape':
# ...
#}

def _wallpaper_details(locale: str='en-US'):
    
    _url = SPOTLIGHT_URL.format(locale=locale)

    r = requests.get(_url)
    j = r.json()

    items = [
        json.loads(i['item'])['ad']
        for i in j['batchrsp']['items']
        ]
    
    details = [
        {
            'image_url': i['image_fullscreen_001_landscape']['u'],
            'image_title': i['hs2_title_text']['tx'],
            'image_description': i['hs2_hover_text']['tx'] if 'hs2_hover_text' in i else '',
            'cta_text': i['hs2_cta_text']['tx'],
            'cta_url': i['hs2_destination_url']['u'].lower().replace('microsoft-edge:', ''),
            'item_title': i['title_text']['tx'],
            'item_copyright_text': i['copyright_text']['tx'],
            'item_url': i['title_destination_url']['u'].lower().replace('microsoft-edge:', '')
        }
        for i in items
    ]

    return details

def _build_caption(item: dict):
    caption = CAPTION_TEMPLATE.format(**item)
    return caption
    

# %%
def get_wallpaper_details():
    items = _wallpaper_details()

    for item in items:
        url = item.pop('image_url')
        caption = _build_caption(item)
        yield (url, caption)