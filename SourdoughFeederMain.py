import paho.mqtt.client as mqtt
import time
import motor_control_h as step
import system_mode_h as mode
from twilio.rest import Client as clnt
account_sid = 'YOUR_ACCOUNT_SID_HERE'
auth_token = 'YOUR_SECRET_AUTH_CODE_HERE'
text_client = clnt(account_sid, auth_token)


status = mode.SystemStatus()


if __name__ == "__main__":

    def messageFunction(client, userdata, message):
        topic = str(message.topic)
        message = str(message.payload.decode("utf-8"))
        print(topic + message)
        
        if (message == "manual"):
            print("Changing mode to manual")
            status.update("manual")
        elif (message == "auto"):
            print("Changing mode to automatic")
            status.update("auto")
        elif (message == "feed"):
            print("ready to feed")
            print()
            if (status.Mode == "auto"):
                print("start auto feeder")
                step.stepperLeft()
                step.stepperRight()
                sms = text_client.messages \
                          .create(
                              body= "Starter has been fed on automatic cycle",
                              from_ = '+61888888888', # Twilio mobile number goes here
                              to = '+61888888888' # Personal mobile number goes here
                              )
            elif (status.Mode == "manual"):
                sms = text_client.messages \
                          .create(
                              body= "Starter is ready to feed. Please use manual option to feed it now",
                              from_ = '+61888888888', # Twilio mobile number goes here
                              to = '+61888888888' # Personal mobile number goes here
                              )
   

    ourClient = mqtt.Client("control_stn")

    ourClient.connect("localhost", 1883)



    ourClient.subscribe("feeder")
    ourClient.on_message = messageFunction
    ourClient.loop_start()
    while(1):
        
        time.sleep(1)
