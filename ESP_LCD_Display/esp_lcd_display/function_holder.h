#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#include "lcd_fn.h"

const char* ssid = "OPPO_KUY";
const char* password = "oppopass";

uint8_t map_data[4][4]={
  {0,0,0,0},
  {0,0,0,0},
  {0,0,0,0},
  {0,0,0,0}
};
String baseUrl="http://192.168.122.19:8000";

bool isWiFiConnected(){
  return WiFi.status() == WL_CONNECTED;
}
void connectToWiFi(){
  Serial.print("Connecting WiFi to ");
  Serial.println(ssid);
  WiFi.begin(ssid,password);
  while( isWiFiConnected()==false){
    Serial.print(".");
    delay(1000);
  }
  Serial.println();
}

void updateMapDataFromServer(){
  HTTPClient http;
  String url=baseUrl+String("/map_data/latest");
  http.begin(url);
  int httpResponseCode = http.GET();
  if (httpResponseCode > 0) {
    if(httpResponseCode == HTTP_CODE_OK){
      String payload = http.getString();
      Serial.println("Response payload: " + payload);
      DynamicJsonDocument jsonDoc(1024);
      DeserializationError error = deserializeJson(jsonDoc,payload);
      if(error){
        Serial.print("deserilizeJson() failed: ");
        Serial.println(error.c_str());
      }else{
        Serial.println("Map Array:");
        JsonArray mapArray = jsonDoc["map_data"].as<JsonArray>();
        for(int i=0;i<mapArray.size();++i){
          JsonArray row=mapArray[i];
          for(int j=0;j<row.size();++j){
            uint8_t v=row[j].as<uint8_t>();
            Serial.print(v);
            Serial.print(" ");
            map_data[i][j]=row[j].as<int>();
          }
          Serial.println();
        }
        Serial.println();
      }
    }else{
      Serial.println("HTTP Error code: ");
      Serial.println(httpResponseCode);
    }
  }else{
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
    if(httpResponseCode==-1){
      if(isWiFiConnected()){
        Serial.println("URL address might be wrong or Server is unavailabled.");
      }else{
        Serial.println("Try connecting");
        connectToWiFi();
      }
    }
  }
  http.end();
}
uint32_t human_frame = 0;
void map_data_to_lcd(){
  clear_lcd();
  for(int x=0;x<4;++x){
    for(int y=0;y<4;++y){
      if(map_data[y][x]==1)
        draw_human(x,y,human_frame);
    }
  }
  display_lcd();
  human_frame=(human_frame+1)%28;
}