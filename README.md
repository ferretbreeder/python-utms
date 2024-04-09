<h1>HTML Email UTM Linker</h1>

<h2>Does what it says on the can!</h2>

<p>
    This program reads an HTML source file and adds UTM tracking query strings to all of the links that need one. The user selects a business unit, inputs a source and campaign name, and the program does the rest. Content will always default to "email" for obvious reasons, and the year will need to be changed manually in the source code when transitioning to a new academic year.
</p>

<p>
    The program also reads the text of every hyperlink and sets the utm_content parameter to that text, all lowercase and hyphen-separated. 
</p>