import requests
import json

CHROMECAST_URL = 'https://clients3.google.com/cast/chromecast/home'

def _get_wallpaper_urls():
    r = requests.get(CHROMECAST_URL)
    t = r.text
    pos = t.index('JSON.parse(') + len("JSON.parse('")
    s = t[pos:t.index("')).")]
    page = s
    page = page.replace("\\x5b", "[")
    page = page.replace("\\x22", "\"")
    page = page.replace("\\/", "/")
    page = page.replace("\\n", "")
    page = page.replace("\\\\u003d", "=")
    page = page.replace("\\x5d", "]")

    j = json.loads(page)

    urls = [i[0] for i in j[0]]

    return urls