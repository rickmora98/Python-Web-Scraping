# scrape_mars.py
# A demonstration of using BeautifulSoup, Splinter, & Pandas for web scraping.
# This script is needed for app.py to execute the scraping processes.
#
# written by: Ricardo G. Mora, Jr.
# last updated: 12/15/2021


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Main function to scrape the required info from the Mars websites
def scrape():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Status message to terminal
    print("Begin scraping.")

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find("div", class_="content_title").text.strip()

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find("div", class_="article_teaser_body").text.strip()

    # Status message to terminal
    print("1st website scraped.")
    print(f"   News Title: {news_title}")

    # Visit JPL space image URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    browser.links.find_by_partial_text("FULL IMAGE").click()

    # Parse the resulting html with soup
    html2 = browser.html
    image_soup = soup(html2, 'html.parser')
    image_elem = image_soup.find("img", class_="headerimage")

    # find the relative image url
    img_url_rel = image_elem["src"]

    # Use the base url to create an absolute url
    img_url = url + "/" + img_url_rel

    # Status message to terminal
    print("2nd website scraped.")
    print(f"   Image URL: {img_url}")

    # Visit mars facts URL
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    # Use Pandas to grab the first table
    df = pd.read_html(url, header=0)[0]

    # Use Pandas to set the first column as the index column
    df = df.rename(columns={"Mars - Earth Comparison": "Attributes"})
    df = df.set_index("Attributes")

    # Use Pandas to create an html string from the dataframe
    html_string = df.to_html()

    # Status message to terminal
    print("3rd website scraped.")
    print(f"   Table retrieved.")

    # Visit Mars Hemispheres URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        
        # We have to find the elements on each loop to avoid a stale element exception
        links = browser.find_by_css('a.product-item img')
        links[i].click()
        temp_soup = soup(browser.html, 'html.parser')
        
        # Next, we find the Sample image anchor tag and extract the href
        image_url = url + temp_soup.find("a", text="Sample")["href"]
        
        # Get Hemisphere title
        hemisphere_title = temp_soup.find("h2", class_="title").text.strip()
        
        # Append hemisphere object to list
        image_url_dict = {
            "title": hemisphere_title,
            "img_url": image_url
        }
        hemisphere_image_urls.append(image_url_dict)
        
        # Finally, we navigate backwards
        browser.back()

    # Close the browser
    browser.quit()

    # Status message to terminal
    print("4th website scraped.")
    print(f"   Last Image Title: {image_url_dict['title']}")

    # Load all scraped information into a dictionary
    mars_full_json = {
        "newsTitle": news_title,
        "newsParagraph": news_p,
        "featuredImageUrl": img_url,
        "factsTable": html_string,
        "hemispheres": hemisphere_image_urls,
        "lastUpdated": dt.datetime.now().ctime()
    }

    # Return the scraped data to the calling routine
    return mars_full_json

