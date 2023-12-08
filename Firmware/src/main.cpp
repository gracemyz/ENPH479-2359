
#include <SPI.h>
#include "Arduino.h"
#include "adi_adpd_driver.h"
#include "adi_adpd_reg.h"
#include "adi_adpd_ssm.h"
#include "adi_adpd_slotops_helper.c"
#include "stdint.h" 
// https://github.com/analogdevicesinc/adpd-drivers/blob/master/adpd40xx

/* Bluepill pin values and settings */
#define BP_LED_BUILTIN PC13 // Bluepill built-in LED
#define BP_DATA_OUT PA7 // Bluepill MOSI 1
#define BP_DATA_IN PA6 // Bluepill MISO 1
#define BP_SCK PA6 // Bluepill SCK 1
#define BP_NSS PA5 // Bluepill Chip Select 1
#define BLINK_DUR_ms 500

/* ADPD4000 SPI settings */
#define maxspeed 24000000 // ADPD4000 sclk frequency
#define dataorder MSBFIRST
#define datamode SPI_MODE0 // Check this!!!!

void blink_bp(int num_blinks);
void test_spi();

void setup() {
  Serial.begin(9600);
  pinMode(BP_LED_BUILTIN, OUTPUT);
  blink_bp(3);

  // Set bluepill SPI pins
  pinMode(BP_DATA_OUT, OUTPUT);
  pinMode(BP_DATA_IN, INPUT);
  pinMode(BP_SCK, OUTPUT);
  pinMode(BP_NSS, OUTPUT);

  digitalWrite(BP_NSS, HIGH); //disable ADPD4000 SPI

  test_spi();
  blink_bp(3);

}

/**
 * @brief Turn LED on for 1 sec and off for 1 sec.
 * @param none
 * @retval none
 */
void loop() {
}

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


  uint16_t ledRegAddress = ADPD4x_REG_LED_POW12_A; // timing slot A, I think

  // hardcoded lol. see adi_adpd_slotops_helper for a more flexible function 
  // in order: LED1A 50mA, LED1A 100mA, LED1B 50mA, LED1B 100mA
  uint16_t led_values[4] = {32U, 64U, 160U, 192U};

  // uint16_t led1A_50mA = 32U;
  // uint16_t led1A_100mA = 64U;
  // uint16_t led1B_50mA = 160U;
  // uint16_t led1B_100mA = 192U;

  uint16_t firsthalf = ((ledRegAddress) << 1U) | ADPD400x_SPI_WRITE;
  uint32_t led_off = ((firsthalf) << 16U) | (uint16_t) 0;
  uint32_t buffer;
  
  int delay_ms = 500;
  SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
  digitalWrite(BP_NSS, LOW); //enable device

  for (int i = 0; i < 4; i++) {
    buffer = ((firsthalf) << 16U) | led_values[i];
    SPI.transfer(buffer, 32);
    delay(delay_ms);
    SPI.transfer(led_off, 32);
    delay(delay_ms);
  }
  digitalWrite(BP_NSS, HIGH);
  SPI.endTransaction();

}




