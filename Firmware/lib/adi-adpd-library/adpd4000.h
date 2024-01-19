#ifndef __ADPD4000_H
#define __ADPD4000__H


#include <stdint.h>

/* Bluepill pin values and settings */
#define BP_LED_BUILTIN PC13 // Bluepill built-in LED
#define BP_DATA_OUT PA7 // Bluepill MOSI 1
#define BP_DATA_IN PA6 // Bluepill MISO 1
#define BP_SCK PA5 // Bluepill SCK 1
#define BP_NSS PA3 // Bluepill Chip Select 1

/* spi 2 */
// #define BP_DATA_OUT PB15 // Bluepill MOSI 2
// #define BP_DATA_IN PB14 // Bluepill MISO 2
// #define BP_SCK PB13 // Bluepill SCK 2
// #define BP_NSS PB12 // Bluepill Chip Select 2

/* arduino */
// #define BP_LED_BUILTIN PB5
// #define BP_DATA_OUT PB3 // Bluepill MOSI 2
// #define BP_DATA_IN PB4  // Bluepill MISO 2
// #define BP_SCK PB5 // Bluepill SCK 2
// #define BP_NSS PB2 // Bluepill Chip Select 2
#define BLINK_DUR_ms 200

/* ADPD4000 SPI settings */
// #define maxspeed 24000000 // ADPD4000 sclk frequency
#define maxspeed 200000
#define dataorder MSBFIRST
#define datamode SPI_MODE0 



uint16_t Adpd400x_SPI_Receive(uint8_t *pTxData, uint8_t *pRxData, 
                              uint16_t TxSize, uint16_t RxSize);
uint16_t Adpd400x_SPI_Transmit(uint8_t *pTxData, uint16_t TxSize);

void blink_bp(int num_blinks);
void test_spi();
void read_chip_id();

#endif