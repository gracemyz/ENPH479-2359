
#include <SPI.h>
#include "adi_adpd_driver.h"
#include "adi_adpd_reg.h"
#include "adi_adpd_reg.h"
#include "adpd4000.h"
#include "Arduino.h"
#include "stdint.h" 

/* ADI */
#define ADI_OK      0
#define ADI_ERROR  -1


/**
 * @brief Blink the bluepill's builtin LED a number of times
 * @param num_blinks 
 * @retval none
 */
void blink_bp(int num_blinks) {
  for (int i=0; i < num_blinks; i++) {
    delay(BLINK_DUR_ms);
    digitalWrite(BP_LED_BUILTIN, LOW);
    delay(BLINK_DUR_ms);
    digitalWrite(BP_LED_BUILTIN, HIGH);
  }
}

/**
 * @brief Alternate LED1A and LED1B at two current values. 
 * @param none
 * @retval none
 */
void test_spi() {
  // uint16_t green_reg = ADPD4x_REG_LED_POW12_A;


  uint16_t ledRegAddress = ADPD4x_REG_LED_POW12_A; // timing slot A, I think

  // hardcoded lol. see adi_adpd_slotops_helper for a more flexible function 
  // in order: LED1A 50mA, LED1A 100mA, LED1B 50mA, LED1B 100mA
  // uint16_t led_values[4] = {32U, 64U, 160U, 192U};
  uint16_t led_values[2] = {8U, 16U};

  // uint16_t led1A_50mA = 32U;
  // uint16_t led1A_100mA = 64U;
  // uint16_t led1B_50mA = 160U;
  // uint16_t led1B_100mA = 192U;

  // first 16 bits: 15 bit register address and 1 bit write command
  uint16_t firsthalf = ((ledRegAddress) << 1U) | ADPD400x_SPI_WRITE; 
  // if all bits are 0, then 0 current?
  uint32_t led_off = ((firsthalf) << 16U) | (uint16_t) 0;
  uint32_t buffer;
  
  int delay_ms = 200;
  
  SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
  digitalWrite(BP_NSS, LOW); //enable device

  for (int i = 0; i < sizeof(led_values); i++) {
    buffer = ((firsthalf) << 16U) | led_values[i];
    SPI.transfer(&buffer, 4);
    delay(delay_ms);
    SPI.transfer(&led_off, 4);
    delay(delay_ms);
  }
  digitalWrite(BP_NSS, HIGH);
  SPI.endTransaction();

}

void read_chip_id() {

  SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
  digitalWrite(BP_NSS, LOW);
  uint16_t buffer = ((ADPD4x_REG_CHIP_ID) << 1U) & ADPD400x_SPI_READ; 
  SPI.transfer16(buffer);
  SPI.transfer16(0x00);
  digitalWrite(BP_NSS, HIGH);
  SPI.endTransaction();

}

void MCU_HAL_Delay(uint32_t d) {
  delay(d);
}

uint16_t Adpd400x_I2C_Transmit(uint8_t *register_address, uint16_t txsize) {
  return ADI_ERROR;
}
uint16_t Adpd400x_I2C_TxRx(uint8_t *register_address, uint8_t *buffer, uint16_t txsize, uint16_t rxsize) {
  return ADI_ERROR;
}

uint16_t Adpd400x_SPI_Receive(uint8_t *pTxData, uint8_t *pRxData, uint16_t TxSize, uint16_t RxSize) {
    SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
    digitalWrite(BP_NSS, LOW); //enable device

    for (int i=0; i < (int)TxSize; i++) {
        SPI.transfer(pTxData[i]);
    }

    // The SPI protocol is based on a one byte OUT / one byte IN interface. 
    // For every byte expected to be received, one (dummy, typically 0x00 or 0xFF) byte must be sent.
    for (int i=0; i < (int)RxSize; i++) {
        pRxData[i] = SPI.transfer(0x00);
    }
    
    digitalWrite(BP_NSS, HIGH);
    SPI.endTransaction();


    return ((TxSize + RxSize) == sizeof(pTxData) + sizeof(pRxData))?ADI_OK:ADI_ERROR;

}

uint16_t Adpd400x_SPI_Transmit(uint8_t *pTxData, uint16_t TxSize) {
    SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
    digitalWrite(BP_NSS, LOW); //enable device

    for (int i=0; i < (int)TxSize; i++) {
        SPI.transfer(pTxData[i]);
    }
    
    digitalWrite(BP_NSS, HIGH);
    SPI.endTransaction();
    
}