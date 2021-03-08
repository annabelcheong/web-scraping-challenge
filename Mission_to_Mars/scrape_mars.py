# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

# Define function scrape_info (and store variables from info scraped from website)
def scrape_info():
    browser = init_browser()

    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    ##### Store VARIABLES in function #######
    
    ### News Title, News Paragraph ###
    #for html home page
    news_title = soup.find('div', class_='content_title').text
    #for html home page
    news_p = soup.find('div', class_='article_teaser_body').text

    ## Main Feature Image ##
    # Using splinter and retrieving content from url
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Attain full url for the image (via inspect on a chrome browser)
    # image_url: url_home + relative_image_path

    # url_home
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    # relative_image_path
    relative_image_path = soup.find('img',class_='headerimage')["src"]
    
    # featured_image_url
    #for html home page
    featured_image_url = url + relative_image_path 

    ## Pandas mars_data_table ##

    # URL
    url = 'https://space-facts.com/mars/'

    # Read url(html) with pandas
    tables = pd.read_html(url)

    df = tables[0]

    # Rename columns
    df.columns = ['', 'Mars']

    # Convert table to an html string
    html_table = df.to_html()
    
    # Clean up html and remove the \n
    #for html home page
    html_table = html_table.replace('\n', '')
    

    ## Four Hemisphere Images ##

    # # Using splinter and retrieving content from url
    # url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    # browser.visit(url)

    # time.sleep(1)

    # # Scrape page into Soup
    # html = browser.html
    # soup = bs(html, "html.parser")

    hemisphere_image_urls = [
    {"title1": "Valles Marineris Hemisphere", "img1_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"},
    {"title2": "Cerberus Hemisphere", "img2_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
    {"title3": "Schiaparelli Hemisphere", "img3_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
    {"title4": "Syrtis Major Hemisphere", "img4_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
    ]

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        # "html_table":  html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # print(mars_data)

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
   

