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

    #############################
    # News Title, News Paragraph
    #############################
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')
    
    ### News Title, News Paragraph ###
    #for html home page
    news_title = soup.find('div', class_='content_title').text
    #for html home page
    news_p = soup.find('div', class_='article_teaser_body').text

    #############################
    # Main Feature Image 
    #############################
    
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
    featured_image_url = url + relative_image_path 

   
     #############################
    # Pandas mars_data_table 
    #############################

    # URL
    url = 'https://space-facts.com/mars/'

    # Read url(html) with pandas
    tables = pd.read_html(url)

    # Assign first table to df variable
    df = tables[0]

    # Rename columns
    df.columns = ['', 'Mars']

    # Set index to variable column
    df.set_index('', inplace=True)

    # Convert table to an html string
    html_table = df.to_html(justify='left')

    # Text-align the headingtext to the left
    html_table = html_table.replace('<th>','<th style="text-align: left;">')

    # Clean up html and remove the \n
    # for html home page
    html_table = html_table.replace('\n', '')
    

    #############################
    # HEMISPHERE IMAGES (BY URL)
    #############################
    # Objective: to attain the title of the image and 
    # put these 4 titles into a title_list[]

    # Using splinter and retrieving content from url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Store title into title_list once retrieved from the soup
    title_list = []

    results = soup.find_all('div', class_='item')

    for result in results:
        title = result.find('h3').text
        title_list.append(title)

    #############################

    ## Overall Objective: To attain 4 image url links (jpg - higher resolution files)

    # Get the specific mar's hemisphere url are located (1 url page per mars' hemisphere, 4 total)
    base_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(base_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all('div', class_='description')

    rel_url_list = []

    for result in results:
        rel_url  = result.find('a').attrs.get("href")
        
        rel_url_list.append(rel_url)

    #############################
    # List out the 4 img_urls and store them in the img_url_page_list
    img_url_page_list = []
    img_url_list = []
    for rel_url in rel_url_list:
        
        img_page_url = "https://astrogeology.usgs.gov" + rel_url
        img_url_page_list.append(img_page_url)
        print(img_page_url)

        # In the for loop on each img_page_url, use beautiful soup to extract out the 
        # specific img_url into the img_url_list
    
        browser.visit(img_page_url)
        time.sleep(1)

        # Scrape page into Soup and find the img_url
        html = browser.html
        soup = bs(html, "html.parser")

        results = soup.find_all('div', class_='downloads')

        for result in results:
            img_url  = result.find('a').attrs.get("href")

        img_url_list.append(img_url)

    #############################
    # Define variables in the hemisphere_image_urls list of dictionaries
    hemisphere_image_urls = [ 
    {'title':title_list[0], 'img_url': img_url_list[0] }, 
    {'title':title_list[1], 'img_url': img_url_list[1] },
    {'title':title_list[2], 'img_url': img_url_list[2] },
    {'title':title_list[3], 'img_url': img_url_list[3] }
    ]

    #############################
    # FINAL SECTION
    #############################
    # STORE VARIABLES INTO DICTIONARY
    #############################

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "html_table":  html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    ##################################

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data