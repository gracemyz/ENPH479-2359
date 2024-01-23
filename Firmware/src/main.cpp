
#include <SPI.h>
#include "Arduino.h"
#include "../adi-adpd-library/adi_adpd_driver.h"
#include "../adi-adpd-library/adi_adpd_reg.h"
#include "../adi-adpd-library/adi_adpd_ssm.h"
#include "../adi-adpd-library/adpd4000.h"
#include "stdint.h" 
// https://github.com/analogdevicesinc/adpd-drivers/blob/master/adpd40xx




void setup() {

  // Set bluepill SPI pins
  pinMode(BP_DATA_OUT, OUTPUT);
  pinMode(BP_DATA_IN, INPUT);
  pinMode(BP_SCK, OUTPUT);
  pinMode(BP_NSS, OUTPUT);

  SPI.setMISO(BP_DATA_IN);
  SPI.setMOSI(BP_DATA_OUT);
  SPI.setSCLK(BP_SCK);
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV128);

  pinMode(BP_LED_BUILTIN, OUTPUT);
  blink_bp(3);
  digitalWrite(BP_NSS, HIGH); //disable ADPD4000 SPI

  

}

/**
 * @brief 
 * @param none
 * @retval none
 */
void loop() {
  
  // read_chip_id();
  uint16_t nAddr = ADPD4x_REG_CHIP_ID;
  uint16_t pnData = 0U;
  adi_adpddrv_RegRead( nAddr,  &pnData);
  blink_bp(3);
  delay(200);
  

}










