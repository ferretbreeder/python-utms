#adding a comment mostly just to see if a git commit works!

#importing libraries
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup

#read the HTML source file
def process_html():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if not file_path:
        return

    # Get user-provided UTM parameters
    utm_unit= unit.get()
    utm_campaign = utm_campaign_entry.get()
    utm_source = utm_source_entry.get()
    utm_medium = utm_medium_entry.get()
    utm_content = utm_content_entry.get()

    with open(file_path, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Iterate through all anchor tags ('a') in the HTML
    for link in soup.findAll('a'):
        href = link.get('href')
        content = link.get(content)
        if href:
            # Append UTM parameters to the hyperlink
            query_string = f"utm_campaign={utm_unit + '-2023-2024-'}{utm_campaign}&utm_source={utm_source}&utm_medium={utm_medium}&utm_content={content}"
            new_href = f"{href}?{query_string}"
            link['href'] = new_href

    # Save the modified HTML to a new file
    save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if save_path:
        with open(save_path, 'w') as save_file:
            save_file.write(soup.prettify())

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

utm_medium_label = tk.Label(root, text="UTM Medium:")
utm_medium_label.pack()
utm_medium_entry = tk.Entry(root)
utm_medium_entry.pack()

utm_content_label = tk.Label(root, text="UTM Content:")
utm_content_label.pack()
utm_content_entry = tk.Entry(root)
utm_content_entry.pack()

# Create a button to select the HTML file
select_button = tk.Button(root, text="Select HTML File", command=process_html)
select_button.pack()

# Display a message to guide the user
message_label = tk.Label(root, text="Choose a file, enter UTM parameters, then click 'Select HTML File' to save the modified HTML.")
message_label.pack()

root.mainloop()