#importing libraries
import re
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup

def mail_tel_img_link_remover(links):

    storage_list =[]

    for link in links:
        if "mailto:" not in link and ".png" not in link and ".tel" not in link and ".jpg" not in link and 'https://one.iu.edu' not in link and "machform" not in link:
            storage_list.append(link)

    return storage_list

# a function that takes some HTML and returns a list of all of the text that's inside a set of <a> tags, formatted for a UTM query string
def content_grabber(html):

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
        html = html.replace(original_link_list[i], new_link_list[i])
        i += 1

    return html

def quote_stripper(links):

    i = 0
    
    for link in links:
        links[i] = link.strip("\"")
        i += 1

    return links

# read the HTML source file
def process_html():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if not file_path:
        return

    # Get user-provided UTM parameters
    utm_unit= unit.get()
    utm_campaign = utm_campaign_entry.get()
    utm_source = utm_source_entry.get()

    with open(file_path, 'r') as file:

        # generate iterable content for the rest of the function
        old_html = file.read()

        # creates variables to hold the content that comes both before and after the content to be updated and stores that content in those variables
        old_html_head = old_html.split("<!-- Begin main content area -->")[0] + "<!-- Begin main content area -->"
        old_html_foot = "<!-- End: main content area -->" + old_html.split("<!-- Begin main content area -->")[1].split("<!-- End: main content area -->")[1]

        # creates the variable that will hold the lines of HTML that need to be searched/updated and stores that content here
        working_html = old_html.split("<!-- Begin main content area -->")[1].split("<!-- End: main content area -->")[0]

        working_replace_links = quote_stripper(re.findall(r'(https?://\S+)', str(working_html)))

        final_replace_links = mail_tel_img_link_remover(working_replace_links)

        working_utm_links = []

        for url in final_replace_links:
            working_utm_links.append((url + "?utm_campaign=" + utm_unit + "-2023-2024-" + utm_campaign + "&utm_source=" + utm_source + "&utm_medium=email"))
        
        final_utm_links = utm_content_appender(working_utm_links, content_grabber(working_html))

        final_body_html = HTML_link_replacer(working_html, final_replace_links, final_utm_links)

        print(final_replace_links)
        print(final_utm_links)

    # Save the modified HTML to a new file
    save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if save_path:
        with open(save_path, 'w') as save_file:
            save_file.write(old_html_head + final_body_html + old_html_foot)

# Create the main window
root = tk.Tk()
root.title("HTML Link Modifier with UTM Parameters")

# Create entry fields for UTM parameters
utm_unit_label = tk.Label(root, text="UTM Unit:")
utm_unit_label.pack()

# define list of business units
units = ["adms", "fye", "schol"]

# converts the picklist value to a string I guess?
# and sets the default unit on the picklist
unit = tk.StringVar(root)
unit.set("adms")

utm_campaign_unit = tk.OptionMenu(root, unit, *units)
utm_campaign_unit.pack()

# Create entry fields for UTM parameters
utm_campaign_label = tk.Label(root, text="UTM Campaign:")
utm_campaign_label.pack()
utm_campaign_entry = tk.Entry(root)
utm_campaign_entry.pack()


utm_source_label = tk.Label(root, text="UTM Source:")
utm_source_label.pack()
utm_source_entry = tk.Entry(root)
utm_source_entry.pack()

# Create a button to select the HTML file
select_button = tk.Button(root, text="Select HTML File", command=process_html)
select_button.pack()

# Display a message to guide the user
message_label = tk.Label(root, text="Choose a file, enter UTM parameters, then click 'Select HTML File' to save the modified HTML.")
message_label.pack()

root.mainloop()