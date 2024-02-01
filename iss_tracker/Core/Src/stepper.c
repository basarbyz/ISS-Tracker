#include <math.h>
#include "stepper.h"
#include "stm32f4xx_hal.h"

void Stepper_Init(Stepper* stepper, PortPin step_port_pin, PortPin dir_port_pin, PortPin endswitch_port_pin, float angle_per_step) {
    stepper->step_pp = step_port_pin;
    stepper->dir_pp = dir_port_pin;
    stepper->endswitch_pp = endswitch_port_pin;
    stepper->angle_per_step = angle_per_step;
    stepper->current_angle = 0;
}

void Stepper_Step(Stepper* stepper) {
    HAL_GPIO_WritePin(stepper->step_pp.port, stepper->step_pp.pin, GPIO_PIN_SET);
    HAL_Delay(1);
    HAL_GPIO_WritePin(stepper->step_pp.port, stepper->step_pp.pin, GPIO_PIN_RESET);
    HAL_Delay(1);
}

void Stepper_TurnAngleRelative(Stepper* stepper, float angle) {
    // the angle is too small for the stepper to accurately turn
    if (fabsf(angle) < fabsf(stepper->angle_per_step))
        return;

    if (signbit(angle) != signbit(stepper->angle_per_step)) {
        Stepper_ToggleDirection(stepper);
    }

    float a;
    for (a = 0; fabsf(a) < fabsf(angle); a += stepper->angle_per_step)
        Stepper_Step(stepper);

    stepper->current_angle += a;
}

void Stepper_TurnToAngleAbsolute(Stepper* stepper, float target_angle) {
    auto normalized_target_angle = target_angle < 180 ? target_angle : target_angle - 360;
    auto angle_delta = normalized_target_angle - stepper->current_angle;
    Stepper_TurnAngleRelative(stepper, angle_delta);
}

void Stepper_ToggleDirection(Stepper* stepper) {
    HAL_GPIO_TogglePin(stepper->dir_pp.port, stepper->dir_pp.pin);
    stepper->angle_per_step *= -1;
}

void Stepper_ResetAngle(Stepper* stepper) {
    stepper->current_angle = 0;
}

GPIO_PinState Stepper_GetEndswitchState(Stepper* stepper) {
    return HAL_GPIO_ReadPin(stepper->endswitch_pp.port, stepper->endswitch_pp.pin);
}
