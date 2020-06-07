from tkinter import *
from tkinter import font
import paho.mqtt.client as mqtt
import motor_control_h as step
from twilio.rest import Client as clnt
account_sid = 'YOUR_ACCOUNT_SID_HERE'
auth_token = 'YOUR_SECRET_AUTH_TOKEN_HERE'
text_client = clnt(account_sid, auth_token)

# Initialising window as a tkinter instance
window = Tk()
window.title("Sourdough Starter Control Centre")
myFont = font.Font(family = 'Helvetica', size = 12, weight = "bold")
window.geometry("+300+150")

# Initialising MQTT client named GUI
ourClient = mqtt.Client("gui")

#Connecting to MQTT broker on Raspberry Pi
ourClient.connect("localhost", 1883)

# For troubleshooting. Demonstrates that a message has been sent, and
# can be configured to print the payload to the command line
def on_publish(client, userdata, message):
    print("data published \n")
    pass

# Sets the on_publish method to be executed when the client publishes a message
ourClient.on_publish = on_publish

# Initialises rad as a Tkinter Integer variable
rad = IntVar()
rad.set(1)

# Function that is defined by the radio button pressed
def changeMode():
    
    select = str(rad.get())
    if select == "1": # Manual mode button has been pressed
        
        # Changes the label below the radio buttons to show manual mode active
        statusFeeder.config(text="Current mode: Manual")
        # MQTT message sent to main program with payload message "manual"
        ourClient.publish("feeder", "manual")
        # Feed button enabled for manual mode
        btn.config(state=NORMAL)
        
    elif select == "2":
        
        # Changes the label below the radio buttons to show manual mode active
        statusFeeder.config(text="Current mode: Automatic")
        # MQTT message sent to main program with payload message "manual"
        ourClient.publish("feeder", "auto")
        # Feed button disabled in automatic mode
        btn.config(state=DISABLED)
    
# Function to run motors. Pulls from motor_control_h header file
def run():

    step.stepperLeft()
    step.stepperRight()
    sms = text_client.messages \
          .create(
              body= "Starter has been manually fed",
              from_ = '+61888888888', # Enter your Twilio mobile number here
              to = '+61888888888' # Enter your personal mobile number here
              )

# Setting of headers and buttons in terms of grid location and function
head1 = Label(window)
head1.grid(row=1, column=1)
head1.config(text="Manual feeding control")
btn = Button(window, text="Feed Starter", bg="black", fg="white", command=run, state=NORMAL)
btn.grid(column=1, row=2)
head2 = Label(window)
head2.grid(row=1, column=2)
head2.config(text="Mode control")
R1 = Radiobutton(window, text="Manual", variable=rad, value=1, command = changeMode)
R1.grid(row=2, column=2)
R2 = Radiobutton(window, text="Automatic", variable=rad, value=2, command = changeMode)
R2.grid(row=3, column=2)
statusFeeder = Label(window)
statusFeeder.grid(row=4, column=2)
statusFeeder.config(text="Current mode: Manual")

# On exit function to end process when window is shut
def close():
    window.destroy()


window.protocol("WM_DELETE_WINDOW", close)
window.mainloop()
