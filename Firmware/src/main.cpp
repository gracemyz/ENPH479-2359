
#include <SPI.h>
#include "Arduino.h"
// #include "adi_adpd_driver.h"
// #include "adi_adpd_reg.h"
// #include "adi_adpd_ssm.h"
// #include "adi_adpd_slotops_helper.c"
// #include "stdint.h" 
// // https://github.com/analogdevicesinc/adpd-drivers/blob/master/adpd40xx


/* arduino */
#define BP_LED_BUILTIN PB5
#define BP_DATA_OUT 11 // Bluepill MOSI 2
#define BP_DATA_IN 12  // Bluepill MISO 2
#define BP_SCK 13 // Bluepill SCK 2
#define BP_NSS 10 // Bluepill Chip Select 2
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
  Serial.begin(9600);
  delay(1000);
  pinMode(BP_LED_BUILTIN, OUTPUT);
  blink_bp(3);

  // Set bluepill SPI pins
  pinMode(BP_DATA_OUT, OUTPUT);
  pinMode(BP_DATA_IN, INPUT);
  pinMode(BP_SCK, OUTPUT);
  pinMode(BP_NSS, OUTPUT);

  // SPI.setMISO(BP_DATA_IN);
  // SPI.setMOSI(BP_DATA_OUT);
  // SPI.setSCLK(BP_SCK);
  // SPI.setSSEL(BP_NSS);
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV128);

  digitalWrite(BP_NSS, HIGH); //disable ADPD4000 SPI

  

}

/**
 * @brief Turn LED on for 1 sec and off for 1 sec.
 * @param none
 * @retval none
 */
void loop() {
  
  
  SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
  digitalWrite(BP_NSS, LOW);
  delay(100);
  uint16_t buffer = ((0x0008u) << 1U) & 0xFFFEu; 
  SPI.transfer16(buffer);
  SPI.transfer16(0x00);
  digitalWrite(BP_NSS, HIGH);
  delay(100);
  SPI.endTransaction();
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









#include <SPI.h>
#include "Arduino.h"
// #include "adi_adpd_driver.h"
// #include "adi_adpd_reg.h"
// #include "adi_adpd_ssm.h"
// #include "adi_adpd_slotops_helper.c"
// #include "stdint.h" 
// // https://github.com/analogdevicesinc/adpd-drivers/blob/master/adpd40xx


/* arduino */
#define BP_LED_BUILTIN PB5
#define BP_DATA_OUT 11 // Bluepill MOSI 2
#define BP_DATA_IN 12  // Bluepill MISO 2
#define BP_SCK 13 // Bluepill SCK 2
#define BP_NSS 10 // Bluepill Chip Select 2
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
  Serial.begin(9600);
  delay(1000);
  pinMode(BP_LED_BUILTIN, OUTPUT);
  blink_bp(3);

  // Set bluepill SPI pins
  pinMode(BP_DATA_OUT, OUTPUT);
  pinMode(BP_DATA_IN, INPUT);
  pinMode(BP_SCK, OUTPUT);
  pinMode(BP_NSS, OUTPUT);

  // SPI.setMISO(BP_DATA_IN);
  // SPI.setMOSI(BP_DATA_OUT);
  // SPI.setSCLK(BP_SCK);
  // SPI.setSSEL(BP_NSS);
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV128);

  digitalWrite(BP_NSS, HIGH); //disable ADPD4000 SPI

  

}

/**
 * @brief Turn LED on for 1 sec and off for 1 sec.
 * @param none
 * @retval none
 */
void loop() {
  
  
  SPI.beginTransaction(SPISettings(maxspeed, dataorder, datamode));
  digitalWrite(BP_NSS, LOW);
  delay(100);
  uint16_t buffer = ((0x0008u) << 1U) & 0xFFFEu; 
  SPI.transfer16(buffer);
  SPI.transfer16(0x00);
  digitalWrite(BP_NSS, HIGH);
  delay(100);
  SPI.endTransaction();
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








