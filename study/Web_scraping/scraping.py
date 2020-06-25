# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


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

def add_class(html,tag,class_name):
    
    lines = html.split("\n")
    for i,line in enumerate(lines):
        if tag in line:
            lines[i] = append_class(line,class_name)
            print(lines[i])
            break
    
    new_lines = "\n".join(lines)
    
    return new_lines
    
def append_class(line,class_name):
    segments = line.split()

    for seg in segments:
        if "class=" in seg:
            keyVal = seg.split("=")
            key = keyVal[0]
            val = keyVal[1]
            classes = val.split("\"")
            classes[1] += " table-striped"
            keyVal[1] = "\"".join(classes)
            new_classes = "=".join(keyVal)
            
    for i,seg in enumerate(segments):
        if "class=" in seg:
            segments[i] = new_classes
            break
        
    new_line = " ".join(segments)
    
    return new_line

def mars_hemispheres(browser):
    try:
        
        # Visit the astrogeology site
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
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
            
        urls = []
        for item in items:
            item_uri = item.find("a")["href"]
            item_url = f"https://astrogeology.usgs.gov{item_uri}"
            
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
        return None
    
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
        htmlcode += '        <img src="' + dicts[0]["img_url"] + ' alt=' + dicts[0]["title"] + ' style="width:100%;">'
        htmlcode += '        <div class="carousel-caption">'
        htmlcode += '          <h3>' + dicts[0]["title"] + '</h3>'
        htmlcode += '        </div>'
        htmlcode += '      </div>'
        
        for n in range(1,len(dicts)):
            htmlcode += '      <div class="item">'
            htmlcode += '        <img src="' + dicts[n]["img_url"] + ' alt=' + dicts[n]["title"] + ' style="width:100%;">'
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
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
   
    # Dict list: One dict per hemisphere
    hemisphere_dicts = mars_hemispheres(browser)
   
    facts = mars_facts() 
    facts = add_class(facts,"table","table-striped")
    
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
