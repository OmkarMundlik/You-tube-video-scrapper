from bs4 import BeautifulSoup as bs
import requests
from flask import Flask, render_template, request

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    driver = webdriver.Chrome()
    driver.get('https://www.youtube.com/@PW-Foundation/videos')
    try: 
        scrap_info = driver.find_elements(By.XPATH, '//a[@class="yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media"]')

    except Exception as e:
        print(e)
    # getting video urls
    urls = []
    for i in scrap_info:
        if len(urls)==5:
            break
        url = i.get_attribute("href")
        urls.append(url)
        # print(url)

        
    # getting titles of videos
    titles = []
    for i in scrap_info:
        if len(titles)==5:
            break
        title = i.get_attribute("title")
        # print(title)
        titles.append(title)

    # getting thumbnaail urls: 
    try: 
        thumbnail_data = driver.find_elements(By.XPATH, '//yt-image//img[@class="yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded"]')
    except Exception as e:
        print("image url exception: ", e)
    thumbnails = []
    for i in thumbnail_data:
        if len(thumbnails)==5:
            break
        try:
            url_t = i.get_attribute('src')
            thumbnails.append(url_t)
        except Exception as e:
            print("thumbnail : ",e)
    
    while(len(thumbnails)!= 5):
        thumbnails.append("NULL")

    # getting views and time of postings of the video: 
    Views = []
    try:
        views_data = driver.find_elements(By.XPATH, '//span[@class="inline-metadata-item style-scope ytd-video-meta-block"]')   
    except Exception as e:
        print("view exceptino: ",e)

    duration = []
    j = 0
    for i in views_data:
        if len(Views)==5 and len(duration)==5:
            break
        try:
            if j%2==0:
                v = i.text
                print(v)
                Views.append(v)
            else:
                d = i.text
                print(d)
                duration.append(d)
            j+=1
        except Exception as e:
            print(e)

    driver.quit()
    data = {
        'Titles' : titles,
        'Video links' : urls,
        'Thumbnail links' : thumbnails,
        'Views' : Views,
        'Time of Posting' : duration
    }

    # df = pd.DataFrame(data)
    # df.to_csv("dataincsv.csv")

    return render_template('index.html', video_links=urls, thumbnail_links = thumbnails, views=Views, times=duration, titles=titles)


if __name__=='__main__' :
    app.run(debug=True)