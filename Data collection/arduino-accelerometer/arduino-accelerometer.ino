#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoOTA.h>  // upload novas versões sem ligação física
#include "HTTPClient.h"
#include "I2Cdev.h"
#include "MPU6050.h"

HTTPClient http;

WiFiServer server(80);

const char* KNOWN_SSID[] = {"Thomson2ED280", "DG-NGOH", "repeater", "MEO-D6547F"};
const char* KNOWN_PASSWORD[] = {"0E048F0A3D", "RaspberryPI", "", "FDD4D8D202"};
const int   KNOWN_SSID_COUNT = sizeof(KNOWN_SSID) / sizeof(KNOWN_SSID[0]); // number of known networks

const char* boardname = "acc001";
String data;
String header;
String log_message;
String servicename="/data/";
String servername="http://192.168.1.79:5000 ";
int httpResponseCode;
int timedelay = 10;

MPU6050 accelgyro;
I2Cdev   I2C_M;

uint8_t buffer_m[6];


int16_t ax, ay, az;
int16_t gx, gy, gz;
int16_t   mx, my, mz;



float heading;
float tiltheading;

float Axyz[3];
float Gxyz[3];
float Mxyz[3];


#define sample_num_mdate  5000

volatile float mx_sample[3];
volatile float my_sample[3];
volatile float mz_sample[3];

static float mx_centre = 0;
static float my_centre = 0;
static float mz_centre = 0;

volatile int mx_max = 0;
volatile int my_max = 0;
volatile int mz_max = 0;

volatile int mx_min = 0;
volatile int my_min = 0;
volatile int mz_min = 0;

void setup() {
  boolean wifiFound = false;
   int i, n;
   Serial.begin(9600);
   // ----------------------------------------------------------------
   // Set WiFi to station mode and disconnect from an AP if it was previously connected
   // ----------------------------------------------------------------
   WiFi.mode(WIFI_STA);
   WiFi.disconnect();
   delay(100);
   Serial.println("Setup done");
   // ----------------------------------------------------------------
   // WiFi.scanNetworks will return the number of networks found
   // ----------------------------------------------------------------
   Serial.println(F("scan start"));
   int nbVisibleNetworks = WiFi.scanNetworks();
   Serial.println(F("scan done"));
   if (nbVisibleNetworks == 0) {
     Serial.println(F("no networks found. Reset to try again"));
     while (true); // no need to go further, hang in there, will auto launch the Soft WDT reset
   }

   // ----------------------------------------------------------------
   // if you arrive here at least some networks are visible
   // ----------------------------------------------------------------
   Serial.print(nbVisibleNetworks);
   Serial.println(" network(s) found");

   // ----------------------------------------------------------------
   // check if we recognize one by comparing the visible networks
   // one by one with our list of known networks
   // ----------------------------------------------------------------
   for (i = 0; i < nbVisibleNetworks; ++i) {
      Serial.println(WiFi.SSID(i)); // Print current SSID
      Serial.print("Testing ");
      Serial.println(WiFi.SSID(i));
     for (n = 0; n < KNOWN_SSID_COUNT; n++) { // walk through the list of known SSID and check for a match

       if (strcmp(KNOWN_SSID[n], WiFi.SSID(i).c_str())) {
         Serial.print(F("\tNot matching "));
         Serial.println(KNOWN_SSID[n]);
       } else { // we got a match
         wifiFound = true;
         break; // n is the network index we found
       }
     } // end for each known wifi SSID
     if (wifiFound) break; // break from the "for each visible network" loop
   } // end for each visible network

   if (!wifiFound) {
     Serial.println(F("no Known network identified. Reset to try again"));
     log_message= "no Known network identified. Reset to try again";
     httplog();
     while (true); // no need to go further, hang in there, will auto launch the Soft WDT reset
   }

   // ----------------------------------------------------------------
   // if you arrive here you found 1 known SSID
   // ----------------------------------------------------------------
   Serial.print(F("\nConnecting to "));
   Serial.println(KNOWN_SSID[n]);

   // ----------------------------------------------------------------
   // We try to connect to the WiFi network we found
   // ----------------------------------------------------------------
   WiFi.begin(KNOWN_SSID[n], KNOWN_PASSWORD[n]);

   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
   }
   Serial.println("");

   // ----------------------------------------------------------------
   // SUCCESS, you are connected to the known WiFi network
   // ----------------------------------------------------------------
   Serial.println(F("WiFi connected, your IP address is "));
   Serial.println(WiFi.localIP());

   log_message = "WiFi connected, your IP address is: " + String(WiFi.localIP());
   httplog();


   // give the Ethernet shield a second to initialize:
   delay(1000);
   server.begin();
   // write something to server just to inform
   header = "{\"sensor\": \"" + String(boardname) +"\"}";//+", sensor:BME280, value1:\"24.25\",\"value2\":\"49.54\",\"value3\":\"1005.14\"}"
   
   //"fname="+String(boardname)+".sensor&fset="+String(boardname)+".set&var1=Hello_this_is_" + String(boardname) + "&+var2=" + String(0) + "&+var3=" + String(0) +
