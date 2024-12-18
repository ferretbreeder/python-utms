from bs4 import BeautifulSoup
import re

def link_filter(links):

    storage_list =[]

    for link in links:
        #filter for IU links
        if 'indiana.edu' in link or 'iu.edu' in link:
            #filter out non-webpage and unnecessary IU links
            if "mailto:" not in link and ".png" not in link and "tel" not in link and ".jpg" not in link and 'https://one.iu.edu' not in link and "machform" not in link:
                storage_list.append(link)

    return storage_list

# a function that takes some HTML and returns a list of all of the text that's inside a set of <a> tags, formatted for a UTM query string
def content_grabber(html):

    i = 0

    soup = BeautifulSoup(html, 'html.parser')
    link_content_list = []

    for link in soup.findAll('a'):
        if 'indiana.edu' in link['href'] or 'iu.edu' in link['href']:
            if "mailto:" not in link['href'] and ".png" not in link['href'] and "tel:" not in link['href'] and ".jpg" not in link['href'] and 'https://one.iu.edu' not in link['href'] and "machform" not in link['href']:
                if len(link.contents) == 1:
                    dirty_content = str(link.contents[0]).replace(" ", "-").lower().strip("\'")
                    char_regex = re.compile(r'\s*[^a-zA-Z0-9\-]\s*')
                    hypen_content = char_regex.sub('', dirty_content)
                    clean_content = hypen_content.replace('--', '-')
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

def utm_content_appender(utm_link_list, content_list):

    i = 0

    for link in utm_link_list:
        utm_link_list[i] = utm_link_list[i] + ("&utm_content=" + content_list[i])
        i += 1

    return utm_link_list

def HTML_link_replacer(html, original_link_list, new_link_list):

    i = 0

    for link in original_link_list:
        html = html.replace('href=\"' + original_link_list[i] + '\"', 'href=\"' + new_link_list[i] + '\"', 1)
        i += 1

    return html

def quote_stripper(links):

    i = 0
    
    for link in links:
        links[i] = link.strip("\"")
        i += 1

    return links