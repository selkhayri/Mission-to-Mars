# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import re

from lxml.html.soupparser import fromstring

def mars_news(browser):
    
    # Add try/except for error handling
    try:
       # Visit the mars nasa news site
       url = 'https://mars.nasa.gov/news/'
       browser.visit(url)
    
       # Optional delay for loading the page
       browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
       # Convert the browser html to a soup object and then quit the browser
       html = browser.html
       
       news_soup = BeautifulSoup(html, 'html.parser')
    
       slide_elem = news_soup.select_one('ul.item_list li.slide')
       slide_elem.find("div", class_='content_title')
    
       # Use the parent element to find the first <a> tag and save it as  `news_title`
       news_title = slide_elem.find("div", class_='content_title').get_text()
       news_title
    
       # Use the parent element to find the paragraph text
       news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
       
       print(news_p + "\n\n" +  news_title)
       return news_title, news_p
   
    except AttributeError:
        
        return None, None

def featured_image(browser):
    try:
    # ### Featured Images
    
        # Visit URL
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        
        # Find and click the full image button
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()
        
        # Find the more info button and click that
        browser.is_element_present_by_text('more info', wait_time=1)
        # more_info_elem = browser.find_link_by_partial_text('more info')    # browser.find_link_by_partial_text deprecated
        more_info_elem = browser.links.find_by_partial_text('more info')
        more_info_elem.click()
        
        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
    
        try:
            
            # Find the relative image url
            img_url_rel = img_soup.select_one('figure.lede a img').get("src")
            
            # Use the base URL to create an absolute URL
            img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
            
            return img_url
            
        except AttributeError:
            
            return None
        
    except BaseException:
        return None
        
def mars_facts():
    
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


def mars_hemispheres(browser):
    try:
        
        # Visit the astrogeology site
        #url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        url = 'https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-online-content/'\
            'module_10/Astropedia+Search+Results+_+USGS+Astrogeology+Science+Center.htm'
        browser.visit(url)
        
        # Set up the HTML parser
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.findAll("div", {"class": "collapsible results"})[0]
        items = results.findAll("div", {"class": "item"})

        titles = []
        for item in items:
            link = item.find("a")["href"]
            title = item.find("h3").get_text()
            titles.append(title)    
        
        main_url = "https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-online-content/module_10/"
        urls = []
        for item in items:
            divdesc = item.find("div",{"class":"description"})
            item_uri = divdesc.find("a")["href"]
            item_url = f"{main_url}{item_uri}"
            
            browser.visit(item_url)
            html = browser.html
        
            soup = BeautifulSoup(html, 'html.parser')
            list_items = soup.findAll("li")
            for li in list_items:
                link = li.find("a")
                if link.text == "Sample":            
                    urls.append(link["href"])
                    break
        
        dicts = []
        for n in range(len(titles)):
            dct = {"title":titles[n],"img_url":urls[n]}
            dicts.append(dct)
        
        
        return dicts    
       
    except BaseException as be:
        print(be)
        return None


def add_class(html,tag,class_name,text=""):
    
    beautifulSoup = BeautifulSoup(html,'lxml')
    if text != "":
        tags = beautifulSoup.find_all(tag,text=re.compile(text))
    else:
        tags = beautifulSoup.find_all(tag)
    
    for tag in tags:
        tag['class'].append(class_name)

    return beautifulSoup.prettify( formatter="html" )


def remove_class(html,tag,class_name,text=""):
    
    beautifulSoup = BeautifulSoup(html,'lxml')
    if text != "":
        tags = beautifulSoup.find_all(tag,text=re.compile(text))
    else:
        tags = beautifulSoup.find_all(tag)
    
    for tag in tags:
        tag['class'].remove(class_name)

    return beautifulSoup.prettify( formatter="html" )


