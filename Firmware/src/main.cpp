
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
#define BP_SCK PA5 // Bluepill SCK 1
#define BP_NSS PA4 // Bluepill Chip Select 1

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
#define datamode SPI_MODE0 // Check this!!!!

//  #include <iostream> 
// using namespace std;

void blink_bp(int num_blinks);
void test_spi();
void read_chip_id();

void setup() {

  // Set bluepill SPI pins
  pinMode(BP_DATA_OUT, OUTPUT);
  pinMode(BP_DATA_IN, INPUT);
  pinMode(BP_SCK, OUTPUT);
  pinMode(BP_NSS, OUTPUT);

  SPI.setMISO(BP_DATA_IN);
  SPI.setMOSI(BP_DATA_OUT);
  SPI.setSCLK(BP_SCK);
  SPI.setSSEL(BP_NSS);
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
  
  read_chip_id();
  blink_bp(2);
  delay(1000);
  

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
  delay(100);
  uint16_t buffer = ((ADPD4x_REG_CHIP_ID) << 1U) & ADPD400x_SPI_READ; 
  SPI.transfer16(buffer);
  SPI.transfer16(0x00);
  digitalWrite(BP_NSS, HIGH);
  delay(100);
  SPI.endTransaction();

}

void read_chip_id_library() {
  uint16_t addr = ADPD4x_REG_CHIP_ID;
  uint16_t pData = 0U;

  adi_adpddrv_RegRead(addr, &pData);
}






