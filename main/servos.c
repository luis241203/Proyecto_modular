#include "servos.h"

static uint32_t angle_to_duty(uint32_t angle)
{
    uint32_t duty_us = SERVO_MIN_PULSEWIDTH_US +
                       ((SERVO_MAX_PULSEWIDTH_US - SERVO_MIN_PULSEWIDTH_US) * angle) / SERVO_MAX_DEGREE;

    uint32_t duty = (duty_us * LEDC_DUTY_MAX) / 20000; // 20ms periodo
    return duty;
}

static void servo_set_angle(ledc_channel_t channel, uint32_t angle)
{
    uint32_t duty = angle_to_duty(angle);
    ledc_set_duty(LEDC_LOW_SPEED_MODE, channel, duty);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, channel);
}

void config_servos(void)
{
    ledc_timer_config_t timer_conf = {
        .speed_mode       = LEDC_LOW_SPEED_MODE,
        .timer_num        = LEDC_TIMER_0,
        .duty_resolution  = LEDC_DUTY_RES,
        .freq_hz          = SERVO_PWM_FREQUENCY,
        .clk_cfg          = LEDC_AUTO_CLK
    };
    ledc_timer_config(&timer_conf);

    ledc_channel_config_t channel1 = {
        .gpio_num       = SERVO_FAN1_PWM_GPIO,
        .speed_mode     = LEDC_LOW_SPEED_MODE,
        .channel        = LEDC_CHANNEL_0,
        .intr_type      = LEDC_INTR_DISABLE,
        .timer_sel      = LEDC_TIMER_0,
        .duty           = 0,
        .hpoint         = 0
    };
    ledc_channel_config(&channel1);

        // Servo 2
        ledc_channel_config_t channel2 = {
            .gpio_num       = SERVO_FAN2_PWM_GPIO ,
            .speed_mode     = LEDC_LOW_SPEED_MODE,
            .channel        = LEDC_CHANNEL_1,
            .intr_type      = LEDC_INTR_DISABLE,
            .timer_sel      = LEDC_TIMER_0,
            .duty           = 0,
            .hpoint         = 0
        };
    ledc_channel_config(&channel2);

    // Servo 3
    ledc_channel_config_t channel3 = {
        .gpio_num       = SERVO_EXP_PWM_GPIO ,
        .speed_mode     = LEDC_LOW_SPEED_MODE,
        .channel        = LEDC_CHANNEL_2,
        .intr_type      = LEDC_INTR_DISABLE,
        .timer_sel      = LEDC_TIMER_0,
        .duty           = 0,
        .hpoint         = 0
    };
    ledc_channel_config(&channel3);
}
