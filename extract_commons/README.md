This is an instruction to use the pywikibot for the extraction of information of 
from commons.wikimedia given a wikidata sourceId. 

1. Retrieve the Pywikibot from https://github.com/wikimedia/pywikibot and generate the user files (see https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation)
	somthing along the lines of "python3 generate_user_files.py" should happen
	1.1 Follow the instruction here https://www.mediawiki.org/wiki/Special:BotPasswords to create a Bot and password
	1.2 The language should be "commons" and the wiki should be "commons" as well
	1.3 An account on the commons-website needs to be created 
	1.4 An bot has to be created on the commons-website as well as a password for the bot
	1.5 Use the bot credentials in the command line prompt

2. You should now have a the files user-password.py and user-config.py in the same directory as pwb.py
3. Now the script extract_web_images.py can be run using 
	python3 extract_web_images.py
4. A new dir "extract_web_images/" will be created and in it the results should be presented in 4 different files 
	image_urls.tsv
	no_image_urls.tsv
	no_data_sourceId.tsv
	unknown_error_urls.tsv