//"&+var4=" + String(0);
   //Serial.println(data);
   Serial.println("Post to server");
   httppost();
   //delay(10000);
   //softReset(); // RESET!

   // join I2C bus (I2Cdev library doesn't do this automatically)
    Wire.begin();

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    //Serial.begin(38400);
    
    // initialize device
    while(!Serial);
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
    
    log_message = accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed";
    httplog();
    
    delay(1000);
    Serial.println("     ");

    Mxyz_init_calibrated();
}

void loop() {

    getAccel_Data();
    getGyro_Data();
    getCompassDate_calibrated(); // compass data has been calibrated here
    getHeading();        //before we use this function we should run 'getCompassDate_calibrated()' frist, so that we can get calibrated data ,then we can get correct angle .
    getTiltHeading();

    data = "{\"sensor\" :" + String(boardname) 
    +", \"calibration_parameter\": {" +
     String(mx_centre) + ", " + String(my_centre) + ", " + String(mz_centre) +
    "}, \"acceleration\" : {" + 
    String(Axyz[0]) + ", " + String(Axyz[1]) + ", " + String(Axyz[2]) +
    "}, \"gyro\" : {"+ 
    String(Gxyz[0]) + ", " + String(Gxyz[1]) + ", " + String(Gxyz[2]) +
    "}, \"compass\" : {"+ 
    String(Mxyz[0]) + ", " + String(Mxyz[1]) + ", " + String(Mxyz[2]) +
    "}, \"heading\" : " + String(heading) + ", \"tiltheading\" : "+ String(tiltheading)
    
    +"}";

    Serial.println("calibration");
    Serial.println(" ");
    Serial.print(mx_centre);
    Serial.print("         ");
    Serial.print(my_centre);
    Serial.print("         ");
    Serial.println(mz_centre);
    Serial.println("     ");
    

    Serial.println("Acceleration(g) of X,Y,Z:");
    Serial.print(Axyz[0]);
    Serial.print(",");
    Serial.print(Axyz[1]);
    Serial.print(",");
    Serial.println(Axyz[2]);
    Serial.println("Gyro(degress/s) of X,Y,Z:");
    Serial.print(Gxyz[0]);
    Serial.print(",");
    Serial.print(Gxyz[1]);
    Serial.print(",");
    Serial.println(Gxyz[2]);
    Serial.println("Compass Value of X,Y,Z:");
    Serial.print(Mxyz[0]);
    Serial.print(",");
    Serial.print(Mxyz[1]);
    Serial.print(",");
    Serial.println(Mxyz[2]);
    Serial.println("The clockwise angle between the magnetic north and X-Axis:");
    Serial.print(heading);
    Serial.println(" ");
    Serial.println("The clockwise angle between the magnetic north and the projection of the positive X-Axis in the horizontal plane:");
    Serial.println(tiltheading);
    Serial.println("   ");
    Serial.println("   ");
    Serial.println("   ");
  
    httppost();

    delay(300);
  // put your main code here, to run repeatedly:

}

void httppost () {

   http.begin(servername+servicename);
   http.addHeader("Content-Type", "application/json");
   httpResponseCode = http.POST(data);
   String payload = http.getString();
   http.end();
   timedelay = payload.toInt();
   Serial.println(payload + httpResponseCode);
   //Serial.println(httpResponseCode);
   //Serial.println();
}

void httplog () {

   http.begin(servername+"/log/");
   http.addHeader("Content-Type", "application/text");
   httpResponseCode = http.POST(log_message);
   String payload = http.getString();
   http.end();
   timedelay = payload.toInt();
   Serial.println(payload + httpResponseCode);
   //Serial.println(httpResponseCode);
   //Serial.println();
}

void httpheader () {

   http.begin(servername+"/header/");
   http.addHeader("Content-Type", "application/json");
   httpResponseCode = http.POST(header);
   String payload = http.getString();
   http.end();
   timedelay = payload.toInt();
   Serial.println(payload + httpResponseCode);
   //Serial.println(httpResponseCode);
   //Serial.println();
}

void getHeading(void) {
    heading = 180 * atan2(Mxyz[1], Mxyz[0]) / PI;
    if (heading < 0) {
        heading += 360;
    }
}

