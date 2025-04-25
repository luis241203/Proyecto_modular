#ifndef SERVOS_H_  
#define SERVOS_H_

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/ledc.h"
#include "esp_err.h"

#define SERVO_MIN_PULSEWIDTH_US (500)   // 0.5 ms
#define SERVO_MAX_PULSEWIDTH_US (2500)  // 2.5 ms
#define SERVO_MAX_DEGREE        (180)
#define SERVO_PWM_FREQUENCY     (50)    // 50 Hz
#define SERVO_FAN1_PWM_GPIO     (11)
#define SERVO_FAN2_PWM_GPIO     (12)
#define SERVO_EXP_PWM_GPIO     (13)

#define LEDC_DUTY_RES           LEDC_TIMER_14_BIT
#define LEDC_DUTY_MAX           ((1 << 14) - 1) // 16383

static uint32_t angle_to_duty(uint32_t angle);

static void servo_set_angle(ledc_channel_t channel, uint32_t angle);

void config_servos(void);

#endif