#include <WiFi.h>        // Include the Wi-Fi library
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>  // upload novas versões sem ligação física
#include "HTTPClient.h"
//#include <SoftwareSerial.h>
//#include <TinyGPS++.h>

static const int RXPIN = 16, TXPIN = 4;
static const uint32_t GPSBAUD = 4800;

// Create an instance of the TinyGPS object
TinyGPSPlus gps;

// Initialize the NewSoftSerial library to the pins you defined above
SoftwareSerial uart_gps(RXPIN, TXPIN);

HTTPClient http;

WiFiServer server(80); // servidor para escrever os resultados


// DEFINE HERE THE KNOWN NETWORKS
const char* KNOWN_SSID[] = {"Thomson2ED280", "DG-NGOH", "repeater"};
const char* KNOWN_PASSWORD[] = {"0E048F0A3D", "RaspberryPI", ""};
const int   KNOWN_SSID_COUNT = sizeof(KNOWN_SSID) /
sizeof(KNOWN_SSID[0]); // number of known networks
const char* boardname = "gps001";
String servicename="sensorvar4.php";
String servername="http://jmarcelino.no-ip.org/";
String data;
int httpResponseCode;
int timedelay = 10;
String mensagens;

void setup() {
   boolean wifiFound = false;
   int i, n;
   Serial.begin(9600);
   // ----------------------------------------------------------------
   // Set WiFi to station mode and disconnect from an AP if it was
previously connected
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
     while (true); // no need to go further, hang in there, will auto
launch the Soft WDT reset
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
     for (n = 0; n < KNOWN_SSID_COUNT; n++) { // walk through the list
of known SSID and check for a match

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
     while (true); // no need to go further, hang in there, will auto
launch the Soft WDT reset
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

   // Port defaults to 8266
   // ArduinoOTA.setPort(8266);

   // Hostname defaults to esp8266-[ChipID]
   ArduinoOTA.setHostname(boardname);

   // No authentication by default
   // ArduinoOTA.setPassword((const char *)"123");

   ArduinoOTA.onStart([]() {
     String type;
     if (ArduinoOTA.getCommand() == U_FLASH) {
       type = "sketch";
     } else { // U_SPIFFS
       type = "filesystem";
     }

     // NOTE: if updating SPIFFS this would be the place to unmount
SPIFFS using SPIFFS.end()
     Serial.println("Start updating " + type);
   });
   ArduinoOTA.onEnd([]() {
     Serial.println("\nEnd");
   });
   ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
     Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
   });
   ArduinoOTA.onError([](ota_error_t error) {
     Serial.printf("Error[%u]: ", error);
     if (error == OTA_AUTH_ERROR) {
       Serial.println("Auth Failed");
     } else if (error == OTA_BEGIN_ERROR) {
       Serial.println("Begin Failed");
     } else if (error == OTA_CONNECT_ERROR) {
       Serial.println("Connect Failed");
     } else if (error == OTA_RECEIVE_ERROR) {
       Serial.println("Receive Failed");
     } else if (error == OTA_END_ERROR) {
       Serial.println("End Failed");
     }
   });
   ArduinoOTA.begin();


   // give the Ethernet shield a second to initialize:
   delay(1000);
   server.begin();
   // write something to server just to inform
   data =
"fname="+String(boardname)+".sensor&fset="+String(boardname)+".set&var1=Hello_this_is_"
+ String(boardname) + "&+var2=" + String(0) + "&+var3=" + String(0) +
"&+var4=" + String(0);
   //Serial.println(data);
   Serial.println("Post to server");
   httppost();
   //delay(10000);
   //softReset(); // RESET!


   // Sets baud rate of your GPS
   uart_gps.begin(GPSBAUD);

   }


void loop() {

int n=gps.satellites.value();
if(n>=1){
   data =
"fname="+String(boardname)+".sensor&fset="+String(boardname)+".set&var1="+String(n)
+ "&+var2=" + String(gps.location.lat()) + "&+var3=" +
String(gps.location.lng()) + "&+var4=" + String(0);
   //Serial.println(data);
   Serial.println("Post to server");
   httppost();

   };
mensagens=String(n)+" "+String(gps.location.lat())+"
"+String(gps.location.lng());
Serial.println(mensagens);

   // put your main code here, to run repeatedly:
  ArduinoOTA.handle();
  WiFiClient client = server.available(); // Check if a client has connected
   if (!client)
   {
     return;
   }
   Serial.println("Cliente ligado");
   // existe um cliente ligado. Vamos escrever no server
   client.println("<!DOCTYPE html>"); //web page is made using HTML
   client.println("<html>");
   client.println("<h1>");
     client.print("This is ");
     client.println(String(boardname));
     Serial.println("Boardname "+String(boardname));
     client.println("</h1>");
     client.println("<br>");
       client.println("<body>");
         client.println(mensagens);
         client.println("<br>");
         client.print("Resultados em: ");
         client.print("<a
href='"+servername+String(boardname)+".sensor'>Ficheiro de leituras</a>");
         client.println("<br>");
         Serial.println("PHP?");
         if(httpResponseCode==200)
         {client.println("Servidor PHP - ON");}
         else
         {client.println("Servidor PHP - OFF");}
         Serial.println("PHP-Done");
       client.println("</body>");
   client.println("</html>");
   //client.stop();
}





void httppost () {

   http.begin(servername+servicename);
   http.addHeader("Content-Type", "application/x-www-form-urlencoded");
   httpResponseCode = http.POST(data);
   String payload = http.getString();
   http.end();
   timedelay = payload.toInt();
   Serial.println(payload + httpResponseCode);
   //Serial.println(httpResponseCode);
   //Serial.println();
}



void softReset(){
       ESP.restart();  // ESP.reset(); //;

}
