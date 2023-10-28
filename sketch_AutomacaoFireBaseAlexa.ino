/*
  Complete project details: https://RandomNerdTutorials.com/esp8266-nodemcu-https-requests/ 
  Based on the BasicHTTPSClient.ino Created on: 20.08.2018 (ESP8266 examples)
*/

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>

// Replace with your network credentials
const char* ssid = "Totonho";
const char* password = "27592230";
const String device_name[] = {"lampada","quarto","id_device_null"};

String token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwZTFkMjM5MDllNzZmZjRhNzJlZTA4ODUxOWM5M2JiOTg4ZjE4NDUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZmlyLWFsZXhhLTc1NGJkIiwiYXVkIjoiZmlyLWFsZXhhLTc1NGJkIiwiYXV0aF90aW1lIjoxNjg0NTY2NjEyLCJ1c2VyX2lkIjoiMUZlY2FpWjdoWWI5ODRtSTlrZm02alpmeldHMiIsInN1YiI6IjFGZWNhaVo3aFliOTg0bUk5a2ZtNmpaZnpXRzIiLCJpYXQiOjE2ODQ2MDg2NzQsImV4cCI6MTY4NDYxMjI3NCwiZW1haWwiOiJpcm4uaXphcXVlQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJpcm4uaXphcXVlQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.KYoWXQDf-rpITOfSuqKO_KnFQgS2Sm_MQOpMJ4onQahhihyGYxsZg5NXPQAhrAlG5as7Wh-aTxCazgEtdFe08ywqdmmuaq1b0Hdga4ttPhLljK17L9wmYj6ej9kuj9-vBxAzXe9joTzEz1uM4Qwc2O0v5GujjnLYcbTOt97JsrysaE7P82_l7pEFx-ZGiEJmLcIUnArutgS7WYwt23h-L0tukcSjGHHQ1lw0oAMaayJ7iC8medN5axgZ_woxcpRbRw6vQrFhK6Oad-dkTDUhai2rIpjelWzNasrK8ZKQVPWD3c5xep9elWaF57sQR6fg1d2QjQHxaaJ1yUtbOtBpNA";
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
    
    //Initializing an HTTPS communication using the secure client
    Serial.print("[HTTPS] begin...\n");
    if (https.begin(*client, "https://fir-alexa-754bd-default-rtdb.firebaseio.com/"+device_name[0]+"/"+device_name[1]+".json?print=pretty&auth=" + token)) {  // HTTPS
      Serial.print("[HTTPS] GET...\n");
      // start connection and send HTTP header
      int httpCode = https.GET();
      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTPS] GET... code: %d\n", httpCode);
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
        Serial.printf("[HTTPS] GET... failed, error: %s\n", https.errorToString(httpCode).c_str());
      }

      https.end();
    } else {
      Serial.printf("[HTTPS] Unable to connect\n");
    }

  }
  Serial.println();
  Serial.println("Waiting the next round...");
  delay(5000);
}