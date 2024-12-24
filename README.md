# HTML Email Tracking UTM Creator

Licensed with the MIT License

## Does what it says on the can!

NOTE: This is used in a hyper-specific environment by me alone using the HTML formatting used by my team. Obviously I'd be thrilled if you forked it to use in your own work, but as is, it will likely not do much for you. Feel free to reach out to me with any questions you might have.

What follows includes some of the aforementioned hyperspecificity:

This program reads an HTML source file and adds UTM tracking query strings to all of the links that need one. The user selects a business unit, inputs a source and campaign name, and the program does the rest. The medium will always default to "email" for obvious reasons, and the year will need to be changed manually in the source code when transitioning to a new academic year.

The program also reads the text of every hyperlink and sets the utm_content parameter to that text, all lowercase and hyphen-separated. 

I chose Python simply because that is the language that I am most familiar with, and I've learned a lot over the last few months of working on this! In the future, there are a few features I'd like to implement:

- Functionality that allows it to be used on the "informal" emails meant to mimic emails sent from an individual sometimes sent by my team
- Handling for non-unicode characters (which currently throw an error and keep the program from continuing)
- Basic error handling/checking
- Proper tests

As the code might betray, I'm a fairly novice programmer whose biggest project is this very repo. But I welcome feedback/edits, and look forward to seeing how fully-featured I can make this little thing!

## How to run

I have only needed to run this program on Windows and Linux, and currently only a Windows binary is being provided in the releases section. But to run it yourself, the only non-standard library required is BeautifulSoup, which is present in the requirements.txt.

The binary is currently compiled manually using PyInstaller with pyinstaller --onefile (at least until I get my github action working again at which point that will run automatically), but of course you can just clone the repo, open link_editor.py in your editor, and run it from there as well.

## How to contribute

I know... so little about programming. I'm still figuring out Github, to be honest. As such, I don't have many guidelines for contributing. If you want to help, create a branch and do what you feel needs to be done. If it seems better than what I've got, then we'll get ourselves a stew goin'!

I don't have many opinions on style or etiquette, so just go hog wild.
