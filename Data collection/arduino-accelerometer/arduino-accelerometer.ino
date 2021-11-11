//Wifi & NTP
#include <WiFi.h>
#include <WebServer.h>
//#include <NTPClient.h>
#include <WiFiUdp.h>
#include <ESPNtpClient.h>
#include "HTTPClient.h"

//Accelerometer
#include "MPU9250.h"

//SD card
#include "SD.h"
#include "FS.h"
#include <SPI.h>

MPU9250 mpu;

HTTPClient http;

WiFiServer server(80);

const char* KNOWN_SSID[] = {"Thomson2ED280", "DG-NGOH", "repeater", "MEO-D6547F", "TP-LINK_FD02"};
const char* KNOWN_PASSWORD[] = {"0E048F0A3D", "RaspberryPI", "", "FDD4D8D202", "39116109"};
const int   KNOWN_SSID_COUNT = sizeof(KNOWN_SSID) / sizeof(KNOWN_SSID[0]); // number of known networks

const int MPU_addr = 0x68;

const String boardname = "acc001";
const String dataFileName = "/data-"+ boardname +".csv";
const String configFileName = "/config-" + boardname + ".txt";
String data;
String header;
String log_message;
String servicename="/data/";
String servername="http://192.168.0.105:5000 ";
int httpResponseCode;
int timedelay = 10;

#define SD_CS 2

// Define NTP Client to get time
//WiFiUDP ntpUDP;
//NTPClient timeClient(ntpUDP);
const PROGMEM char* ntpServer = "pool.ntp.org";

// Variables to save date and time
String formattedDate;
String dayStamp;
String timeStamp;

boolean isStart;

String dataMessage;

boolean isConfigured;
#define CONFIGURATION_PERIOD 100000

void setup() {
    boolean wifiFound = false;
    isConfigured = false;

    int i, n;
    Serial.begin(115200);

    // ----------------------------------------------------------------
    // Set WiFi to station mode and disconnect from an AP if it was previously connected
    // ----------------------------------------------------------------
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(100);
    Serial.println("Setup done");
    pinMode(33,OUTPUT);
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
      httplog ("no Known network identified. Reset to try again");
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

    IPAddress ip = WiFi.localIP();
    String ipAddressString = String(ip[0]) + String(".") + String(ip[1]) + String(".") + String(ip[2]) + String(".") + String(ip[3])  ;
    Serial.println(ipAddressString);
    digitalWrite(33,LOW);

    httplog ("WiFi connected, your IP address is: " + ipAddressString);

    // Initialize a NTPClient to get time
    NTP.setInterval (300);
    NTP.begin (ntpServer);
    //timeClient.begin();
    // Set offset time in seconds to adjust for your timezone, for example:
    // GMT +1 = 3600
    // GMT +8 = 28800
    // GMT -1 = -3600
    // GMT 0 = 0
    //timeClient.setTimeOffset(3600);

    // Initialize SD card
    SD.begin(SD_CS);  
    if(!SD.begin(SD_CS)) {
      httplog ("Card Mount Failed");
      Serial.println("Card Mount Failed");
      return;
    }
    uint8_t cardType = SD.cardType();
    if(cardType == CARD_NONE) {
      httplog ("No SD card attached");
      Serial.println("No SD card attached");
      return;
    }
    Serial.println("Initializing SD card...");
    if (!SD.begin(SD_CS)) {
      httplog ("ERROR - SD card initialization failed!");
      Serial.println("ERROR - SD card initialization failed!");
      return;    // init failed
    }

    // If the data.csv file doesn't exist
    // Create a file on the SD card and write the data labels
    File file = SD.open(dataFileName);
    if(!file) {
      Serial.println("File doens't exist");
      Serial.println("Creating file...");
      
    }
    else {
      httplog ("Data file already exists");
      Serial.println("Data file already exists");  
    }
    file.close();
   
    Wire.begin();
    delay(2000);

    if (!mpu.setup(MPU_addr)) {  // change to your own address
      while (1) {
        httplog ("MPU connection failed. Please check your connection with `connection_check` example.");
        Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
        delay(5000);
      }
    }

    readConfigureFile();

    if(!isConfigured){
      configure();
    }
    isStart = true;
    
}

