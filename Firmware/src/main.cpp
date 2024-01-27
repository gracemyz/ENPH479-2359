
#include <SPI.h>
#include "Arduino.h"
#include "../adi-adpd-library/adi_adpd_driver.h"
#include "../adi-adpd-library/adi_adpd_reg.h"
#include "../adi-adpd-library/adi_adpd_ssm.h"
#include "../adi-adpd-library/adpd4000.h"
#include "stdint.h" 
// https://github.com/analogdevicesinc/adpd-drivers/blob/master/adpd40xx



void setup () {
  Serial.begin(9600);

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
  digitalWrite(BP_LED_BUILTIN, LOW);
  // blink_bp(3);
  digitalWrite(BP_NSS, HIGH); //disable ADPD4000 SPI

  tAdiAdpdDcfgInst dcfg_ADPD4000[39] =
  {
    {0x0009U, 0x0085U}, // oscillator
    {0x000bU, 0x02faU},
    {0x000fU, 0x0006U}, // sys ctl
    {0x000dU, 0x4E20U}, // ts freq
    {0x0006U, 0x0003U}, // fifo th
    {0x0014U, 0x8000U}, // int enable
    {0x001eU, 0x0000U}, // fifo status bytes
    {0x0020U, 0x0004U}, // input sleep
    {0x0021U, 0x0000U}, // input cfg
    {0x0022U, 0x0403U}, // gpio cfg
    {0x0023U, 0x0002U}, // gpio1
    {0x0024U, 0x0000U}, // gpio23
    {0x0100U, 0x0000U}, // signal path setup
    {0x0101U, 0x41daU},
    {0x0102U, 0x0005U},
    {0x0103U, 0x5002U},
    {0x0104U, 0x03C9U},
    {0x0105U, 0x000aU}, // led settings
    {0x0107U, 0x0101U}, // num int
    {0x010aU, 0x0003U}, // integ width
    {0x010bU, 0x0206U}, // integ offset
    {0x010eU, 0x2000U}, // adc offset
    {0x0110U, 0x0004U}, // data format
    {0x0010U, 0x0000U} // opmode
  };

  static tAdiAdpdSSmInst oAdiAppInst;

  // // ret = adi_adpdssm_SetLedCurrent(nUId,  nLed, 32U);
  adi_adpddrv_OpenDriver();
  adi_adpdssm_loadDcfg(dcfg_ADPD4000, 0x00U);
  // adi_adpdssm_slotinit(&oAdiAppInst);
  
}

void loop () {
  // test_spi();
  // blink_bp(2);

}
  














