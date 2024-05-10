#adding a comment mostly just to see if a git commit works!

#importing libraries
import urllib
import re
import tkinter as tk
from tkinter import filedialog

#read the HTML source file
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

        base_url = ""
        new_html = ""

        if utm_unit == "adms":
            base_url = "admissions.indiana.edu"
        elif utm_unit == "fye":
            base_url = "fye.indiana.edu"
        elif utm_unit == "schol":
            base_url = "scholarships.indiana.edu"

        replace_links = re.findall(r'(https?://\S+)', str(working_html))

        utm_links = []

        for url in replace_links:
            if base_url in url:
                naked_url = url.strip("\"")
                print(naked_url + "?utm_campaign=" + utm_unit + "-2023-2024-" + utm_campaign + "&utm_source=" + utm_source + "&utm_medium=email")
                utm_links.append((naked_url + "?utm_campaign=" + utm_unit + "-2023-2024-" + utm_campaign + "&utm_source=" + utm_source + "&utm_medium=email"))

        print(utm_links)

    # Save the modified HTML to a new file
    save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if save_path:
        with open(save_path, 'w') as save_file:
            save_file.write(old_html_head + working_html + old_html_foot)

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