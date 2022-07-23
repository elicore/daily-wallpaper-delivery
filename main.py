import typer
import requests
import sys


BING_URL_BASE = 'https://www.bing.com'
BING_WP_URL = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx={index}&n=1&mkt={market}'
MARKETS = ["en-US", "zh-CN", "ja-JP", "en-AU", "en-GB", "de-DE", "en-NZ", "en-CA", "en-IN"]

RESOLUTIONS = ["1366x768.jpg", "1920x1080.jpg", "UHD.jpg"]

CAPTION_TEMPLATE = """<b>{title}</b>
<a href="{link}">{copyright}</a>
"""

def daily_wallpaper_details(market: str, index: int=0) ->  dict:
    r = requests.get(
        url=BING_WP_URL.format(market=market, index=index),
        headers={
            "Referer": BING_URL_BASE,
            "User-Agent": 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/8.0; .NET4.0C; .NET4.0E)'
        }
    )

    return r.json()

def build_wallpaper_url(daily_url: str, resolution: str="1920x1080.jpg"):
    return f'{BING_URL_BASE}{daily_url}_{resolution}'


def bot_send_photo(url: str, bot_token: str, chat_id: str, caption: str):
    message = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        json={'chat_id': chat_id, 'photo': url, 'caption': caption, 'parse_mode': 'html'})

    print(message.json())

def build_wallpaper_caption(image: dict):
    title = image['title']
    copyright = image['copyright']
    link = image['copyrightlink']

    return CAPTION_TEMPLATE.format(**locals())


def main(bot_token: str, chat_id: str):
    wp = daily_wallpaper_details(MARKETS[0]) # en-US
    url_base = wp['images'][0]['urlbase']
    url = build_wallpaper_url(url_base)
    caption = build_wallpaper_caption(wp['images'][0])

    bot_send_photo(url, bot_token, chat_id, caption)


if __name__ == '__main__':
    # typer.run(main)
    main(sys.argv[1], sys.argv[2])
