import os
import time
import telegram
from random import choice
from dotenv import load_dotenv


def main():
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    time_step = int(os.getenv("TIME_STEP"))
    images = os.listdir('Images')
    bot = telegram.Bot(token=telegram_token)
    while True:
        random_image = choice(images)
        image_path = os.path.join('Images', random_image)
        with open(image_path, 'rb') as file:
            bot.send_photo(chat_id=chat_id, photo=file)
        time.sleep(time_step)


if __name__ == '__main__':
    main()