void loop() {
    if (isStart == true){
      String firstLine = "Initial Date: ,"+ String(NTP.getTimeDateStringUs ()) + "," + millis() +  "\r\n";
      writeFile(SD, dataFileName.c_str(), firstLine.c_str());
      appendFile(SD, dataFileName.c_str(), "Sensor, acceleration x(*1000), acceleration y(*1000), acceleration z(*1000), gyro x, gyro y, gyro z, Hour \r\n");
      isStart = false;
     }
     else {
    if (mpu.update()) {
        sendData();
        
    }}
}

void print_calibration() {
    Serial.println("< calibration parameters >");
    Serial.println("accel bias [g]: ");
    Serial.print(mpu.getAccBiasX() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getAccBiasY() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getAccBiasZ() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.println();
    Serial.println("gyro bias [deg/s]: ");
    Serial.print(mpu.getGyroBiasX() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getGyroBiasY() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getGyroBiasZ() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.println();
    Serial.println("mag bias [mG]: ");
    Serial.print(mpu.getMagBiasX());
    Serial.print(", ");
    Serial.print(mpu.getMagBiasY());
    Serial.print(", ");
    Serial.print(mpu.getMagBiasZ());
    Serial.println();
    Serial.println("mag scale []: ");
    Serial.print(mpu.getMagScaleX());
    Serial.print(", ");
    Serial.print(mpu.getMagScaleY());
    Serial.print(", ");
    Serial.print(mpu.getMagScaleZ());
    Serial.println();
}

void httppost () {

   http.begin(servername+servicename);
   http.addHeader("Content-Type", "application/json");
   httpResponseCode = http.POST(data);
   String payload = http.getString();
   http.end();
   timedelay = payload.toInt();
   Serial.println(payload + httpResponseCode);
}

void httplog (String logMessage) {

   http.begin(servername+"/log/");
   http.addHeader("Content-Type", "application/text");
   httpResponseCode = http.POST("Sensor " + boardname + ": " + logMessage);
   String payload = http.getString();
   http.end();
   timedelay = payload.toInt();
   Serial.println(payload + httpResponseCode);
}

void httpheader () {

   http.begin(servername+"/header/");
   http.addHeader("Content-Type", "application/json");
   httpResponseCode = http.POST(header);
   String payload = http.getString();
   http.end();
   timedelay = payload.toInt();
   Serial.println(payload + httpResponseCode);
}

void sendData() {
  dataMessage = String(boardname)  + 
    ", " + String(mpu.getAccX() * 1000.0f) + ", " + String(mpu.getAccY() * 1000.0f) + ", " + String(mpu.getAccZ() * 1000.0f) +
    ", " + String(mpu.getGyroX()) + ", " + String(mpu.getGyroY()) + ", " + String(mpu.getGyroZ()) +
    ", " + String(millis ()) + " \r\n";
  //Serial.println("Save data: ");
  //Serial.println(dataMessage);
  appendFile(SD, dataFileName.c_str(), dataMessage.c_str()); 
 }

 // Write to the SD card (DON'T MODIFY THIS FUNCTION)
void writeFile(fs::FS &fs, const char * path, const char * message) {
  Serial.printf("Writing file: %s\n", path);

  File file = fs.open(path, FILE_WRITE);
  if(!file) {
    httplog ("Failed to open file for appending");
    Serial.println("Failed to open file for writing");
    return;
  }
  if(file.print(message)) {
    httplog ("File written");
    Serial.println("File written");
  } else {
    httplog ("Write failed");
    Serial.println("Write failed");
  }
  file.close();
}

// Append data to the SD card (DON'T MODIFY THIS FUNCTION)
void appendFile(fs::FS &fs, const char * path, const char * message) {
  //Serial.printf("Appending to file: %s\n", path);

  File file = fs.open(path, FILE_APPEND);
  if(!file) {
    httplog ("Failed to open file for appending");
    Serial.println("Failed to open file for appending");
    return;
  }
  if(file.print(message)) {
    //httplog ("Message appended");
    //Serial.println("Message appended");
  } else {
    httplog ("Append failed");
    Serial.println("Append failed");
  }
  file.close();
}

void readConfigureFile(){
  Serial.println("Read " + configFileName);
  float AccX, AccY, AccZ, GyroX, GyroY, GyroZ, MagBX, MagBY, MagBZ, MagSX, MagSY, MagSZ;
  char temp;
  char setting;
  bool isSetting = true;
  File configFile = SD.open(configFileName);
  if (configFile) {
    Serial.println(configFile);
    while (configFile.available()) {
      temp = configFile.read();
      if (isSetting == true) {
        if (temp == '=') {
          Serial.print("="); //Writes '=' to console
          isSetting  = false;
        }
        else {
          setting=temp;
          Serial.print(temp); //Writes SETTING part to console
        }
      }
      else {
        if (temp == '\n' || temp == '\r') {
          isSetting = true;
          }
        else {
          if(setting == 'AccBiasX'){
            AccX = temp;  
          }
          if(setting == 'AccBiasY'){
            AccY = temp;  
          }

          if(setting == 'AccBiasZ'){
            AccZ = temp;  
          }
          if(setting == 'GyroBiasX'){
            GyroX = temp;  
          }
          if(setting == 'GyroBiasY'){
            GyroY = temp;  
          }
          if(setting == 'GyroBiasZ'){
            GyroZ = temp;  
          }
          if(setting == 'MagBiasX'){
            MagBX = temp;  
          }
          if(setting == 'MagBiasY'){
            MagBY = temp;  
          }
          if(setting == 'MagBiasZ'){
            MagBZ = temp;  
          }
          if(setting == 'MagScaleX'){
            MagSX = temp;  
          }
          if(setting == 'MagScaleY'){
            MagSY = temp;  
          }
          if(setting == 'MagScaleZ'){
            MagSZ = temp;  
          }
          Serial.print(temp); //Writes VALUE part to console
          }
        }
    }
    configFile.close();
    mpu.setAccBias(AccX, AccY, AccZ);
    mpu.setGyroBias(GyroX, GyroY, GyroZ);
    mpu.setMagBias(MagBX, MagBY, MagBZ);
    mpu.setMagScale(MagSX, MagSY, MagSZ);
    isConfigured = true;
  } else {
    Serial.println("Can't open config.txt");
  }
}

void configure(){
    // calibrate anytime you want to
    httplog ("Accel Gyro calibration will start in 5sec.");
    Serial.println("Accel Gyro calibration will start in 5sec.");
    httplog ("Please leave the device still on the flat plane.");
    Serial.println("Please leave the device still on the flat plane.");
    mpu.verbose(true);
    delay(5000);
    mpu.calibrateAccelGyro();

    httplog ("Mag calibration will start in 5sec.");
    Serial.println("Mag calibration will start in 5sec.");
    httplog ("Please Wave device in a figure eight until done.");
    Serial.println("Please Wave device in a figure eight until done.");
    delay(5000);
    mpu.calibrateMag();

    print_calibration();
    mpu.verbose(false);
    
    Serial.println("Writing config file");
    isConfigured = true;
    //File configFile = SD.open("/CONFIG.TXT", FILE_WRITE);
    String message = "AccBiasX = " + String(mpu.getAccBiasX()) + "\n" +
                     "AccBiasY = " + String(mpu.getAccBiasY()) + "\n" +
                     "AccBiasZ = " + String(mpu.getAccBiasZ()) + "\n" +
                     "GyroBiasX = " + String(mpu.getGyroBiasX()) + "\n" +
                     "GyroBiasY = " + String(mpu.getGyroBiasY()) + "\n" +
                     "GyroBiasZ = " + String(mpu.getGyroBiasZ()) + "\n" +
                     "MagBiasX = " + String(mpu.getMagBiasX()) + "\n" +
                     "MagBiasY = " + String(mpu.getMagBiasY()) + "\n" +
                     "MagBiasZ = " + String(mpu.getMagBiasZ()) + "\n" +
                     "MagScaleX = " + String(mpu.getMagScaleX()) + "\n" +
                     "MagScaleY = " + String(mpu.getMagScaleY()) + "\n" +
                     "MagScaleZ = " + String(mpu.getMagScaleZ()) + "\n";
    
    File configFile = SD.open(configFileName.c_str());
    if(!configFile) {
      httplog ("Config file doens't exist");
      Serial.println("Config file doens't exist");
      httplog ("Creating config file...");
      Serial.println("Creating config file...");
      writeFile(SD, configFileName.c_str(), message.c_str());
    }
    else {
      httplog ("Config file already exists");
      Serial.println("Config file already exists");  
    }
    configFile.close();
    Serial.print(message);
    Serial.print("Configurado");
}
