#ifndef __ADPD4000_H
#define __ADPD4000__H

#include <stdint.h>

uint16_t Adpd400x_SPI_Receive(uint8_t *pTxData, uint8_t *pRxData, 
                              uint16_t TxSize, uint16_t RxSize);
uint16_t Adpd400x_SPI_Transmit(uint8_t *pTxData, uint16_t TxSize);

#endif