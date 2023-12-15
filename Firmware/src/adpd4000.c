
#include "adpd4000.h"
#include <stdint.h>
#include <SPI.h>


#define ADI_OK      0
#define ADI_ERROR  -1

#ifndef __STDINT_H_
    typedef int int16_t;
    typedef unsigned int uint16_t;
#endif

/* ADPD4000 SPI settings */
#define maxspeed 24000000 // ADPD4000 sclk frequency
#define dataorder MSBFIRST
#define datamode SPI_MODE0 // Check this!!!!
/**
 * @brief    function to write a byte and read specified number of bytes from Adpd400 SPI
 * @param    pTxData: 8-bit register address pointer
 * @param    pRxData: 8-bit data pointer
 * @param    TxSize: 16-bit size of the data to write to the hardware
 * @param    RxSize: 16-bit size of the data to read from the hardware
 * @retval   status: 0 (Success), -1 (Error)
 */
uint16_t Adpd400x_SPI_Receive(uint8_t *pTxData, uint8_t *pRxData, 
                              uint16_t TxSize, uint16_t RxSize) {
    // uint16_t cnt = 0;
    
    // cnt = spi.write((const char*)pTxData, (int)TxSize, 
    //                 (char *)pRxData, (int)RxSize);
    // spi_cs = 1;
    
    // serial_to_pc.printf("%u\r\n", cnt);
    
    // return ((TxSize + RxSize) == cnt)?ADI_HAL_OK:ADI_HAL_ERROR;

}

uint16_t Adpd400x_SPI_Transmit(uint8_t *pTxData, uint16_t TxSize) {

}