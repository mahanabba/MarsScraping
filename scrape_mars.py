import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests as req

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

def scrape():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    imagepath = soup2.find("img", class_="thumb")["src"]
    featured_image_url = f'https://jpl.nasa.gov{imagepath}'
    twit_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twit_url)
    twit_html = browser.html
    twit_soup = BeautifulSoup(twit_html, 'html.parser')
    tweet = twit_soup.find_all('div', class_='js-tweet-text-container')[0].text
    tweet = tweet.replace('\n','').split('pic.twitter')[0]
    mf_url = 'https://space-facts.com/mars/'
    mf_df = pd.read_html(mf_url)[0]
    mf_df.columns = ['Records:','Mars', 'Earth']
    mf_df.set_index('Records:',inplace=True)
    mf_html = mf_df.to_html()
    h_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(h_url)
    h_html = browser.html
    h_soup = BeautifulSoup(h_html, 'html.parser')
    h_paths = h_soup.find_all('div',class_='item')
    paths = []
    for path in h_paths:
        imagepath = path.a['href']
        paths.append(f'https://astrogeology.usgs.gov{imagepath}')
    img_urls = []

    for path in paths:

        browser.visit(path)
        path_html = browser.html
        path_soup = BeautifulSoup(path_html, 'html.parser')
    
        title = path_soup.find('h2',class_='title').text
    
        for a in path_soup.find_all('a'):
            if a.text == 'Sample':
                hemi_dict = {'title' :title,'img_url':a['href']}
                img_urls.append(hemi_dict)

    browser.quit()
    mars_dict = {
            'title': news_title,
            'text': news_p,
            'image': featured_image_url,
            'twitter' : tweet,
            'table' : mf_html,
            'hemisphere' : img_urls
        }

    return mars_dict
