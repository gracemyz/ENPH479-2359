
#include <SPI.h>
#include "Arduino.h"
#include "../adi-adpd-library/adi_adpd_driver.h"
#include "../adi-adpd-library/adi_adpd_reg.h"
#include "../adi-adpd-library/adi_adpd_ssm.h"
#include "../adi-adpd-library/adpd4000.h"
#include "stdint.h"
// https://github.com/analogdevicesinc/adpd-drivers/blob/master/adpd40xx

tAdiAdpdDcfgInst dcfg_ADPD4000[39] = {
    {0x0009U, 0x0085U}, // set high freq osc to half max frequency?
    {0x000bU, 0x02faU}, // set low freq osc to about 0.75 max
    {0x000fU, 0x0006U}, // use internal oscs. Use GPIO0 for alt clock. Use 1 MHz as low freq and enable it.
    {0x000dU, 0x4E20U}, // low freq osc period set to 20000 (s?)
    {0x0006U, 0x0003U}, // generate interrupt when number of bytes in fifo is more than 3
    {0x0014U, 0x8000U}, // enable drive of the FIFO threshold status on Interrupt X.
    {0x001eU, 0x0000U}, // do not enable interrupt status bytes?
    {0x0020U, 0x0004U}, // input pair in1 and in2 sleep state: in1 connected to vc1, in2 floating
    {0x0021U, 0x0000U}, // input config: all inputs are single ended. vc1 and vc2 set to avdd during sleep
    {0x0022U, 0x0403U}, // slow slew control, med drive control,  gpio3 normal output, gpio2 disabled, gpio1 disabled, gpio0 output inverted,
    {0x0023U, 0x0002U}, // gpio1 output signal select output logic 0. gpio1 interrupt X.
    {0x0024U, 0x0000U}, // gpio 2 and 3 output signal logic 0
    {0x010eU, 0x2000U}, // adc offset
    {0x0110U, 0x0004U}, // data format
};

tAdiAdpdDcfgInst single_integration_config[26] =
    {
        {0x0009U, 0x0085U},              // set high freq osc to half max frequency?
        {0x000bU, 0x02faU},              // set low freq osc to about 0.75 max
        {0x000fU, 0x0006U},              // use internal oscs. Use GPIO0 for alt clock. Use 1 MHz as low freq and enable it.
        {0x000dU, 0x4E20U},              // low freq osc period set to 20000 (s?)
        {0x0006U, 0x0003U},              // generate interrupt when number of bytes in fifo is more than 3
        {0x0014U, 0x8000U},              // enable drive of the FIFO threshold status on Interrupt X.
        {0x001eU, 0x0000U},              // do not enable interrupt status bytes?
        {0x0020U, 0x0004U},              // input pair in1 and in2 sleep state: in1 connected to vc1, in2 floating
        {0x0021U, 0x0000U},              // input config: all inputs are single ended. vc1 and vc2 set to avdd during sleep
        {ADPD4x_REG_TS_CTRL_A, 0x0000U}, // sample type A: default setting 0 for default sampling mode
        {ADPD4x_REG_TS_PATH_A, 0x1DAU},  // signal path selection: TIA, BPF, integrator, and ADC.
        // {ADPD4x_REG_TS_PATH_A, 0x0E6}, // TIA ADC mode
        {ADPD4x_REG_INPUTS_A, 0x0005U},  // 101: IN1 connected to channel 1; IN2 connected to channel 2; all else disconnected
        {ADPD4x_REG_CATHODE_A, 0x5002U}, // precon anode to TIA_VREF, set 250 mV reverse bias across photodiode
        // set TIA_VREF to 1.265 V;
        // set TIA_VREF pulse alternate value also to 1.265 V (no pulses?),
        // set TIA channel 2 gain to 100 kOhm and TIA channel 1 gain also to 100 kOhm
        {ADPD4x_REG_AFE_TRIM_A, 0x03C9U},
        {ADPD4x_REG_LED_POW12_A, 0xAU},    // led settings: led1A to 16 mA
        {ADPD4x_REG_PERIOD_A, 0U},         // TIA is continuously connected to input after precondition. No connection modulation.
        {ADPD4x_REG_LED_PULSE_A, 0x219U},  // led pulse width 2us, first pulse offset 25 us
        {ADPD4x_REG_INTEG_WIDTH_A, 0x3U},  // 3 us integration width, 1 ADC conversion per pulse
        {ADPD4x_REG_INTEG_OFFSET_A, 0x1U}, // integ offset. Example had 0x0206.
        {ADPD4x_REG_COUNTS_A, 0x0101U},    // 105 = 5 pulses, 155=27 pulses?. 1 integration per ADC conversion.
        {0x0022U, 0x0403U},                // slow slew control, med drive control,  gpio3 normal output, gpio2 disabled, gpio1 disabled, gpio0 output inverted,
        {0x0023U, 0x0002U},                // gpio1 output signal select output logic 0. gpio1 interrupt X.
        {0x0024U, 0x0000U},                // gpio 2 and 3 output signal logic 0
        // {0x010eU, 0x2000U}, // adc offset
        {0x0110U, 0x0004U}, // data format: 4 bytes signal data
        {0x0010U, 0x0000U}, // operation mode idle
        {0, 0xFFFFU}        // sentinel for end of loop???
};

