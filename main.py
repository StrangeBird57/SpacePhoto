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


def download_image(path, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(url):
    response = requests.get(url)
    response.raise_for_status()
    image_links = response.json()["links"]["flickr_images"]
    for i in range(len(image_links)):
        download_image("Images/spacex{}.jpg".format(i + 1), image_links[i])


def fetch_nasa_apod(url, token):
    params = {
      "api_key": token,
      "count": 30
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    for i in range(len(response.json())):
        extension = get_extension(response.json()[i]["url"])
        download_image("Images/nasa_apod_{}{}".format(i + 1, extension),
                       response.json()[i]["url"])


def fetch_nasa_epic(url, token):
    url_template = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png"
    params = {
      "api_key": token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    for i in range(10):
        date = datetime.datetime.strptime(response.json()[i]["date"],
                                          "%Y-%m-%d %H:%M:%S")
        image_url = url_template.format(date.strftime("%Y"),
                                        date.strftime("%m"),
                                        date.strftime("%d"),
                                        response.json()[i]["image"])
        image_response = requests.get(image_url, params)
        download_image("Images/nasa_epic_{}.png".format(i + 1),
                       image_response.url)


def main():
    load_dotenv()
    Path("Images").mkdir(parents=True, exist_ok=True)
    nasa_token = os.getenv("NASA_TOKEN")
    spacex_url = "https://api.spacexdata.com/v3/launches/87"
    apod_url = "https://api.nasa.gov/planetary/apod"
    epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    fetch_spacex_last_launch(spacex_url)
    fetch_nasa_apod(apod_url, nasa_token)
    fetch_nasa_epic(epic_url, nasa_token)


if __name__ == '__main__':
    main()
