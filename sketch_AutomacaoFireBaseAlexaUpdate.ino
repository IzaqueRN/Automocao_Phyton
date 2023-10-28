/*
  Complete project details: https://RandomNerdTutorials.com/esp8266-nodemcu-https-requests/ 
  Based on the BasicHTTPSClient.ino Created on: 20.08.2018 (ESP8266 examples)
*/

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>
#include <ArduinoJson.h>
// Replace with your network credentials
const char* ssid = "Totonho";
const char* password = "27592230";
const String device_name[] = {"sensor","quarto","id_device_null"};
String dados ="";
String token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwZTFkMjM5MDllNzZmZjRhNzJlZTA4ODUxOWM5M2JiOTg4ZjE4NDUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZmlyLWFsZXhhLTc1NGJkIiwiYXVkIjoiZmlyLWFsZXhhLTc1NGJkIiwiYXV0aF90aW1lIjoxNjg0NTY2NjEyLCJ1c2VyX2lkIjoiMUZlY2FpWjdoWWI5ODRtSTlrZm02alpmeldHMiIsInN1YiI6IjFGZWNhaVo3aFliOTg0bUk5a2ZtNmpaZnpXRzIiLCJpYXQiOjE2ODQ2MTM3MzcsImV4cCI6MTY4NDYxNzMzNywiZW1haWwiOiJpcm4uaXphcXVlQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJpcm4uaXphcXVlQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.lF7Q8gHNLp4aZo0UNhJfX9QL6diwGg8ZkuR41Kl-PJD4zWYww9xwaXUVlFI-L0rgTSxXdfSsOrHd6VaqfV2aqTjk5yVSGLOLYzEHRSIB-uwPanG7AUfUFKuPlEKZlTv2ELesJnH9WCwNAqZWZlkck_XAt2HGmNMw2iLtDLnaNqetMb_k8LkbvpR-Hg_baTvFxlTZ9AUIDa16Dx7R8vfNcwvPcbnU6dKBLHYcyhVrOzM46M7kRRk5-YzjEPEy3Ej-qNdHfoMu6C7ozuwm5U7h047W03YrdnzW1t0Uca00AMGJfIh44bSvaB-2Q2bJSnlYM_k-9irPMK0-MUAA4Kk1_w";
void setup() {
  Serial.begin(115200);
  //Serial.setDebugOutput(true);
  pinMode(2, OUTPUT);
  Serial.println();
  Serial.println();
  Serial.println();

  //Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
}


void loop() {
  // wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) {

    std::unique_ptr<BearSSL::WiFiClientSecure>client(new BearSSL::WiFiClientSecure);

    // Ignore SSL certificate validation
    client->setInsecure();
    
    //create an HTTPClient instance
    HTTPClient https;
    int httpCode = 0;
    //Initializing an HTTPS communication using the secure client
    Serial.print("[HTTPS] begin...\n");
    if (https.begin(*client, "https://fir-alexa-754bd-default-rtdb.firebaseio.com/"+device_name[0]+"/"+device_name[1]+".json?print=pretty&auth=" + token)) {  // HTTPS
      Serial.print("[HTTPS] PUT...\n");
      // start connection and send HTTP header
    DynamicJsonDocument doc(1024);
    doc["temperatura"] = random(-60, 100);
    dados ="";
    serializeJson(doc, dados);
      httpCode = https.PUT(dados);
      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTPS] PUT... code: %d\n", httpCode);
        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = https.getString();
          Serial.println(payload);
          if(payload.toInt() > 0)
          {
            digitalWrite(2,1);
          }else
          {
            digitalWrite(2,0);
          }

        }
      } else {
        Serial.printf("[HTTPS] PUT... failed, error: %s\n", https.errorToString(httpCode).c_str());
      }

      https.end();
    } else {
      Serial.printf("[HTTPS] Unable to connect\n");
    }

  }
  Serial.println();
  Serial.println("Waiting the next round...");
  delay(1000);
}
