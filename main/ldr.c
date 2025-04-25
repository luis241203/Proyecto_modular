#include "ldr.h"

const static char *TAG = "ADC_LDR";

int ldr_raw;
int tur_raw;

int ldr_lim = 2000;

void return_read_ldr(void *pvParameters)
{
    
    while (1)
    {
        adc_oneshot_unit_handle_t *ldr_handle = (adc_oneshot_unit_handle_t *)pvParameters;
        ESP_ERROR_CHECK(adc_oneshot_read(ldr_handle, EXAMPLE_LDR1_CHAN0, &ldr_raw));
        ESP_ERROR_CHECK(adc_oneshot_read(ldr_handle, EXAMPLE_TUR1_CHAN0, &tur_raw));
        
        if (ldr_raw >= ldr_lim)
        {
            gpio_set_level(LED_PIN, 1);
        }
        else
        {
            gpio_set_level(LED_PIN, 0);
        }
        
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void configurate_adc_ldr()
{
    /*CONFIGURING THE LEDS*/
    gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);
    //-------------ADC1 Init---------------//
    adc_oneshot_unit_handle_t ldr1_handle;
    adc_oneshot_unit_init_cfg_t init_config1 = {
        .unit_id = ADC_UNIT_1,
    };

    ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config1, &ldr1_handle));

    adc_oneshot_chan_cfg_t config = {
    .bitwidth = ADC_BITWIDTH_DEFAULT,
    .atten = EXAMPLE_LDR_ATTEN,
    };

    adc_oneshot_chan_cfg_t config_turb = {
        .bitwidth = ADC_BITWIDTH_DEFAULT,
        .atten = EXAMPLE_TUR_ATTEN,
        };

    ESP_ERROR_CHECK(adc_oneshot_config_channel(ldr1_handle, EXAMPLE_LDR1_CHAN0, &config));
    ESP_ERROR_CHECK(adc_oneshot_config_channel(ldr1_handle, EXAMPLE_TUR1_CHAN0, &config_turb));

    //-------------ADC1 Calibration Init---------------//
    adc_cali_handle_t adc1_cali_chan0_handle = NULL;
    adc_cali_handle_t adc1_cali_chan1_handle = NULL;
    example_adc_calibration_init_ldr(ADC_UNIT_1, EXAMPLE_LDR1_CHAN0, EXAMPLE_LDR_ATTEN, &adc1_cali_chan0_handle);
    example_adc_calibration_init_ldr(ADC_UNIT_1, EXAMPLE_TUR1_CHAN0, EXAMPLE_TUR_ATTEN, &adc1_cali_chan1_handle);

    //-------------ADC1 start reading---------------//
    xTaskCreate(return_read_ldr,"sensor_ldr_task",4096, (void *)&ldr1_handle,1,NULL);

    vTaskDelete(0);
}

static bool example_adc_calibration_init_ldr(adc_unit_t unit, adc_channel_t channel, adc_atten_t atten, adc_cali_handle_t *out_handle)
{
    adc_cali_handle_t handle = NULL;
    esp_err_t ret = ESP_FAIL;
    bool calibrated = false;

#if ADC_CALI_SCHEME_CURVE_FITTING_SUPPORTED
    if (!calibrated) {
        ESP_LOGI(TAG, "calibration scheme version is %s", "Curve Fitting");
        adc_cali_curve_fitting_config_t cali_config = {
            .unit_id = unit,
            .chan = channel,
            .atten = atten,
            .bitwidth = ADC_BITWIDTH_DEFAULT,
        };
        ret = adc_cali_create_scheme_curve_fitting(&cali_config, &handle);
        if (ret == ESP_OK) {
            calibrated = true;
        }
    }
#endif

#if ADC_CALI_SCHEME_LINE_FITTING_SUPPORTED
    if (!calibrated) {
        ESP_LOGI(TAG, "calibration scheme version is %s", "Line Fitting");
        adc_cali_line_fitting_config_t cali_config = {
            .unit_id = unit,
            .atten = atten,
            .bitwidth = ADC_BITWIDTH_DEFAULT,
        };
        ret = adc_cali_create_scheme_line_fitting(&cali_config, &handle);
        if (ret == ESP_OK) {
            calibrated = true;
        }
    }
#endif

    *out_handle = handle;
    if (ret == ESP_OK) {
        ESP_LOGI(TAG, "Calibration Success");
    } else if (ret == ESP_ERR_NOT_SUPPORTED || !calibrated) {
        ESP_LOGW(TAG, "eFuse not burnt, skip software calibration");
    } else {
        ESP_LOGE(TAG, "Invalid arg or no memory");
    }

    return calibrated;
}