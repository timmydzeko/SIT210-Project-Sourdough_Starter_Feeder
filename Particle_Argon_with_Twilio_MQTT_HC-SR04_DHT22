// This #include statement was automatically added by the Particle IDE.
#include <Adafruit_DHT.h>
#include <MQTT.h>
#include <vector>

using namespace std;

#define DHTPIN D6
#define DHTTYPE DHT22

// Connect to MQTT broker, hosted on the Raspberry Pi
MQTT client("raspberrypi", 1883, callback);

DHT dht(DHTPIN, DHTTYPE);

// Assigning of variables for the Ultrasonic distance sensor calculations
unsigned long duration;
float speedOfSound = 0.0343; //speed of suond in centimetres per microsecond
float heightArray[15];
int size = sizeof(heightArray) / sizeof(heightArray[0]);
int median = 7; // index 7 of array is centre number (15 positions/2 =7.5, therefore middle number is 8 with 7 indices on either side)
int containerHeight = 33.5;
float maxHeight = 0;
String status = "null";

// Assigning of variables for the temperature sensor calculations
float temperature;
String lastTempRead;
String currentTempRead;
String tempData;
String body;

void callback(char* topic, byte* payload, unsigned int length){
    //used when a message is received. (not populated for this project) 
}


/*
---------------------------------------------------------
TEMPERATURE CALCULATION FUNCTIONS
---------------------------------------------------------
*/

// Returns the temperature recorded by DHT22 in Celcius
float readTemperature() {
    return dht.getTempCelcius();
}

// Returns the status of the temperature, whether it's higher, lower or within the desired range (24-28 degrees) 
String currentTempCalc(float temp){
    
    if (temp < 24)
    {
        return "low";
    }
    else if (temp > 28)
    {
        return "high";
    }
    else
    {
        return "good";
    }
}

// Publishes event to trigger an IFTTT text message if temp has crossed the threshold of being too high
void highTemp(String current, String last){
    if ((current == "high") && (last != "high"))
    {
        body = "The ambient temperature has risen above the desired range. Please move feeder into a cooler location";
        Particle.publish("twilio_sms", body, PRIVATE);
        Serial.println("High temp message sent");
    }
}

// Publishes event to trigger an IFTTT text message if temp has crossed the threshold of being too low
void lowTemp(String current, String last){
    if ((current == "low") && (last != "low"))
    {
        body = "The ambient temperature has dropped below the desired range. Please move feeder into a warmer location";
        Particle.publish("twilio_sms", body, PRIVATE);
        Serial.println("Low temp message sent");
    }
}

// Publishes event to trigger an IFTTT text message if temp has returned to the desired range
void goodTemp(String current, String last){
    if ((current == "good") && (last != "good"))
    {
        body = "The ambient temperature has returned to within the desired range.";
        Particle.publish("twilio_sms", body, PRIVATE);
        Serial.println("good temp message sent");
    }
}

/*
---------------------------------------------------------
DISTANCE CALCULATION FUNCTIONS
---------------------------------------------------------
*/


//  Reads the distance 15 times in a short amount of time to ensure we get a valid value
void readDistance(int size)
{
    for (int i=0;i<size;i++)
    {
        digitalWrite(D2, HIGH); // activate trigger
        delayMicroseconds(10);
        digitalWrite(D2, LOW);  // deactivates trigger
        duration = pulseIn(D4, HIGH);   // Records time taken to receive echo 
        delay(10);
        float distance = distanceInCentimetres(duration);
        float height = sourdoughHeight(distance);
        heightArray[i] = height;

    }
     
}


//  Converts the duration recording for the echo into a distance reading in cm
float distanceInCentimetres(unsigned long duration){
    return((duration/2)*speedOfSound);
}

//  Returns the difference between the height of the jar and the distance value
float sourdoughHeight(float dist)
{
    return(containerHeight-dist);
}

//  A basic bubble sort algorithm to put all values in the array in ascending order from index 0
void bubbleSort(float arr[], int size) {


    for (int step = 0; step < size - 1; step++)
    {
        for (int i = 0; i < size - step - 1; i++)
        {
            if (arr[i] > arr[i + 1])
            {
                float tmp = arr[i];
                arr[i] = arr[i + 1];
                arr[i + 1] = tmp;
            }
        }
    }
}

//  Finds the middle value of the array
float medianValue(float arr[], int median)
{
    return arr[median];
}

// Determines a new value for the status variable (whether it is time for feeding or not)
String readyToFeed(float median, float max, String status, int containerHeight)
{
    if ((median < 0) or (median > containerHeight))
    {
        status = "null";
        return status;
    }
    else
    {
        if (median < (0.9 * max))
        {
            status = "feed";
            return status;
        }
        else
        {
            return status;
        }   
    }
    
}


// Runs on initial startup of Particle Argon
void setup() {
    
    Serial.begin(9600); // For debugging purposes
    client.connect("argonDev"); // Connects to the server under the name "dev"
    dht.begin();    // initialises DHT22 sensor
    delay(2000);

    pinMode(D4, INPUT);   // echo pin to D4 on Argon
    pinMode(D2, OUTPUT);   // Trigger pin to D2 on Argon
    
    temperature = readTemperature();
    currentTempRead = "default";
    Serial.println(temperature);
    Serial.println();

    
    Serial.println("Setup complete");
    Serial.println();
}




void loop() {
    
    status = "null";
    lastTempRead = currentTempRead;
    Serial.println(status);
    Serial.println();
    delay(1000);
    
    temperature = readTemperature();
    currentTempRead = currentTempCalc(temperature);
    if (currentTempRead == "high")
    {
        highTemp(currentTempRead, lastTempRead);
    }    
    else if (currentTempRead == "low")
    {   
        lowTemp(currentTempRead, lastTempRead);
    }
    
    else if (currentTempRead == "good")
    {
        goodTemp(currentTempRead, lastTempRead);
    }
    else
    {
        Serial.println("Temperature reading error");
    }
    
    tempData = String(temperature);
    Serial.print("Temperature (C): ");
    Serial.println(temperature);
    Serial.println();
    
    readDistance(size); // Returns an array of 15 temperature readings
    bubbleSort(heightArray, size);  // Sorts array into ascending order
    float medianHeight = medianValue(heightArray, median);  // Finds the median height of the array (the value we will be using)
    if (medianHeight > maxHeight)
    {
        maxHeight = medianHeight;   // When the maximum height recorded for the feed cycle is surpassed, the variable is updated to the new maximum value
    }
    Serial.print("Median Height recording: ");
    Serial.println(medianHeight);
    Serial.println();
    Serial.print("Maximum height recorded for feed cycle: ");
    Serial.println(maxHeight);
    Serial.println();
    status = readyToFeed(medianHeight, maxHeight, status, containerHeight);  //  For evaluating if communication with the Raspberry Pi for feeding is required
    Serial.println(status);
    Serial.println();
    
    if (client.isConnected())
    {
        if (status == "feed")
        {
            client.publish("feeder", "Start feeder");
            delay(1000);
        }
        
        client.loop();
    }
    if (status == "feed")
    {
        maxHeight = 0;
    }
    delay(29000);
}
