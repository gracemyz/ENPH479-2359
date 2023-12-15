
#include "adpd4000.h"
#include <stdint.h>
#include <SPI.h>

/* Bluepill pin values and settings */
#define BP_LED_BUILTIN PC13 // Bluepill built-in LED
#define BP_DATA_OUT PA7     // Bluepill MOSI 1
#define BP_DATA_IN PA6      // Bluepill MISO 1
#define BP_SCK PA6          // Bluepill SCK 1
#define BP_NSS PA5          // Bluepill Chip Select 1

/* ADI */
#define ADI_OK 0
#define ADI_ERROR -1

/**
 * Including this because sometimes uint16_t doesn't get recognized as a type
 * even though stdint.h is included...
 */
// #ifndef __STDINT_H_
//     typedef int int16_t;
//     typedef unsigned int uint16_t;
// #endif

/* ADPD4000 SPI settings */
#define maxspeed 24000000 // ADPD4000 sclk frequency
#define dataorder MSBFIRST
#define datamode SPI_MODE0 // Check this!!!!
/**
 * @brief    function to write a byte and read specified number of bytes from Adpd400 SPI
 * @param    pTxData: 8-bit register address pointer. Array of 2 bytes
 * @param    pRxData: 8-bit data pointer. Array of 4 bytes
 * @param    TxSize: 16-bit size of the data to write to the hardware
 * @param    RxSize: 16-bit size of the data to read from the hardware
 * @retval   status: 0 (Success), -1 (Error)
 */
uint16_t Adpd400x_SPI_Receive(uint8_t *pTxData, uint8_t *pRxData, uint16_t TxSize, uint16_t RxSize)
{
    SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
    digitalWrite(BP_NSS, LOW); // enable device

    // Write register address and READ command
    uint16_t buffer = (pTxData[0] << 8) | (pTxData[1]);
    SPI.transfer(&buffer, (int)TxSize);

    // The SPI protocol is based on a one byte OUT / one byte IN interface.
    // For every byte expected to be received, one (dummy, typically 0x00 or 0xFF) byte must be sent.
    for (int i = 0; i < (int)RxSize; i++)
    {
        pRxData[i] = SPI.transfer(0x00);
    }

    digitalWrite(BP_NSS, HIGH);
    SPI.endTransaction();

    return ((TxSize + RxSize) == sizeof(pTxData) + sizeof(pRxData)) ? ADI_OK : ADI_ERROR;
}
/**
//  * @brief    function to transmit data through Adpd400x SPI
//  * @param    8-bit register address pointer
//  * @param    16-bit size of the data to write to the hardware
//  * @retval   status: 0 (Success), -1 (Error)
//  */

uint16_t Adpd400x_SPI_Transmit(uint8_t *pTxData, uint16_t TxSize)
{
    // me
    //*pTxData: 8-bit register address pointer
    // TxSize: 16-bit size of the data to write to the hardware

    // use arduino spi library instead of adpd

    //     uint16_t cnt = 0;
    //
    //     spi_cs_mux = 1;
    //     spi_cs = 0;
    //     cnt = spi.write((const char *)pTxData, (int)TxSize, 0, 0);
    //     spi_cs = 1;
    // SPI.transfer((const char *)pTxData, (int)TxSize);

    return (TxSize == (int)TxSize);
    //?ADI_HAL_OK:ADI_HAL_ERROR;
}