uint8_t aFifoDataBuf[MAX_SAMPLES_IN_FIFO];
static tAdiAdpdSSmInst oAdiAppInst;

void setup()
{
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
  digitalWrite(BP_NSS, HIGH); // disable ADPD4000 SPI

  // /* ADPD400x interrupt configuration instance */
  // InterruptIn adpd4x_interrupt(ADPD_INT_PIN);
  // EventFlags adpd4x_int_event;

  adi_adpddrv_OpenDriver();

  uint16_t ret = adi_adpdssm_loadDcfg(single_integration_config, 0xFFU);
  if (ret == ADI_ADPD_SSM_SUCCESS)
  {
    Serial.println("register config successful");
  }
  else
  {
    Serial.println("register config unsuccessful");
  }
  ret = adi_adpdssm_slotinit(&oAdiAppInst);
  if (ret == ADI_ADPD_SSM_SUCCESS)
  {
    Serial.println("slot init successful");
  }
  else
  {
    Serial.println("slot init unsuccessful");
  }

  ret = adi_adpdssm_setOperationMode(E_ADI_ADPD_MODE_SAMPLE);
  if (ret == ADI_ADPD_SSM_SUCCESS)
  {
    Serial.println("op mode successful");
  }
  else
  {
    Serial.println("op mode unsuccessful");
  }
  delay(1000);
}

void loop()
{
  optimize_int_sequence(true);

  // uint16_t nAdpdFifoLevelSize;
  // ADI_ADPD_COMM_MODE bus_mode;
  // uint32_t adpd_ch1 = 0U;
  // uint16_t loop = 0U;
  // static uint32_t tick = 0U;

  // uint16_t offset = 0;

  // while(1) {
  //   /* Wait for FIFO_TH Interrupt, see ADPD400x_ISR
  //   *  Wait forever for event '1', auto clear
  //   */
  //   // adpd4x_int_event.wait_any(1U);
  //   uint32_t nRetValue = 0U;
  //   // Not using ADPD400x auto clear int flag -> need to clear
  //   adi_adpddrv_RegWrite(ADPD4x_REG_INT_STATUS_DATA, 0x8000);
  //   /* Read the size of the data available in the FIFO */
  //   nRetValue = adi_adpdssm_getFifoLvl(&nAdpdFifoLevelSize);
  //   if (nRetValue != ADI_ADPD_DRV_SUCCESS) {
  //     Serial.println("get fifo level error");
  //     continue;
  //   }
  //   /* Read the fifo data available in the FIFO */
  //   nRetValue = adi_adpddrv_ReadFifoData(nAdpdFifoLevelSize, &aFifoDataBuf[0]);
  //   if (nRetValue != ADI_ADPD_DRV_SUCCESS) {
  //       Serial.println("read fifo data error");
  //       continue;
  //   }
  //   loop = 0U;
  //   adpd_ch1 = 0U;
  //   /* Read the data from the FIFO and print them */
  //   while (nAdpdFifoLevelSize != 0u) {

  //       /* Byte swapping is needed to print ADPD data in proper format */
  //       adpd_ch1 = ((aFifoDataBuf[loop] << 8) +
  //                   (aFifoDataBuf[loop + 1]) +
  //                   (aFifoDataBuf[loop + 2] << 24) +
  //                   (aFifoDataBuf[loop + 3] << 16));
  //       // Serial.print(nAdpdFifoLevelSize);
  //       // Serial.print(",");
  //       // Serial.print(tick);

  //       Serial.println(adpd_ch1);

  //       nAdpdFifoLevelSize -= oAdiAppInst.oAdpdSlotInst.nTotalSlotSz;
  //       loop += oAdiAppInst.oAdpdSlotInst.nTotalSlotSz;
  //       tick += 1;
  //   }
  //   // Serial.print(loop);
  //   // Serial.println(" loop");

  // }
  // delay(43200000);
}