def add_attribute(html,tag,attr_name,attr_value,text=""):
    beautifulSoup = BeautifulSoup(html,'lxml')
    if text != "":
        tags = beautifulSoup.find_all(tag,text=re.compile(text))
    else:
        tags = beautifulSoup.find_all(tag)
    
    for tag in tags:
        tag[attr_name] = attr_value

    return beautifulSoup.prettify( formatter="html" )


def remove_attribute(html,tag,attr_name,text=""):
    beautifulSoup = BeautifulSoup(html,'lxml')

    tags = beautifulSoup.find_all(tag)
    
    for t in tags:
        del(t[attr_name])

    return beautifulSoup.prettify( formatter="html" )


def get_carousel(dicts):
        
        htmlcode = ''
        htmlcode += '<div class="container">'
        htmlcode += '  <div id="myCarousel" class="carousel slide" data-ride="carousel">'
        htmlcode += '    <!-- Indicators -->'
        htmlcode += '    <ol class="carousel-indicators">'
        htmlcode += '      <li data-target="#myCarousel" data-slide-to="0" class="active"></li>'
        
        for n in range(1,len(dicts)):            
            htmlcode += '      <li data-target="#myCarousel" data-slide-to="{n}"></li>'
            
        htmlcode += '    </ol>'
        htmlcode += ''
        htmlcode += '    <!-- Wrapper for slides -->'
        htmlcode += '    <div class="carousel-inner">'
        htmlcode += ''
        htmlcode += '      <div class="item active">'
        htmlcode += '        <img src="' + dicts[0]["img_url"] + '" alt="' + dicts[0]["title"] + '" style="width:100%;">'
        htmlcode += '        <div class="carousel-caption">'
        htmlcode += '          <h3>' + dicts[0]["title"] + '</h3>'
        htmlcode += '        </div>'
        htmlcode += '      </div>'
        
        for n in range(1,len(dicts)):
            htmlcode += '      <div class="item">'
            htmlcode += '        <img src="' + dicts[n]["img_url"] + '" alt="' + dicts[n]["title"] + '" style="width:100%;">'
            htmlcode += '        <div class="carousel-caption">'
            htmlcode += '          <h3>' + dicts[0]["title"] + '</h3>'
            htmlcode += '        </div>'
            htmlcode += '      </div>'
            
        htmlcode += '  '
        htmlcode += '    </div>'
        htmlcode += ''
        htmlcode += '    <!-- Left and right controls -->'
        htmlcode += '    <a class="left carousel-control" href="#myCarousel" data-slide="prev">'
        htmlcode += '      <span class="glyphicon glyphicon-chevron-left"></span>'
        htmlcode += '      <span class="sr-only">Previous</span>'
        htmlcode += '    </a>'
        htmlcode += '    <a class="right carousel-control" href="#myCarousel" data-slide="next">'
        htmlcode += '      <span class="glyphicon glyphicon-chevron-right"></span>'
        htmlcode += '      <span class="sr-only">Next</span>'
        htmlcode += '    </a>'
        htmlcode += '  </div>'
        htmlcode += '</div>'
        
        return htmlcode


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=False)
    news_title, news_paragraph = mars_news(browser)
   
    # Dict list: One dict per hemisphere
    hemisphere_dicts = mars_hemispheres(browser)
    print(hemisphere_dicts)
    
    facts = mars_facts() 
    # Add bootstrap classes table-hover and table-responsive classes 
    # to dataframe table
    facts = add_class(facts,"table","table-hover table-responsive")
    
    # Remove style attribute from tr tag 
    facts = remove_attribute(facts,"tr","style","Mars")
    
    # Center Mars table heading with bootstrap class
    facts = add_attribute(facts,"th","class","text-center","Mars")
    
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": facts,
          "last_modified": dt.datetime.now(),
          "carousel": get_carousel(hemisphere_dicts)
    }
    
    
    return data


if __name__ == "__main__":
    # If running as script, print scraped data
    sa = scrape_all()
