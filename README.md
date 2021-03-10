# web-scraping-challenge
Week 12 Homework

This repository contains:

- the folder Mission_to_Mars:

	- mission_to_mars.ipynb 
	(See all the outputs line by line. Code in this file is transferred to scrape_mars.py as a function 'def scrape_info():' )

	- scrape_mars.py 
	(variable mars_data created which is a dictionary storing various variables developed in this function 'def scrape_info()' )

	- app.py
	(Flask app created which calls in the dictionary from scrape_mars.py and stores it into MongoDB. Mongo DB returns it as dictionary variable for use in index.html)

	- Templates (folder)
		- index.html
		(Values retrieved via dictionary variable from app.py)

	- Static (folder)
		- styles.css
		(Formatting and aesthetic design to support index.html)

	- Screenshots (folder)
	This folder contains 3 screenshots of the final produced local host page when running app.py.
		- localhost page - Top Screen
		- localhost page - Mid Screen
		- localhost page - Bottom Screen
	
