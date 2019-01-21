# Weather-App
A weather app using Python and REST API's. Sends customized emails based on the following weather conditions - 

1) If weather is sunny or 5 degrees warmer than the average temperature at this time of the year -> "It's nice out! Enjoy a discount on us."

2) If temperature is 5 degrees cooler than the average temperature at this time of the year -> "Not so nice out? That's okay, enjoy a discount on us."

3) Otherwise send an email with the subject -> "Enjoy a discount on us." 

The directory structure for the app ->

1) `/frontend` - Contains all frontend specific files and Python files to store information in MySQL.
2) `/backend` - Contains all backend specific files to fetch weather data, for email specific tasks and sending the emails.
3) `/config` - JSON configuration files to use with secrets manager.
4) `/utilites` - Python files for utilities like logging , using AWS Secrets Manager.
5) `/logging` - Log files for different sections of the app.

The app is operated using a webpage in /frontend with a simple form consisting of two fields -> An email and location. The 
web page uses Google Maps API to enable autocomplete for locations. When entering the form looks like this - 

![Web Page Image](https://i.imgur.com/ATrR4wy.png)

To avoid malicious attacks like SQL injections the form in the webpage uses HTML's `pattern` attribute using a regex 
`^.+@.+$` to ensure that only strings that confirm to email id formats pass through. 

The App uses the Flask web framework to recieve data from the webpage which it then stores in a MySQL database. 
The Schema of the database is very simple - 

`email_addr->varchar(255) PRIMARY KEY`
`location->varchar(255)`

The app has the following dependencies - 

1) AWS Secrets Manager - To avoid storing database credentials and email credentials (to use when sending emails through SMTP) in plain text format or in JSON files , AWS Secrets Manager has been used to store credentials. When required the secrets_manager.py file in /utilities is used to connect to and fetch credentials from secrets manager.

2) Weatherbit API (https://www.weatherbit.io/) - REST API to retrieve current and historical weather information.

To send emails the app is called using `python weather_app.py` from the `/backend` directory (Will be setting this as a cron job to automate it).


To-Do's - 

1) Add unit tests for all Python files.
2) Deploy on AWS LightSail on an NGINX instance, so that the app can be accessed and used by anybody. (Should be done soon)
3) Add CI/CD functionalities (Hopefully)
