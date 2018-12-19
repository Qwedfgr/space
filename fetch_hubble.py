import requests
import os


def fetch_picture(image_name, url):
    directory = 'images/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = '{}{}'.format(directory, image_name)
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)


def fetch_hubble_foto(id):
    url = 'http://hubblesite.org/api/v3/image/{}'.format(id)
    r = requests.get(url)
    links = r.json()['image_files']
    last_foto = links[-1]
    extension = get_file_extension(last_foto)
    path = 'hubble{}.{}'.format(id, extension)
    fetch_picture(path, last_foto['file_url'])


def fetch_hubble_collection():
    r = requests.get('http://hubblesite.org/api/v3/images/wallpaper')
    collection = r.json()
    for number, foto in enumerate(collection):
        fetch_hubble_foto(foto['id'])

def get_file_extension(foto):
    link = foto['file_url']
    return link.split('.')[-1]

if __name__ == '__main__':
    fetch_hubble_collection()






