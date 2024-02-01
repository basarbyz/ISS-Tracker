#ifndef INC_PORTPIN_H_
#define INC_PORTPIN_H_

#include <stdlib.h>
#include "stm32f4xx_hal.h"

typedef struct {
    GPIO_TypeDef* port;
    uint16_t pin;
} PortPin;

#endif /* INC_PORTPIN_H_ */
