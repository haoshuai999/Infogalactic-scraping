# Infogalatic Scraper

Infogalactic is a right-wing website founded in 2016. The entire website was forked from wikipedia, but there are a lot of revisions to the entries. This repo can help you compare the differences between president profile page on wikipedia and infogalactic. The python script will output several HTML files named after the presidents. In the output files, the blue lines are from the content of wikipedia, and the red lines are from the content of infogalactic.

To do the comparison on PC:
1. Download the python file and chromedriver.exe
2. Check the version of the Chrome browser, make sure the version of matches the browser
3. In the Infogalatic.py file on line 30, user_agent = "Chrome/[version of browser]"
4. Run python Infogalatic.py on Terminal
