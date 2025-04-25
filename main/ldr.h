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
#define EXAMPLE_LDR1_CHAN0          ADC_CHANNEL_8

// Define the adc attenuation
#define EXAMPLE_LDR_ATTEN           ADC_ATTEN_DB_12


// Define the adc pin
#define EXAMPLE_TUR1_CHAN0          ADC_CHANNEL_6

// Define the adc attenuation
#define EXAMPLE_TUR_ATTEN           ADC_ATTEN_DB_12

// Define de actuator pin
#define LED_PIN                     48
 

extern int tur_raw;
 

extern int ldr_raw;

void return_read_ldr(void *pvParameters);
void configurate_adc_ldr();
static bool example_adc_calibration_init_ldr(adc_unit_t unit, adc_channel_t channel, adc_atten_t atten, adc_cali_handle_t *out_handle);

#endif