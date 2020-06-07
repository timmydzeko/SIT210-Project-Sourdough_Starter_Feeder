#User Manual For Setting Up Twilio and MQTT For This System

It is assumed that the user has set up their Raspberry Pi 3B+ and claimed their Particle Argon. Both are connected to their wi-fi.

Setting up MQTT broker – Raspberry Pi

a)	The MQTT broker needs to be installed on the Raspberry Pi and initialised so it turns on upon reboot of the system. To do this, you need to download the mosquitto mqtt broker. Open a terminal window and type into the command line:

  sudo apt install mosquitto mosquito-clients

If this is the first time you have used the sudo call, you will be prompted to enter your password upon pressing enter. The “mosquitto-clients” line on the end will allow you to use your Raspberry Pi as a broker and a client at the same time. 

b)	To turn on the mosquitto broker, enter into the command line:
  
  sudo systemctl enable mosquitto

This should always now run the broker. If you want to check if the broker is running at any time, run the above code in your command line  but replacing enable with status, which will look like this:

  sudo systemctl status mosquitto

Setting up MQTT connection – Raspberry Pi

The following section will demonstrate how to publish an mqtt message and how to subscribe to an mqtt topic. In one program running on the Raspberry Pi will receive messages, the other will send messages to the first program.

a)	Test Program for MQTT subscribe

a.	Basic notation

i.	To subscribe to an MQTT topic from the command line, you need a couple of bits of information:

•	Broker Name/IP address

•	Topic

ii.	As the broker is set up on your Raspberry Pi, the broker name is simply the name given to your Raspberry Pi. If you haven’t set it, the default is raspberrypi. To check this, simply open a terminal window and type hostname into the command line. 

iii.	The topic has no default or specific value. You can set it as whatever you like. It will only receive published messages that use the same topic name.

iv.	Open a new terminal window, and type this into the command line:

  mosquitto_sub -h hostname -t “topic”

You can either replace hostname with your Raspberry Pi’s hostname, or as the broker is on the same Raspberry Pi device, you can use the term localhost. An example subscribe call would be:

  mosquitto_sub -h localhost -t “test/message”


b)	Test Program for MQTT publish

a.	Basic notation

i.	To publish a message to an MQTT broker from the command line, you need three bits of information:

•	Broker Name/IP address

•	Topic

•	Message

ii.	The broker name and topic sections are the same as above (see Section A, parts a. ii & a. iii)

iii.	The message section contains the data you are intending to send via the mqtt broker. 

iv.	Open a new terminal window, and type this into the command line:

  mosquitto_pub -h hostname -t “topic” -m “message”

The message can contain whatever you like, it can be used to just be printed to the terminal or it can be transformed to trigger specific methods once it is received, both of which happen subscribing client side.. The below call will send the message “hello world” to the subscribing client from Section A, part a. iv:

  mosquitto_sub -h localhost -t “test/message” -m “hello world”

If you run the subscribe call in a different window prior to this one, you should see the message “hello world” now printed in that window.

c)	Installing Paho MQTT library

a.	To easily integrate MQTT protocol into python scripts, we can utilise the paho-mqtt library. This library will allow us to create a client object, then easily integrate the details above that we implemented in the basic command line message call. The line to install this library is:

  sudo pip3 install paho-mqtt

Because we want to ensure it downloads for python 3, pip3 is used instead of the regular pip call. Now we can include this library in any script.

d)	Adding client credentials to SystemControl.py script

a.	Once the steps above have been followed, download the four python files from the Github link above. Open the SystemControl.py file. 

b.	Everything should be already set up for you to use, but if you have personalised values in any other file (e.g. topic names, message outputs), check these lines to ensure they are correct:

i.	Line 17 initialises an MQTT client object called ourClient, the client’s name is currently set to “gui”, that can be left as default or changed to whatever you want.

ii.	Line 20 in the script connects the client object to the broker. It is by default connected to “localhost” and port 1883, so you can leave that as is.

iii.	On lines 44 and 53, check that the topic is correct on all files (if you leave them all as default from my scripts, they should all be called “feeder”

e)	Adding client credentials to SourdoughFeederMain.py script

a.	This is already set up as above, make sure to check these lines to ensure they are included/correct:

i.	Line 49 for the MQTT client object initialisation

ii.	Line 51 connecting to the broker “localhost”

iii.	Line 55 subscribing to correct topic (default set to “feeder”)

iv.	Line 56 should state it will run messageFunction when the client receives a message

v.	Line 57 should start the client loop

Setting up MQTT  connection – Particle Argon

a)	Personalising file

a.	There is not a great deal that you need to do to setup the Argon script. First, go to the Github link above and copy the C++ particle Argon script. Open up the Particle Web IDE and paste the code in. Go to the code tab, name the file and save.

b.	On line 12, inside the brackets, place the MQTT broker hostname inside the quotation marks. If your Raspberry Pi’s hostname is raspberrypi already, this doesn’t need to be changed

i.	1883 is the default gateway. It should be left as is

