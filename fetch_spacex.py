import requests
import os


def _fetch_picture(image_name, url):
    directory = 'images/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = '{}{}'.format(directory, image_name)
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)


def fetch_spacex_last_launch():
    r = requests.get('https://api.spacexdata.com/v3/launches/latest')
    links = r.json()['links']['flickr_images']
    for image_number, link in enumerate(links):
        path = 'spacex{}.jpg'.format(image_number+1)
        _fetch_picture(path, link)

