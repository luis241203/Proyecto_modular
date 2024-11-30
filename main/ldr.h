#ifndef LDR_H_  
#define LDR_H_

// Headers for the adc configuration
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

// Define the adc pin
#define EXAMPLE_ADC1_CHAN0          ADC_CHANNEL_8

// Define the adc attenuation
#define EXAMPLE_ADC_ATTEN           ADC_ATTEN_DB_12

// Define the gpio pin
#define GPIO_NUM         47           

void return_read(void *pvParameters);
void configurate_adc();
static bool example_adc_calibration_init(adc_unit_t unit, adc_channel_t channel, adc_atten_t atten, adc_cali_handle_t *out_handle);

#endif