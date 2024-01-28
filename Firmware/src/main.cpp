
#include <SPI.h>
#include "Arduino.h"
<<<<<<< HEAD
#include "adi_adpd_driver.h"
#include "adi_adpd_reg.h"
#include "adi_adpd_ssm.h"
#include "adi_adpd_slotops_helper.c"
#include "stdint.h"
// https://github.com/analogdevicesinc/adpd-drivers/blob/master/adpd40xx

/* Bluepill pin values and settings */
#define BP_LED_BUILTIN PC13 // Bluepill built-in LED
#define BP_DATA_OUT PA7     // Bluepill MOSI 1
#define BP_DATA_IN PA6      // Bluepill MISO 1
#define BP_SCK PA5          // Bluepill SCK 1
#define BP_NSS PA4          // Bluepill Chip Select 1
#define BLINK_DUR_ms 500

/* ADPD4000 SPI settings */
#define maxspeed 24000000 // ADPD4000 sclk frequency
#define dataorder MSBFIRST
#define datamode SPI_MODE0 // Check this!!!!

void blink_bp(int num_blinks);
void test_spi();

void setup()
{
  Serial.begin(9600);
  pinMode(BP_LED_BUILTIN, OUTPUT);
  blink_bp(3);
=======
#include "../adi-adpd-library/adi_adpd_driver.h"
#include "../adi-adpd-library/adi_adpd_reg.h"
#include "../adi-adpd-library/adi_adpd_ssm.h"
#include "../adi-adpd-library/adpd4000.h"
#include "stdint.h" 
// https://github.com/analogdevicesinc/adpd-drivers/blob/master/adpd40xx



void setup () {
  Serial.begin(9600);
>>>>>>> 0e5ced9cf88d48b1d9926f797363067f176022a8

  // Set bluepill SPI pins
  pinMode(BP_DATA_OUT, OUTPUT);
  pinMode(BP_DATA_IN, INPUT);
  pinMode(BP_SCK, OUTPUT);
  pinMode(BP_NSS, OUTPUT);

  SPI.setMISO(BP_DATA_IN);
  SPI.setMOSI(BP_DATA_OUT);
  SPI.setSCLK(BP_SCK);
  SPI.begin();
<<<<<<< HEAD
  SPI.setClockDivider(SPI_CLOCK_DIV16);

  digitalWrite(BP_NSS, LOW); // disable ADPD4000 SPI
}

/**
 * @brief Turn LED on for 1 sec and off for 1 sec.
 * @param none
 * @retval none
 */
void loop()
{
  test_spi();
  blink_bp(2);
=======
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

>>>>>>> 0e5ced9cf88d48b1d9926f797363067f176022a8
}
  

<<<<<<< HEAD
/**
 * @brief Blink the bluepill's builtin LED a number of times
 * @param num_blinks
 * @retval none
 */
void blink_bp(int num_blinks)
{
  for (int i = 0; i < num_blinks; i++)
  {
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
void test_spi()
{
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
  uint32_t led_off = ((firsthalf) << 16U) | (uint16_t)0;
  uint32_t buffer;

  int delay_ms = 500;
  SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
  digitalWrite(BP_NSS, LOW); // enable device

  for (int i = 0; i < sizeof(led_values); i++)
  {
    buffer = ((firsthalf) << 16U) | led_values[i];
    SPI.transfer(&buffer, 4);
    delay(delay_ms);
    SPI.transfer(&led_off, 4);
    delay(delay_ms);
  }
  // digitalWrite(BP_NSS, HIGH);
  SPI.endTransaction();
}
=======













>>>>>>> 0e5ced9cf88d48b1d9926f797363067f176022a8
