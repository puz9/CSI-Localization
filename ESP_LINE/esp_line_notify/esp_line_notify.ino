#include "function_holder.h"

void setup() {
  Serial.begin(115200);
  Serial.println("BOO");
  // Connect to Wi-Fi
  connectToWiFi();
}

void loop() {
  if (isWiFiConnected()==false) {
    // WiFi is disconnected, attempt to reconnect
    Serial.println("WiFi might be disconnected");
    connectToWiFi();
    return;
  }
  updateMapDataFromServer();
  sendMapDataToLine(true);
  delay(1000);
}
