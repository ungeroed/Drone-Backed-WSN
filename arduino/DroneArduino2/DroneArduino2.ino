#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

// Ultrasonic settings
#define echoPin 7
#define trigPin 8

#define maxDistance 200
#define minDistance 10

// Radio settings
#define timeoutMs 150
RF24 radio(9,10);
const uint64_t pipes[2] = { 0xF0F0F0F0E1LL, 0xF0F0F0F0D2LL };

void setup(void)
{
  Serial.begin(9600);
  
  // Ultrasonic setup
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Radio setup
  radio.begin();
  radio.setRetries(15,15);
  
  radio.openWritingPipe(pipes[0]);
  radio.openReadingPipe(1,pipes[1]);
}

void loop(void)
{
  if ( Serial.available() )
  {
    char c = toupper(Serial.read());
    
    if ( c == 'A' ) {
      pingRadio();
    }
  }
}

void pingRadio() {
  radio.stopListening();
  
  unsigned long start_time = millis();
  // This call blocks until the receiver has acknowledged
  bool ok = radio.write( &start_time, sizeof(unsigned long) );
  
  if (!ok) {
    Serial.println(0);
    return;
  }
  
  unsigned long ack_time = millis() - start_time;
  Serial.println(ack_time);
  
  radio.startListening();
}
