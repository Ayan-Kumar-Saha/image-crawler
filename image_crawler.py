
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import os

image_name = input('Enter the image subject you want to download: ')
image_count= int(input('Number of images you want to download: '))

print('Openning Firefox...', end='\n\n')
browser = webdriver.Firefox()
browser.minimize_window()

URL = "https://unsplash.com/"

print('Going to %s' % URL, end='\n\n')
browser.get(URL)
time.sleep(1)

print('Please wait...', end="\n\n")

search_bar = browser.find_element_by_id('SEARCH_FORM_INPUT_homepage-header-big')
search_bar.clear()
search_bar.click()
search_bar.send_keys(image_name)
search_bar.send_keys(Keys.RETURN)
time.sleep(2)

print('Searching images on %s...' % image_name, end="\n\n")

result_page = browser.find_element_by_tag_name("body")

print('Please wait...', end="\n\n")

no_of_pagedowns = 50

while no_of_pagedowns:
    result_page.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.4)
    no_of_pagedowns-=1
    
image_elements = browser.find_elements_by_css_selector('div ._2zEKz')


i = None
files_count = 0

if not os.path.exists('images'):
    os.mkdir('images')
    i = 1
else:
    files_count = len(os.listdir('images'))
    
i = files_count + 1

for image_element in image_elements:

    if i <= image_count + files_count:

        image_name = image_element.get_attribute('alt')

        if image_name == '':
            image_name = 'demo name'

        image_link = image_element.get_attribute('src')

        print('Downloading image %s...'% image_name)

        image_data = requests.get(image_link)

        try:
            image_data.raise_for_status()
        except Exception as e:
            print('There is a problem with this image: ' + e)

        image_file = open('images/'+str(i)+'-'+image_name+'.jpg', 'wb')

        for chunk in image_data.iter_content(100000):
            image_file.write(chunk)

        image_file.close()
        print('Download status: Ok!', end='\n\n')
        i += 1

    else:

        break

browser.quit()

print('Images successfully downloaded! Please check ./images folder!')

