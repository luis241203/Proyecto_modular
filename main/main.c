#include <stdio.h>
#include "dht11.h"
#include "ds18b20.h"
#include "ldr.h"
#include "servos.h"
#include "esp_log.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "sdkconfig.h"

#define DS_PIN 14
#define FAN_OUTPUT_PIN 47

static const char *TAG = "MAIN";

// PROTOTYPES
void tarea_de_lecturas();
void tarea_sensor_ambiente();


float TempC, TempF;
int temp_amb, hum_amb;
int temp_amb_lim = 34;

void DS18B20_readings()
{
	ds18b20_init(DS_PIN);
    ds18b20_requestTemperatures();

    TempC = ds18b20_get_temp();
    TempF = TempC*9/5 + 32;
		
}

void app_main()
{
    DHT11_init(GPIO_NUM_4);
    config_servos();
    gpio_set_direction(FAN_OUTPUT_PIN, GPIO_MODE_OUTPUT);
    //configurate_adc();
    xTaskCreate(
        tarea_sensor_ambiente,
        "ambiente",
        4098,
        NULL,
        2,
        NULL
    );

    xTaskCreate(
        tarea_de_lecturas,
        "sensores_temp",
        4098,
        NULL,
        1,
        NULL
    );

    xTaskCreate(
        configurate_adc_ldr,
        "iniciar_adc_ldr",
        4098,
        NULL,
        2,
        NULL
    );
}

void tarea_de_lecturas()
{
    while(1) {
        DS18B20_readings();
        ESP_LOGI(TAG,"Water temperature is %.2f\n", TempC);
        ESP_LOGI(TAG,"Temperature is %d \n", temp_amb);
        ESP_LOGI(TAG,"Humidity is %d\n", hum_amb);
        ESP_LOGI(TAG,"LDR ADC READING =  %d\n", ldr_raw);
        ESP_LOGI(TAG,"TUR ADC READING =  %d\n", tur_raw);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void tarea_sensor_ambiente()
{
    while (1)
    {
        temp_amb = DHT11_read().temperature;
        hum_amb = DHT11_read().humidity;
        vTaskDelay(pdMS_TO_TICKS(1000));

        if(temp_amb >= temp_amb_lim)
        {
            ESP_LOGI(TAG, "SE ENCIENDE VENTILADOR");
            gpio_set_level(FAN_OUTPUT_PIN, 1);
            servo_set_angle(LEDC_CHANNEL_0, 180);
        }
        else{
            ESP_LOGI(TAG, "VENTILADOR APAGADO");
            gpio_set_level(FAN_OUTPUT_PIN, 0);
            servo_set_angle(LEDC_CHANNEL_0, 0);
        }
    }
}