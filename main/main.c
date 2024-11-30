#include <stdio.h>
#include "dht11.h"
#include "ds18b20.h"
#include "ldr.h"
#include "esp_log.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "sdkconfig.h"

#define DS_PIN 14

static const char *TAG = "MAIN";

// PROTOTYPES
void tarea_de_lecturas();


float TempC, TempF;

void DS18B20_readings()
{
	ds18b20_init(DS_PIN);
    ds18b20_requestTemperatures();

    TempC = ds18b20_get_temp();
    TempF = TempC*9/5 + 32;
		
}

void app_main()
{
    //configurate_adc();
    xTaskCreate(
        tarea_de_lecturas,
        "sensores_temp",
        4098,
        NULL,
        1,
        NULL
    );

    xTaskCreate(
        configurate_adc,
        "iniciar_adc",
        4098,
        NULL,
        1,
        NULL
    );
}

void tarea_de_lecturas()
{
    DHT11_init(GPIO_NUM_4);
    while(1) {
        DS18B20_readings();
        ESP_LOGI(TAG,"Water temperature is %.2f\n", TempC);
        ESP_LOGI(TAG,"Temperature is %d \n", DHT11_read().temperature);
        ESP_LOGI(TAG,"Humidity is %d\n", DHT11_read().humidity);
        //ESP_LOGI("Status code is %d\n", DHT11_read().status);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}