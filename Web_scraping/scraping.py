# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import re

# mars_news
# =========
# This function retrieves the latest Mars news from the mars.nasa.gov/news
# site and then returns the title and the teaser. In the case of an exception,
# nothing is returned.
#
# Arguments
# browser - And instance of chromedriver for sending requests and receiving
#           responses.
#
# Return:
# title and teaser in the case of normal completion. Nothin otherwise.
# Nothing in the case of an exception.

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
       
       return news_title, news_p
   
    except AttributeError:
        
        return None, None

# featured_image
# ==============
# This function retrieves the URL of the featured image from the 
# www.jpl.nava.gov website.
#
# Arguments:
# # browser - And instance of chromedriver for sending requests and receiving
#           responses.
#
# Return:
# The URL of the featured image. Nothing in the case of an exception.
# Nothing in the case of an exception.

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

# mars_facts
# ==========
# This function retrieves the table of facts from the space-facts.com/mars/
# site.
#
# Arguments
# None
#
# Return
# A table of Mars facts.
# Nothing in the case of an exception.

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

# mars_hemispheres
# ================
# This function retrieves the titles and URLs of the images of four 
# Mars hemispheres.
#
# Argument:
# browser - And instance of chromedriver for sending requests and receiving
#           responses.
#
# Return:
# A list of dictionaries. Each dictionary contains the title and URL of one
# of the Mars' hemispheres.
# Nothing in the case of an exception.

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
        
        # find the first div whose class is 'collapsible results'
        results = soup.findAll("div", {"class": "collapsible results"})[0]
        
        # get a list of the item divs. Each item div contains the title of
        # the hemisphere and a link to the full image of the hemisphere
        items = results.findAll("div", {"class": "item"})

        # Iterate through the item divs and retrieve the titkes into a 
        # titles list.
        titles = []
        for item in items:
            link = item.find("a")["href"]
            title = item.find("h3").get_text()
            titles.append(title)    
        
        # Iterate through the item divs and retrieve the URLs of the full
        # images of the hemispheres into a urls list.
        main_url = "https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-online-content/module_10/"
        urls = []
        for item in items:
            # find the div whose class is description
            divdesc = item.find("div",{"class":"description"})            
            # grab the href from the <a> element inside the div
            item_uri = divdesc.find("a")["href"]
            # get the item url by combining the main url with the item uri
            item_url = f"{main_url}{item_uri}"
            
            # Visit the url of the full image
            browser.visit(item_url)
            html = browser.html
        
            # Create a Beautifulsoup object from the full image page
            soup = BeautifulSoup(html, 'html.parser')
            
            # Grab all the list items in the page
            list_items = soup.findAll("li")
            
            # Search the items for an item that contains a link <a> whose
            # text content is "Sample". 
            for li in list_items:
                # find the link in the list item.
                link = li.find("a")
                # If the link contains the text "Sample"
                if link.text == "Sample":            
                    # append the link to the urls list
                    urls.append(link["href"])
                    break
        
        # Iterate through the titles and urls lists and, for each title-URL
        # pair, create a dict. Append the dict to the dicts list.
        dicts = []
        for n in range(len(titles)):
            dct = {"title":titles[n],"img_url":urls[n]}
            dicts.append(dct)
        
        
        # return the list of hemisphere dicts
        return dicts    
       
    except BaseException as be:
        print(be)
        return None


# add_class
# =========
# This function finds the tag whose name is tag and text content is text
# and appends the class_name to the class attribute of the tag
#
# Arguments:
# html : the html object to search
# tag : the tag for which to search
# text: the text content of the tag
# class_name: a text string containing a space-delimiter list of class names
# 
# Return:
# the new html 

def add_class(html,tag,class_name,text=""):
    # Instantiate a BeautifulSoup object
    beautifulSoup = BeautifulSoup(html,'lxml')
    
    # If the text argument is not blank
    if text != "":
        # find all the tag tags whose text content is text
        tags = beautifulSoup.find_all(tag,text=re.compile(text))
    # If the text argument is blank
    else:
        # find all the tag tags
        tags = beautifulSoup.find_all(tag)
    
    # Iterate through the tags list and append the new class_name to the
    # class attribute.
    for tag in tags:
        tag['class'].append(class_name)

    # Return the new html 
    return beautifulSoup.prettify( formatter="html" )


