


from splinter import Browser
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import numpy as np
from iteration_utilities import unique_everseen





def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)





def mars_news():

    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    first_title = soup.find('div', class_='content_title').text
    first_paragraph = soup.find('div', class_='article_teaser_body').text
    browser.quit()

    return first_title, first_paragraph





def jpl_image():

    browser = init_browser()
    base_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(base_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    return featured_image_url





def mars_wheater():

    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup=BeautifulSoup(html,'html.parser')
    tweet=soup.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    return tweet





def mars_facts():

    tables =pd.read_html('https://space-facts.com/mars/')
    df=tables[0]
    df.columns=['Description','Value']
    df.set_index(df['Description'],inplace=True)
    del df['Description']

    return df.to_html()





def mars_hemis():
    list_of_url = ['cerberus_enhanced','schiaparelli_enhanced','syrtis_major_enhanced','valles_marineris_enhanced']
    url_final = [f'https://astrogeology.usgs.gov/search/map/Mars/Viking/{element}' for element in list_of_url]

    mars_hemisphere = []

    for idx,element in enumerate(url_final):
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=True)
        browser.visit(url_final[idx])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2',class_='title').text
        picture = soup.li.a['href']
        mars_hemisphere.append({'title':title,'img_url':picture})

    return mars_hemisphere


def scrape():

    data_dict = {}
    mars_news_split = mars_news()
    data_dict['mars_news'] = mars_news_split[0]
    data_dict['mars_paragraph'] = mars_news_split[1]
    data_dict['mars_image'] = jpl_image()
    data_dict["mars_weather"] = mars_wheater()
    data_dict["mars_facts"] = mars_facts()
    data_dict["mars_hemisphere"] = mars_hemis()

    return data_dict