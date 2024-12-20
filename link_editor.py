# UTM Linker
# Licensed with the GNU General Public License version 3 I guess

#importing libraries
import re
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
from functions import *

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

        # builds a list out of all the links in the working HTML string and strips the extra quotation mark that's coming along with them for some reason
        # hopefully I'll be able to get rid of this function at some point
        working_replace_links = quote_stripper(re.findall(r'(https?://\S+)', str(working_html)))

        final_replace_links = link_filter(working_replace_links)

        working_utm_links = []

        # checks to see if there is an existing query string in the source URL. if so, the UTM parameters are added onto that existing query string rather than added as a new query string
        for url in final_replace_links:
            if "?" in url:
                working_utm_links.append((url + "&utm_campaign=" + utm_unit + "-2024-2025-" + utm_campaign + "&utm_source=" + utm_source + "&utm_medium=email"))
            else:
                working_utm_links.append((url + "?utm_campaign=" + utm_unit + "-2024-2025-" + utm_campaign + "&utm_source=" + utm_source + "&utm_medium=email"))

        # create the final list of links with UTMs attached that will be added into the current working HTML string
        final_utm_links = anchor_ripper(utm_content_appender(working_utm_links, content_grabber(working_html)))
        
        # looks through the working HTML string and replaces the links inside with their corresponding UTM links
        final_body_html = HTML_link_replacer(working_html, final_replace_links, final_utm_links)

    # Save the modified HTML to a new file
    save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if save_path:
        with open(save_path, 'w') as save_file:
            save_file.write(old_html_head + final_body_html + old_html_foot)
    
    working_utm_links = []
    working_replace_links = []
    final_replace_links = []
    final_utm_links = []

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