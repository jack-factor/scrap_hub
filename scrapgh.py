from urllib.request import urlopen
from bs4 import BeautifulSoup
from PIL import Image
import os

USER_GH = 'jack-factor'
BASE_URL = 'https://github.com/'
IMAGE_PATH = 'resources/img/'

"""
Html to Object
"""


def get_obj_current_page(user):
    try:
        gh_html = urlopen(BASE_URL + user)
        bsObj = BeautifulSoup(gh_html.read(), 'html.parser')
        return bsObj
    except Exception:
        return None


def get_index_data(user=USER_GH):
    pageObj = get_obj_current_page(user)
    if pageObj is None:
        return None
    data = {}
    # data profile
    mainContent = pageObj.find('div', {'role': 'main'})
    name = mainContent.find('span', {'class': 'vcard-fullname'})
    username = mainContent.find('span', {'class': 'vcard-username'})
    html_bio = mainContent.find('div', {'class': 'user-profile-bio'})
    image = mainContent.find('img', {'class': 'avatar'})['src']
    image_name = __process_image(username.text, image)

    # description
    description = ''
    if html_bio is not None:
        description = html_bio.text
    # organization
    organization = pageObj.findAll('a', {'class': 'avatar-group-item'})
    org_data = []
    for item in organization:
        org_data.append({'href': item['href'],
                         'name': item['aria-label']})
    data['organization'] = org_data
    data['name'] = name.text
    data['image'] = image_name
    data['username'] = username.text
    data['description'] = description
    # repositories
    repositories = pageObj.findAll('li', {'class': 'pinned-repo-item'})
    repo_data = []
    for repository in repositories:
        rep_text = repository.find('a')
        rep_body = repository.find('span',
                                   {'class': 'pinned-repo-item-content'})
        # language
        text_language = ''
        if rep_body.find('span', {'class': 'repo-language-color'}) is not None:
            rep_body.find('span', {'class': 'repo-language-color'}).extract()
            [a.extract() for a in rep_body.findAll('a')]
            text_language = rep_body.find(
                'p', {'class': 'mb-0'}
            ).text.strip('\n ')

        repo_data.append({
            'title': rep_text.find('span').text,
            'description': rep_body.find(
                'p', {'class': 'pinned-repo-desc'}
            ).text,
            'url': rep_text['href'],
            'langauage': text_language})
    data['repositories'] = repo_data
    return data


"""
Process image and save
"""


def __process_image(image_name, image_url, image_path=IMAGE_PATH):
    # open url image (the image not show extension)
    uopen = urlopen(image_url)
    # set paths
    image_path_full = image_path + image_name
    # verify directory
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    # create a file image without extension
    f = open(image_path_full, 'wb')
    f.write(uopen.read())
    f.close()
    # use pillow to open image
    image_file = Image.open(image_path_full)
    # read format
    image_format = image_file.format.lower()
    # concat new name
    new_name = image_name + '.' + image_format
    # save image whit new name
    image_file.save(image_path + new_name)
    # remove old image
    os.unlink(image_path_full)
    # return new name
    return new_name