void getTiltHeading(void) {
    float pitch = asin(-Axyz[0]);
    float roll = asin(Axyz[1] / cos(pitch));

    float xh = Mxyz[0] * cos(pitch) + Mxyz[2] * sin(pitch);
    float yh = Mxyz[0] * sin(roll) * sin(pitch) + Mxyz[1] * cos(roll) - Mxyz[2] * sin(roll) * cos(pitch);
    float zh = -Mxyz[0] * cos(roll) * sin(pitch) + Mxyz[1] * sin(roll) + Mxyz[2] * cos(roll) * cos(pitch);
    tiltheading = 180 * atan2(yh, xh) / PI;
    if (yh < 0) {
        tiltheading += 360;
    }
}



void Mxyz_init_calibrated() {

    Serial.println(F("Before using 9DOF,we need to calibrate the compass frist,It will takes about 2 minutes."));
    Serial.print("  ");
    Serial.println(F("During  calibratting ,you should rotate and turn the 9DOF all the time within 2 minutes."));
    Serial.print("  ");
    Serial.println(F("If you are ready ,please sent a command data 'ready' to start sample and calibrate."));
    while (!Serial.find("ready"));
    Serial.println("  ");
    Serial.println("ready");
    Serial.println("Sample starting......");
    Serial.println("waiting ......");

    get_calibration_Data();

    Serial.println("     ");
    Serial.println("compass calibration parameter ");
    Serial.print(mx_centre);
    Serial.print("     ");
    Serial.print(my_centre);
    Serial.print("     ");
    Serial.println(mz_centre);
    Serial.println("    ");
}


void get_calibration_Data() {
    for (int i = 0; i < sample_num_mdate; i++) {
        get_one_sample_date_mxyz();
        /*
            Serial.print(mx_sample[2]);
            Serial.print(" ");
            Serial.print(my_sample[2]);                            //you can see the sample data here .
            Serial.print(" ");
            Serial.println(mz_sample[2]);
        */



        if (mx_sample[2] >= mx_sample[1]) {
            mx_sample[1] = mx_sample[2];
        }
        if (my_sample[2] >= my_sample[1]) {
            my_sample[1] = my_sample[2];    //find max value
        }
        if (mz_sample[2] >= mz_sample[1]) {
            mz_sample[1] = mz_sample[2];
        }

        if (mx_sample[2] <= mx_sample[0]) {
            mx_sample[0] = mx_sample[2];
        }
        if (my_sample[2] <= my_sample[0]) {
            my_sample[0] = my_sample[2];    //find min value
        }
        if (mz_sample[2] <= mz_sample[0]) {
            mz_sample[0] = mz_sample[2];
        }

    }

    mx_max = mx_sample[1];
    my_max = my_sample[1];
    mz_max = mz_sample[1];

    mx_min = mx_sample[0];
    my_min = my_sample[0];
    mz_min = mz_sample[0];



    mx_centre = (mx_max + mx_min) / 2;
    my_centre = (my_max + my_min) / 2;
    mz_centre = (mz_max + mz_min) / 2;

}






void get_one_sample_date_mxyz() {
    getCompass_Data();
    mx_sample[2] = Mxyz[0];
    my_sample[2] = Mxyz[1];
    mz_sample[2] = Mxyz[2];
}


void getAccel_Data(void) {
    accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);
    Axyz[0] = (double) ax / 16384;
    Axyz[1] = (double) ay / 16384;
    Axyz[2] = (double) az / 16384;
}

void getGyro_Data(void) {
    accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);
    Gxyz[0] = (double) gx * 250 / 32768;
    Gxyz[1] = (double) gy * 250 / 32768;
    Gxyz[2] = (double) gz * 250 / 32768;
}

void getCompass_Data(void) {
    I2C_M.writeByte(MPU9150_RA_MAG_ADDRESS, 0x0A, 0x01); //enable the magnetometer
    delay(10);
    I2C_M.readBytes(MPU9150_RA_MAG_ADDRESS, MPU9150_RA_MAG_XOUT_L, 6, buffer_m);

    mx = ((int16_t)(buffer_m[1]) << 8) | buffer_m[0] ;
    my = ((int16_t)(buffer_m[3]) << 8) | buffer_m[2] ;
    mz = ((int16_t)(buffer_m[5]) << 8) | buffer_m[4] ;

    Mxyz[0] = (double) mx * 1200 / 4096;
    Mxyz[1] = (double) my * 1200 / 4096;
    Mxyz[2] = (double) mz * 1200 / 4096;
}

void getCompassDate_calibrated() {
    getCompass_Data();
    Mxyz[0] = Mxyz[0] - mx_centre;
    Mxyz[1] = Mxyz[1] - my_centre;
    Mxyz[2] = Mxyz[2] - mz_centre;
}
