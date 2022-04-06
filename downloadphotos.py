import os
import datetime
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit, unquote


def get_extension(url):
    pathname = urlsplit(url).path
    filename = unquote(os.path.split(pathname)[1])
    extension = os.path.splitext(filename)[1]
    return extension


def download_image(path, url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    url = "https://api.spacexdata.com/v3/launches/87"
    response = requests.get(url)
    response.raise_for_status()
    image_links = response.json()["links"]["flickr_images"]
    for image_index, image_link in enumerate(image_links, start=1):
        download_image("Images/spacex{}.jpg".format(image_index), image_link)


def fetch_nasa_apod(token):
    url = "https://api.nasa.gov/planetary/apod"
    params = {
      "api_key": token,
      "count": 30
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    for image_index, image in enumerate(response.json(), start=1):
        extension = get_extension(image["url"])
        download_image("Images/nasa_apod_{}{}".format(image_index, extension),
                       image["url"])


def fetch_nasa_epic(token):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    url_template = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png"
    params = {
      "api_key": token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    for image_index in range(10):
        date = datetime.datetime.strptime(response.json()[image_index]["date"],
                                          "%Y-%m-%d %H:%M:%S")
        image_url = url_template.format(date.strftime("%Y"),
                                        date.strftime("%m"),
                                        date.strftime("%d"),
                                        response.json()[image_index]["image"])
        download_image("Images/nasa_epic_{}.png".format(image_index + 1),
                       image_url, params)


def main():
    load_dotenv()
    Path("Images").mkdir(parents=True, exist_ok=True)
    nasa_token = os.getenv("NASA_TOKEN")
    fetch_spacex_last_launch()
    fetch_nasa_apod(nasa_token)
    fetch_nasa_epic(nasa_token)


if __name__ == '__main__':
    main()