ii.	callback will run the callback function (line 33) that handles the mqtt messages received when subscribe has been run. As the Argon is not subscribing, the function is blank, but still needs to appear as an argument on line 12

c.	Inside the setup function, connect to the broker by giving your Argon client a name. This appears on line 185 inside the quotation marks. It can be left as argonDev, or you can personalise it.

d.	On line 259, ensure the topic inside the quotation marks is the same as the one in the SourdoughFeederMain.py script. If you left it as default, it will be already set.

Twilio Integration – Creating account/buying number

a)	Signing up to Twilio

a.	Go to twilio.com/try-twilio to sign up for a free trial account. This account will give you a $15 dollar credit which we can use to purchase a phone number.

i.	Enter your first name, last name, email and choose a password

b.	Follow the prompts on screen (i.e. accessing confirmation email, confirming phone number)

c.	Now you should be at the dashboard for your Twilio account.

i.	You will see in the middle of your page an Account SID and a Secret Auth token. Take note of where these are as you will need them later.

b)	Generating a number

a.	From the dashboard, choose the tab the tab that contains an ellipses (…) inside a circle. Choose the Phone Numbers option

b.	Click on the Buy a Number option

i.	Set the country to Australia (or whichever is local for you) and make sure the SMS option is ticked. From here, you can choose any number. There will be a monthly rate next to each, try to choose the lowest value. Press buy

ii.	Confirm this number is the one wanted

iii.	Select “individual” under who will use this number

iv.	On the Comply with Regulatory Requirements, choose create regulatory bundle if none show in the search drop down bar

1.	You will be prompted to enter your full name, upload supporting documents (drivers license for address and passport for name verification will do) then submit for review. Once your bundle gets approved, go to step v.

v.	Select your regulatory bundle from the drop down, then do the same for address. Once filled, you should be able to press the “Buy +61……” button. Now you have a number to sms your phone with.

Twilio Integration – Particle Argon via Webhook

a)	The code inside the Particle Argon script has been set up already, all that is left to do is configure the webhook.

a.	Open the Particle Console 

i.	Either type “particle console” into a search engine, or if in the Web IDE, select the bar graph tab on the left hand side.

ii.	Select the “Integrations” tab, which looks like a network graph

iii.	Select the “New Integration” option

1.	It will ask what type of integration you want to create, choose webhook

iv.	Enter the following details:

1.	Event Name = twilio_sms

2.	URL = https://api.twilio.com/2010-04-01/Accounts/{{YOUR_ACCOUNT_SID_HERE}}/Messages

a.	Replace {{YOUR_ACCOUNT_SID_HERE}} with your Twilio Account SID (remove brackets). It will start with the letters AC

3.	Request Type = POST

4.	Request Format = Web Form

5.	Device = Any

v.	Select the Advanced Settings option

vi.	Find the FORM FIELDS section, setting it to Custom. Then enter the following details:

1.	To: {{enter your personal mobile here}}

a.	Do not include brackets here

b.	Ensure your phone number uses the area code (i.e. +61)	

2.	From: {{enter Twilio mobile number here}}

a.	As above

3.	Body: {{PARTICLE_EVENT_VALUE}}

a.	Keep brackets in this one. This will look for a message attached to the particle event, and will send it as the sms body.

vii.	Find the HTTP BASIC AUTH section and enter the following

1.	Username = {{YOUR_ACCOUNT_SID_HERE}}

a.	Without brackets

b.	Copy your Twilio account SID as above

2.	Password = {{TWILIO_SECRET_AUTH_TOKEN_HERE}}

a.	Without brackets

b.	Copy your Twilio secret auth token from the Twilio Dashboard

viii.	Select Save, and now your webhook should be set up and functioning. Test this by selecting the test button on the webhooks info page.

Twilio Integration – Raspberry Pi via Rest API

a)	Open a terminal window on the Raspberry Pi and download the python Twilio library by using the command

  pip install twilio

Both main scripts on the Raspberry Pi will include this library automatically in their header file.

b)	Open the SystemControl.py script and adjust the following:

a.	On line 6, enter your Twilio account SID inside the quotation marks, replacing YOUR_ACCOUNT_SID_HERE

b.	On line 7, enter your secret authentication token inside the quotation marks, replacing YOUR_SECRET_AUTH_TOKEN_HERE

c.	On line 64, you can adjust the message body to output whatever you would like.

d.	Line 65 needs to be changed to your new Twilio mobile number

e.	Line 66 needs to be changed to your personal mobile number

c)	Now open SourdoughFeederMain.py script and adjust the following:

a.	On line 6, enter your Twilio account SID inside the quotation marks, replacing YOUR_ACCOUNT_SID_HERE

b.	On line 7, enter your secret authentication token inside the quotation marks, replacing YOUR_SECRET_AUTH_TOKEN_HERE

c.	On lines 36 and 43 you can adjust the sms message body to return whatever you would like

d.	Lines 37 and 44 need to have the mobile number changed to your new Twilio number

e.	Lines 38 and 45 need to have the mobile number changed to your personal mobile number
