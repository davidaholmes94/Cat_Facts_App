# Cat_Facts_App
 Texts your friends random cat facts every minute using Twilio API
 
 This code is meant to run on your local machine.
 The code uses a ngrok tunnel to receive messages and stop the application.
 Before Running the Application:
 1. Sign up for Twilio
 2. Update the information in the credentials-template.json file with your Twilio account information
 3. Rename the file to credentials.json

 To run the application you need to open up 2 command windows.
 
 1st command window:
	- run the program using python run.py
	
 2nd command window:
	- Run the following command
	- twilio phone-numbers:update "************" --sms-url="http://localhost:5000/sms"
	- Replace the *'s with your Twilio phone number

This starts the ngrok tunnel that takes in the SMS messages and allows the Flask application to
do some action upon receiving them.