# remove_class
# ============
# This function finds the tag whose name is tag and text content is text
# and removes class_name from the class attribute of the tag
#
# Arguments:
# html : the html object to search
# tag : the tag for which to search
# text: the text content of the tag
# class_name: the name of the class to be removed
# 
# Return:
# the new html 

def remove_class(html,tag,class_name,text=""):
    # Instantiate a BeautifulSoup object
    beautifulSoup = BeautifulSoup(html,'lxml')
    
    # If the text argument is not blank
    if text != "":
        # find all the tag tags whose text content is text
        tags = beautifulSoup.find_all(tag,text=re.compile(text))
    # If the text argument is blank
    else:
        # find all the tag tags
        tags = beautifulSoup.find_all(tag)
    
    # Iterate through the tags list and remove class_name from the
    # class attribute.
    for tag in tags:
        tag['class'].remove(class_name)

    # Return the new html 
    return beautifulSoup.prettify( formatter="html" )


# add_attribute
# =============
# This function finds the tag whose name is tag and text content is text
# and removes class_name from the class attribute of the tag
#
# Arguments:
# html : the html object to search
# tag : the tag for which to search
# text: the text content of the tag
# attr_name: the name of the new attribute
# attr_value: the value of the new attribute
#
# Return:
# the new html 

def add_attribute(html,tag,attr_name,attr_value,text=""):
    # Instantiate a BeautifulSoup object
    beautifulSoup = BeautifulSoup(html,'lxml')
    
    # If the text argument is not blank
    if text != "":
        # find all the tag tags whose text content is text
        tags = beautifulSoup.find_all(tag,text=re.compile(text))
    # If the text argument is blank
    else:
        # find all the tag tags
        tags = beautifulSoup.find_all(tag)
    
    for tag in tags:
        tag[attr_name] = attr_value

    # Return the new html 
    return beautifulSoup.prettify( formatter="html" )


# remove_attribute
# ================
# This function removes attribute attr_name from the tag satisfying the search
# criteria
#
# Arguments:
# html : the html object to search
# tag : the tag for which to search
# text: the text content of the tag
# attr_name: the name of the attribute to remove
#
# Return
# the modified html object

def remove_attribute(html,tag,child_tags,attr_name,text=""):
    # Instantiate a BeautifulSoup object
    beautifulSoup = BeautifulSoup(html,'lxml')

    # find all the tag tags
    tags = beautifulSoup.find_all(tag)
    
    # Iterate through the tags 
    for tg in tags:
        # if the text argument is not blank
        if text != "":
            # find all the text contents of the child tags
            text_contents = [t.text for t in tg.find_all(child_tags)]
            # Iterate through text items
            for item in text_contents:
                # If there is a match
                if item.strip() == text:
                    # delete attribute attr_name from parent node
                    del(tg[attr_name])
        else:
            # if the text argument is blank
            del(tg[attr_name])

    # Return the new html 
    return beautifulSoup.prettify( formatter="html" )


# get_carousel  (BOOTSTRAP)
# ============
# The function creates the html segment that displays the images of the four
# Mars hemispheres in a carousel.
#
# Arguments:
# dicts: the list of dicts containing the Mars hemispheres' titles and image
#        URLs
#
# Return:
# the html segment for the hemisphere carousel.  

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

# scrape_all
# =========
# This function invokes all the other functions and uses their outputs to 
# create the data dictionary which is returned to the calling function.
#
# Arguments:
# None
#
# Return:
# A data dictionary containing all the scraped information pertaining to Mars.

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
   
    # Dict list: One dict per hemisphere
    hemisphere_dicts = mars_hemispheres(browser)
    
    # Get the Mars facts html segment
    facts = mars_facts() 
    
    # Add classes table-hover and table-responsive classes  (BOOTSTRAP)
    facts = add_class(facts,"table","table-hover table-responsive")
    
    # Remove style attribute from tr tag 
    facts = remove_attribute(facts,"tr",['th','td'],"style","Mars")
    
    # Center Mars table heading with bootstrap class (BOOTSTRAP)
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
    print(sa)
