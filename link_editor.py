#adding a comment mostly just to see if a git commit works!

#importing libraries
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

        base_url = ""
        links = []

        if utm_unit == "adms":
            base_url = "admissions.indiana.edu"
        elif utm_unit == "fye":
            base_url = "fye.indiana.edu"
        elif utm_unit == "schol":
            base_url = "scholarships.indiana.edu"

        for line in file:
            if base_url in line:
                print(line.strip('\t, " "') + "\n")
                links.append(line)

    # Save the modified HTML to a new file
    save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if save_path:
        with open(save_path, 'w') as save_file:
            save_file.write(links[0] + '\n' + links[1] + '\n' + links[2])

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