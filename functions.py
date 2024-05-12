from bs4 import BeautifulSoup

def mail_tel_img_link_remover(links):

    storage_list =[]

    for link in links:
        if "mailto:" not in link and ".png" not in link and ".tel" not in link and ".jpg" not in link and 'https://one.iu.edu' not in link and "machform" not in link:
            storage_list.append(link)

    return storage_list

# a function that takes some HTML and returns a list of all of the text that's inside a set of <a> tags, formatted for a UTM query string
def content_grabber(html):

    i = 0

    soup = BeautifulSoup(html, 'html.parser')
    link_content_list = []

    for link in soup.findAll('a'):
        if "mailto:" not in link['href'] and ".png" not in link['href'] and "tel:" not in link['href'] and ".jpg" not in link['href'] and 'https://one.iu.edu' not in link['href'] and "machform" not in link['href']:
            if len(link.contents) == 1:
                link_content_list.append(str(link.contents[0]).replace(" ", "-").lower().strip("\'"))
            else:
                link_content_list.append(str(link.contents[2]).strip().replace(" ", "-").lower().strip().strip("\n").strip("\'") + "-button")
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