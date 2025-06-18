from bs4 import BeautifulSoup
from datetime import datetime
import re

# uses June 20 as an arbitrary cutoff date to determine the current academic year
def date_checker():

    current_month_day = datetime.today().strftime('%Y-%m')

    if current_month_day > '06-20':
        current_academic_year = datetime.today().strftime('%Y') + '-' + str(int(datetime.today().strftime('%Y')) + 1)
    else:
        current_academic_year = str(int(datetime.today().strftime('%Y')) + 1) + '-' + str(int(datetime.today().strftime('%Y')) + 2)

    return current_academic_year

# duplicates content of content_grabber, but is currently used outside of that function to filter the list of original links so that the lengths of the original list of links and the updated list of links matches. Will be implemented into content_grabber in the future.
def link_filter(links):

    storage_list =[]

    for link in links:
        #filter for IU links
        if 'indiana.edu' in link or 'iu.edu' in link or "{{Form-Link}}" in link or "{{Form-Survey-Link}}" in link:
            #filter out non-webpage and unnecessary IU links
            if "mailto:" not in link and ".png" not in link and "tel" not in link and ".jpg" not in link and 'https://one.iu.edu' not in link and "machform" not in link and "go.iu.edu" not in link:
                storage_list.append(link)

    return storage_list

# a function that takes some HTML and returns a list of all of the text that's inside a set of <a> tags, formatted for a UTM query string
def content_grabber(html):

    i = 0
    # create an object from the content of the HTML file
    soup = BeautifulSoup(html, 'html.parser')
    # initialize an empty list to store the link content values
    link_content_list = []

    for link in soup.findAll('a'):
        # filter out the links that don't need to be updated
        if 'indiana.edu' in link['href'] or 'iu.edu' in link['href'] or "{{Form-Link}}" in link['href'] or "{{Form-Survey-Link}}" in link['href']:
            if "mailto:" not in link['href'] and ".png" not in link['href'] and "tel:" not in link['href'] and ".jpg" not in link['href'] and 'https://one.iu.edu' not in link['href'] and "machform" not in link['href'] and "go.iu.edu" not in link['href']:
                # case if link is not a button
                # this code chops and screws the content and appends the anchor tag to the end of the content if it exists
                if len(link.contents) == 1:
                    if '#' in link['href']:
                        url = link['href'].split('#')[0]
                        anchor = '#' + link['href'].split('#')[1]
                        dirty_content = str(link.contents[0]).replace(" ", "-").lower().strip("\'")
                        # this regex removes non-alphanum characters from the content
                        char_regex = re.compile(r'\s*[^a-zA-Z0-9\-]\s*')
                        hypen_content = char_regex.sub('', dirty_content)
                        # cleanup step to remove double hyphens when an illegal character is removed
                        clean_content = hypen_content.replace('--', '-') + anchor
                        link_content_list.append(clean_content)
                    # does the same as the above for links with no anchor tags
                    else:
                        dirty_content = str(link.contents[0]).strip().replace(" ", "-").lower().strip().strip("\n").strip("\'")
                        char_regex = re.compile(r'\s*[^a-zA-Z0-9\-]\s*')
                        hypen_content = char_regex.sub('', dirty_content)
                        clean_content = hypen_content.replace('--', '-')
                        link_content_list.append(clean_content)
                # case if link IS a button
                # rinse and repeat
                else:
                    if '#' in link['href']:
                        url = link['href'].split('#')[0]
                        anchor = '#' + link['href'].split('#')[1]
                        dirty_content = str(link.contents[2]).replace(" ", "-").lower().strip("\'") + "-button"
                        char_regex = re.compile(r'\s*[^a-zA-Z0-9\-]\s*')
                        hypen_content = char_regex.sub('', dirty_content)
                        clean_content = hypen_content.replace('--', '-') + anchor
                        link_content_list.append(clean_content)
                    else:
                        dirty_content = str(link.contents[2]).strip().replace(" ", "-").lower().strip().strip("\n").strip("\'") + "-button"
                        char_regex = re.compile(r'\s*[^a-zA-Z0-9\-]\s*')
                        hypen_content = char_regex.sub('', dirty_content)
                        clean_content = hypen_content.replace('--', '-')
                        link_content_list.append(clean_content)
        else:
            pass

    return link_content_list

# function that takes a list of created UTM links and appends the content values to them to complete the process
def utm_content_appender(utm_link_list, content_list):

    i = 0

    for link in utm_link_list:
        utm_link_list[i] = utm_link_list[i] + ("&utm_content=" + content_list[i])
        i += 1

    return utm_link_list

# function that goes through the HTML file and replaces the original links with their UTM-laden counterparts
def HTML_link_replacer(html, original_link_list, new_link_list):

    i = 0

    for link in original_link_list:
        html = html.replace('href=\"' + original_link_list[i] + '\"', 'href=\"' + new_link_list[i] + '\"', 1)
        i += 1

    return html

# a hopefully soon-to-be-unneeded function that removes the random quotation mark that is coming along with the links out of the HTML file for some reason
def quote_stripper(links):

    i = 0
    
    for link in links:
        links[i] = link.strip("\"")
        i += 1

    return links

# a function used to grab the anchor tag content from original links so that it can be appended to the end of the new link
def anchor_ripper(links):

    final_anchor_links = []

    for link in links:
        if '#' in link:
            anchorless_url = link.split('#')[0] + '?' + link.split('?')[1]
            final_anchor_links.append(anchorless_url)
        else:
            final_anchor_links.append(link)

    return final_anchor_links
