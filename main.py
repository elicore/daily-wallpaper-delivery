import requests
import sys

from providers import bing, spotlight



def bot_send_photo(url: str, bot_token: str, chat_id: str, caption: str):
    message = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        json={'chat_id': chat_id, 'photo': url, 'caption': caption, 'parse_mode': 'html'})

    print(message.json())


def bot_send_document(url: str, bot_token: str, chat_id: str, caption: str):
    message = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendDocument',
        json={'chat_id': chat_id, 'document': url, 'caption': caption, 'parse_mode': 'html'})

    print(message.json())



def main(bot_token: str, chat_id: str):
    # send bing photo
    (url, caption) = bing.get_wallpaper_details()
    # bot_send_photo(url, bot_token, chat_id, caption)
    bot_send_document(url, bot_token, chat_id, caption)

    # send spotlight photo
    for url, caption in spotlight.get_wallpaper_details():
        # bot_send_photo(url, bot_token, chat_id, caption)
        bot_send_document(url, bot_token, chat_id, caption)



if __name__ == '__main__':
    # typer.run(main)
    main(sys.argv[1], sys.argv[2])
