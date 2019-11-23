import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from time import sleep
import requests

# make functions to call in the data from the jupyter notebook
# basically copy and paste from the notebook

def newest_article(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    latest_title = news_soup.find("div", class_="content_title").text
    first_teaser_paragraph = news_soup.find("div", class_="article_teaser_body").text
    return latest_title, first_teaser_paragraph

def featured_image(browser):
    jpg_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpg_url)
    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")
    jpg_html = browser.html
    jpg_soup = BeautifulSoup(jpg_html, 'html.parser')
    jpg_url = jpg_soup.find("img", class_="main_image")["src"]
    featured_image_url = f"https://www.jpl.nasa.gov{jpg_url}"
    return featured_image_url

def weather_tweet(browser):
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, "html.parser")
    recent_tweet = twitter_soup.find("p", class_="TweetTextSize").text
    return recent_tweet

def mars_facts(browser):
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[0]
    facts_df.columns = ['Column1','Column2']
    return facts_df.to_html()

def hemispheres():
    root_url = 'https://astrogeology.usgs.gov/'
    page = requests.get(root_url + "search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    hemisphere_soup = BeautifulSoup(page.text, "html.parser")
    divs = hemisphere_soup.findAll('div', attrs={"class": "item"})

    hemisphere_dict = {}

    for d in divs:
        name = d.find('h3').text
        link_bs = BeautifulSoup(requests.get(root_url + d.find('a').attrs['href']).text, 'html.parser')
        url = link_bs.find('div', attrs={'class': 'downloads'}).find('a').attrs['href']
        hemisphere_dict[name] = url


# Make dictionary to send to mongo
def run():
    # I was told it was poor form to call the browser before it was needed
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    a, b = newest_article(browser)
    mars_dict = {
        "headline_article": a,
        "headline_description": b,
        "main_image": featured_image(browser),
        "latest_weather_report": weather_tweet(browser),
        "mars_facts": mars_facts(browser),
        "hemispheres": hemispheres
    }
    return mars_dict