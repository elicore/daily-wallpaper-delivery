import typer
import requests


# {
# 	"images": [{
# 		"startdate": "20220723",
# 		"fullstartdate": "202207230700",
# 		"enddate": "20220724",
# 		"url": "/th?id=OHR.FoxgloveHawkmoth_EN-US4340017481_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp",
# 		"urlbase": "/th?id=OHR.FoxgloveHawkmoth_EN-US4340017481",
# 		"copyright": "Elephant hawk-moth on foxglove flower (© David Chapman/Alamy)",
# 		"copyrightlink": "https://www.bing.com/search?q=elephant+hawk+moth&form=hpcapt&filters=HpDate%3a%2220220723_0700%22",
# 		"title": "Stealthy pollinator",
# 		"quiz": "/search?q=Bing+homepage+quiz&filters=WQOskey:%22HPQuiz_20220723_FoxgloveHawkmoth%22&FORM=HPQUIZ",
# 		"wp": true,
# 		"hsh": "3a20986812f56f8fd054551ba63b5e1b",
# 		"drk": 1,
# 		"top": 1,
# 		"bot": 1,
# 		"hs": []
# 	}],
# 	"tooltips": {
# 		"loading": "Loading...",
# 		"previous": "Previous image",
# 		"next": "Next image",
# 		"walle": "This image is not available to download as wallpaper.",
# 		"walls": "Download this image. Use of this image is restricted to wallpaper only."
# 	}
# }

BING_URL_BASE = 'https://www.bing.com'
BING_WP_URL = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx={index}&n=1&mkt={market}'
MARKETS = ["en-US", "zh-CN", "ja-JP", "en-AU", "en-GB", "de-DE", "en-NZ", "en-CA", "en-IN"]

RESOLUTIONS = ["1366x768.jpg", "1920x1080.jpg", "UHD.jpg"]

def daily_wallpaper_details(market: str, index: int=0) ->  dict:
    r = requests.get(
        url=BING_WP_URL.format(),
        headers={
            "Referer": BING_URL_BASE,
            "User-Agent": 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/8.0; .NET4.0C; .NET4.0E)'
        }
    )

    return r.json()

def build_wallpaper_url(daily_url: str, resolution: str="1920x1080.jpg"):
    return f'{BING_URL_BASE}{daily_url}_{resolution}'


def bot_send_photo(url: str, bot_token: str, chat_id: str):
    message = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        json={'chat_id': chat_id, 'photo': url})

    print(message.json())


def main(bot_token: str, chat_id: str):
    wp = daily_wallpaper_details(MARKETS[0]) # en-US
    url_base = wp['images'][0]['urlbase']
    url = build_wallpaper_url(url_base)
    print(url)


if __name__ == '__main__':
    typer.run(main)
