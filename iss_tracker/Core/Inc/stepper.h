#ifndef INC_STEPPER_H_
#define INC_STEPPER_H_

#include "portPin.h"

typedef struct {
    PortPin step_pp;
    PortPin dir_pp;
    PortPin endswitch_pp;
    float angle_per_step;
    float current_angle;
} Stepper;

void Stepper_Init(Stepper* stepper, PortPin step_port_pin, PortPin dir_port_pin, PortPin endswitch_port_pin, float angle_per_step);
void Stepper_TurnAngleRelative(Stepper* stepper, float angle);
void Stepper_TurnToAngleAbsolute(Stepper* stepper, float angle);
void Stepper_Step(Stepper* stepper);
void Stepper_ResetAngle(Stepper* stepper);
GPIO_PinState Stepper_GetEndswitchState(Stepper* stepper);

#endif /* INC_STEPPER_H_ */
