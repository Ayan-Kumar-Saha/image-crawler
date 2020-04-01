
import time
from selenium import webdriver
# Chrome users change the below line to 
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import os

URL = "https://unsplash.com/"

image_name = input('Enter the image subject you want to download: ')
image_count= int(input('Number of images you want to download: '))

options = Options()
options.headless = True

print('Openning Firefox...', end='\n\n')

# Chrome users change the below line to
# browser = webdriver.Chrome(options = options)
browser = webdriver.Firefox(options = options)

wait = WebDriverWait(browser, 20)

print('Going to %s' % URL, end='\n\n')

print('Please wait...', end="\n\n")

browser.get(URL)

try:
    search_bar = wait.until(EC.presence_of_element_located((By.ID, 'SEARCH_FORM_INPUT_homepage-header-big')))
    search_bar.clear()
    search_bar.click()
    search_bar.send_keys(image_name, Keys.RETURN)

except:
    print('Internet connection is too slow')
    browser.quit()
    exit()

time.sleep(2)

print('Searching images on %s...' % image_name, end="\n\n")

result_page = browser.find_element_by_tag_name("body")

no_of_pagedowns = 50

print('Please wait...', end="\n\n")

while no_of_pagedowns:
    result_page.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.4)
    no_of_pagedowns-=1
    
image_elements = browser.find_elements_by_css_selector('div ._2zEKz')

i = 0
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

