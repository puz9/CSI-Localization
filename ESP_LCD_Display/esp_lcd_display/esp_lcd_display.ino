#include "function_holder.h"




void updateMap_task(void* param){
  while(1){
    updateMapDataFromServer();
    vTaskDelay(100);
  }
}
void update_lcd_task(void* param){
  while(1){
    map_data_to_lcd();
    vTaskDelay(100);
  }
}

void setup() {
  setup_lcd();
  connectToWiFi();

  // Create task for updateMap_task
  xTaskCreatePinnedToCore(
    updateMap_task,    // Task function
    "UpdateMapTask",   // Task name
    10000,             // Stack size (bytes)
    NULL,              // Task parameters (none in this case)
    1,                 // Task priority (lower number means higher priority)
    NULL,              // Task handle (optional, not used in this example)
    1                  // Core to run the task on (Core 1 in this case)
  );

  // Create task for update_lcd_task
  xTaskCreatePinnedToCore(
    update_lcd_task,   // Task function
    "UpdateLCDTask",   // Task name
    10000,             // Stack size (bytes)
    NULL,              // Task parameters (none in this case)
    1,                 // Task priority
    NULL,              // Task handle
    1                  // Core to run the task on (Core 1 in this case)
  );
}

void loop() {

}


