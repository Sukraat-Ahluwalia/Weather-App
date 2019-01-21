# Weather-App
A weather app using Python and REST API's. Sends customized emails based on the following weather conditions - 

1) If weather is sunny or 5 degrees warmer than the average temperature at this time of the year -> "It's nice out! Enjoy a discount on us."

2) If temperature is 5 degrees cooler than the average temperature at this time of the year -> "Not so nice out? That's okay, enjoy a discount on us."

3) Otherwise send an email with the subject -> "Enjoy a discount on us." 

The app is operated using a webpage in /frontend with a simple form consisting of two fields -> An email and location. The 
web page uses Google Maps API to enable autocomplete for locations. When entering the form looks like this - 

![Web Page Image]
(https://imgur.com/a/AD5L8LH)
