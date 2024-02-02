
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
  // digitalWrite(BP_LED_BUILTIN, LOW);
  // blink_bp(3);
  digitalWrite(BP_NSS, HIGH); //disable ADPD4000 SPI

  tAdiAdpdDcfgInst single_integration_config[13] =
  {
    {ADPD4x_REG_TS_CTRL_A, 0x0000U}, // sample type A: default setting 0 for default sampling mode
    {ADPD4x_REG_TS_PATH_A, 0x1DAU}, // signal path selection: TIA, BPF, integrator, and ADC.
    {ADPD4x_REG_INPUTS_A, 0x0005U}, // 101: IN1 connected to channel 1; IN2 connected to channel 2; all else disconnected
    {ADPD4x_REG_CATHODE_A, 0x5002U}, // precon anode to TIA_VREF, set 250 mV reverse bias across photodiode
    // set TIA_VREF to 1.265 V;
    // set TIA_VREF pulse alternate value also to 1.265 V (no pulses?), 
    // set TIA channel 2 gain to 100 kOhm and TIA channel 1 gain also to 100 kOhm
    {ADPD4x_REG_AFE_TRIM_A, 0x03C9U}, 
    {ADPD4x_REG_LED_POW12_A, 0xAU}, // led settings: led1A to 16 mA
    {ADPD4x_REG_PERIOD_A, 0U}, // TIA is continuously connected to input after precondition. No connection modulation.
    {ADPD4x_REG_LED_PULSE_A, 0x219U}, // led pulse width 2us, first pulse offset 25 us
    {ADPD4x_REG_INTEG_WIDTH_A, 0x3U}, // 3 us integration width, 1 ADC conversion per pulse 
    {ADPD4x_REG_INTEG_OFFSET_A, 0x0206U}, // integ offset. Needs to be optimzed!
    {ADPD4x_REG_COUNTS_A, 0x0105U}, // 5 pulses. 1 integration per ADC conversion.
    {0x0010U, 0x0000U},
    {0,0xFFFFU} // sentinel for end of loop???
  };

  static tAdiAdpdSSmInst oAdiAppInst;

  // // ret = adi_adpdssm_SetLedCurrent(nUId,  nLed, 32U);
  // adi_adpddrv_OpenDriver(); // probably not needed - for i2c and interrupts?
  // adi_adpdssm_loadDcfg(dcfg_ADPD4000, 0x00U);
  // adi_adpdssm_slotinit(&oAdiAppInst);
  blink_bp(3);
  delay(1000);
  if (adi_adpdssm_loadDcfg(single_integration_config, 0xFFU) == ADI_ADPD_SSM_SUCCESS) {
    blink_bp(1);
  } else {
    blink_bp(2);
  }
  delay(1000);

  if (adi_adpdssm_slotinit(&oAdiAppInst) == ADI_ADPD_SSM_SUCCESS) {
    blink_bp(1);
  } else {
    blink_bp(2);
  }
  delay(1000);
  if (adi_adpdssm_setOperationMode(E_ADI_ADPD_MODE_SAMPLE) == ADI_ADPD_SSM_SUCCESS) {
    blink_bp(1);
  } else {
    blink_bp(2);
  }
  delay(1000);
  
}

void loop () {
  
  // blink_bp(2);

}
  














