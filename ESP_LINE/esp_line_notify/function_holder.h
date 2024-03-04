//Cover wifi connecting
//Cover request to PC's local server

#include "TridentTD_LineNotify.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define LINE_TOKEN "LmrfwOvhBiVAoOtpoxEQ1BwGdbrsnPMaut4o3ogCQqZ"


const char* ssid = "OPPO_KUY";
const char* password = "oppopass";
//ip address history
// "192.168.222.18"
const char* serverAddress = "192.168.122.19"; // Replace with the IP address of your PC
const int serverPort = 8000; // Port on which FastAPI server is running
String url="http://"+String(serverAddress)+":"+serverPort;



String takenArea="🟥";
String emptyArea="⬛";
String wtfArea="🟧";


bool isWiFiConnected(){
  return WiFi.status() == WL_CONNECTED;
}

void connectToWiFi(){
  // if(isWiFiConnected()==false){
  //   Serial.println("Connecting to WiFi...");
  //   WiFi.begin(ssid,password);
  //   while( isWiFiConnected()==false){
  //     Serial.print(".");
  //     delay(1000);
  //   }
  //   Serial.println();
  // }

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid,password);
  while( isWiFiConnected()==false){
    Serial.print(".");
    delay(1000);
  }
  Serial.println();
}



uint8_t map_data0[4][4];
uint8_t map_data[4][4];

void updateMapDataFromServer(){
  HTTPClient http;
  String url="http://"+String(serverAddress)+":"+String(serverPort)+"/map_data/latest";
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
        Serial.println("Server address might be wrong or Server is unavailabled.");
      }else{
        Serial.println("Try connecting");
        connectToWiFi();
      }
    }
  }
  http.end();
}

float compare_2d_arrays(uint8_t arr1[4][4], uint8_t arr2[4][4]) {
    // Count the number of differing elements
    int differing_elements = 0;
    int total_elements = 16; // Total number of elements in a 4x4 matrix

    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (arr1[i][j] != arr2[i][j]) {
                differing_elements++;
            }
        }
    }

    // Calculate the percentage of differing elements
    float difference_percentage = (float)differing_elements / total_elements * 100;

    return difference_percentage;
}

void sendMapDataToLine(bool only_if_different=true){
  float diff_percent=compare_2d_arrays(map_data0,map_data);
  if(only_if_different==true && diff_percent<5){
    Serial.print("Not sent to LINE, ");
    Serial.print(diff_percent);
    Serial.println("%");
    return;
  }
  LINE.setToken(LINE_TOKEN);
  String msg="";
  for(int i=0;i<4;++i){
    msg+="\n";
    for(int j=0;j<4;++j){
      switch(map_data[i][j]){
        case 0:
          msg+=emptyArea;
          break;
        case 1:
          msg+=takenArea;
          break;
        default:
          msg+=wtfArea;
          break;
      }
    }
  }
  LINE.notify(msg);
  Serial.print("Sent message to LINE, ");
  Serial.print(diff_percent);
  Serial.println("%");


  for(int i=0;i<4;++i){
    for(int j=0;j<4;++j){
      map_data0[i][j]=map_data[i][j];
    }
  }

}
