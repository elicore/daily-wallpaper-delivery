import requests

# region Constants
BING_URL_BASE = 'https://www.bing.com'
BING_WP_URL = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx={index}&n=1&mkt={market}'
MARKETS = ["en-US", "zh-CN", "ja-JP", "en-AU", "en-GB", "de-DE", "en-NZ", "en-CA", "en-IN"]

RESOLUTIONS = ["1366x768.jpg", "1920x1080.jpg", "UHD.jpg"]

CAPTION_TEMPLATE = (
    '<b>{title}</b>'
    '<a href="{link}">{link_text}</a>'
    )
# endregion

def _wallpaper_details(market: str=MARKETS[0], index: int=0) ->  dict:
    r = requests.get(
        url=BING_WP_URL.format(market=market, index=index),
        headers={
            "Referer": BING_URL_BASE,
            "User-Agent": 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/8.0; .NET4.0C; .NET4.0E)'
        }
    )

    return r.json()

def _wallpaper_url(daily_url: str, resolution: str="1920x1080.jpg"):
    return f'{BING_URL_BASE}{daily_url}_{resolution}'

def _build_caption(image: dict):
    title = image['title']
    link_text = image['copyright']
    link = image['copyrightlink']

    return CAPTION_TEMPLATE.format(**locals())

def get_wallpaper_details():
    wp = _wallpaper_details()
    url_base = wp['images'][0]['urlbase']
    url = _wallpaper_url(url_base)

    caption = _build_caption(wp['images'][0])

    return (url, caption)
