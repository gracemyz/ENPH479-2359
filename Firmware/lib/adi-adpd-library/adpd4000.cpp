
#include <SPI.h>

#include "adi_adpd_driver.h"
#include "adi_adpd_reg.h"
#include "adi_adpd_ssm.h"
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
    digitalWrite(BP_LED_BUILTIN, HIGH);
    delay(BLINK_DUR_ms);
    digitalWrite(BP_LED_BUILTIN, LOW);
  }
}

/**
 * @brief Alternate LED1A and LED1B at two current values. 
 * @param none
 * @retval none
 */
void test_spi() {

  uint16_t nUId = E_ADI_ADPD_SLOTA;
  ADI_ADPD_LEDID nLed = E_ADI_ADPD_LED2A;
  uint16_t led_values[2] = {8U, 16U};
  uint16_t ret;

  // read_chip_id_lib();
  ret = adi_adpdssm_SetLedCurrent(nUId,  nLed, 0);
  uint16_t *pLedCurrent;
  adi_adpdssm_GetLedCurrent(nUId, nLed, pLedCurrent);
  if (*pLedCurrent == 0) {
    blink_bp(2);

  } else {
    blink_bp(1);
  }
  delay(1000);



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

void read_chip_id_lib() {
  uint16_t reg = ADPD4x_REG_CHIP_ID;
  uint16_t data = 0U;
  if (adi_adpddrv_RegRead(reg, &data) == 0) {
    blink_bp(1);
  } else {
    blink_bp(2);
  }

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


    return ADI_OK;

}

uint16_t Adpd400x_SPI_Transmit(uint8_t *pTxData, uint16_t TxSize) {
    SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
    digitalWrite(BP_NSS, LOW); //enable device

    for (int i=0; i < (int)TxSize; i++) {
        SPI.transfer(pTxData[i]);
    }
    
    digitalWrite(BP_NSS, HIGH);
    SPI.endTransaction();
    return ADI_OK;
    
}

/* blinks once for SPI, twice for I2C, three times for none*/
void get_com_mode() {
  ADI_ADPD_COMM_MODE bus_mode = adi_adpddrv_GetComMode();
  if (bus_mode == E_ADI_ADPD_SPI_BUS) {
    blink_bp(1);
  } else if (bus_mode == E_ADI_ADPD_I2C_BUS) {
    blink_bp(2);
  } else {
    blink_bp(3);
  }

  delay(1000);  
}

