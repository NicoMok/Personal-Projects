# I got inspiration for this project from the "Automate the Boring Stuff With Python" book.
# However, I decided to write code to download all the comics from XKCD from scratch, based on the syntax that I learned from the IBM
# Data Science course.

# ============================================================================
#  WEB SCRAPING PROJECT: DOWNLOADING ALL XKCD COMICS
# ============================================================================
# Loads XKCD home page, saves comic image on that page, follows the Previous
# Comic link, repeats until it reaches the first comic.
#
# Code:
# Download pages with requests module.
# Find the URL of the comic image for a page using Beautiful Soup.
# Download and save commic image to hard drive with iter_content().
# Find URL of previous comic link & repeat.

import os
import requests
from bs4 import BeautifulSoup
import urllib.request

url = 'http://xkcd.com'
path = r'C:\Users\nicco\OneDrive\Desktop\Personal_Projects\xkcd'
os.makedirs(path, exist_ok=False)

# When you are at the last comic, the previous comic link will be http://xkcd.com/#
while not url.endswith('#'):
    # Download the page.
    print(url)
    response = requests.get(url)
    html_data = response.text
    soup = BeautifulSoup(html_data,"html.parser")
    
    # Find the url of the comic image
    # Comic image is always within the <div id="comic"> tag
    # src: the URL of an image within a website
    
    comic_body = soup.find('div',{'id': 'comic'})
    # find all tags <div id = "comic">, there's only 1
    
    url_image = comic_body.find('img').get('src') 
    # extract url_image
    # returns the value of src: "//... .png"
    # src: the URL of an image within a website

    # Download the image from the url_image
    # Without an "https:", it seems BeautifulSoup has issues reading the image...
    url_image = "https:"+url_image
    imageresponse = requests.get(url_image)

    # Each html link has the form: https://xkcd.com/.../image.png
    # Save 'image.png' into the variable 'image_name'
    image_name = url_image.split('/')[-1]

    with open(os.path.join(path,image_name),'wb') as f:
        f.write(imageresponse.content)
        # Create a file called 'C:\Users\nicco\...\image.png
        # Write the content of the image extracted from BeautifulSoup into this png file.

    # Get the url of the previous image.
    # The previous image's url corresponds to the tag <a rel="prev" ...>
    prevButton = soup.find('a', rel="prev")
    # prevButton = [<a rel="prev" href="/n/" accesskey="p">&lt; Prev</a>]

    tag_of_prevImg = prevButton.get('href')
    # returns the value of href which will be "/n/"
    # n = the id of the image.
    # The url of each page is as follows:
    # 1st page: http://xkcd.com
    # Subsequent pages: http://xkcd.com/n/
    # Final page: http://xkcd.com/#
    
    if url is not 'http://xkcd.com':
        img_id = url.split('/')[-2]
        # Obtain the 'n' value of the current page
      
        tag2 = tag_of_prevImg.replace('/','')
        # Obtain the 'n' value of the previous page by removing the '/' from '/n/'
      
        url = url.replace(img_id, tag2)
        # In the url, replace the current value of 'n' with the 'n' of the previous page.
        print(url)
    else: 
        url = url + tag_of_prevImg
        print(url)



    
    
    
    
    
