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
    
    if ( c == 'E' ) {
      pingRadio(false);
    } else if ( c == 'A' ) {
      pingRadio(true);
    } else if ( c == 'D' ) {
      distance();
    }
  }
}

void distance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
 
  digitalWrite(trigPin, LOW);
  
  unsigned long duration = pulseIn(echoPin, HIGH);
  unsigned long distance = duration / 58.2;
  
  if ( distance < minDistance || distance > maxDistance ) {
    distance = 0;
  }
  
  Serial.println(distance);
}

void pingRadio(bool ack) {
  radio.stopListening();
  
  unsigned long start_time = millis();
  // This call blocks until the receiver has acknowledged
  bool ok = radio.write( &start_time, sizeof(unsigned long) );
  
  if (!ok) {
    Serial.println(0);
    return;
  }
  
  unsigned long ack_time = millis() - start_time;
  
  radio.startListening();
  
  unsigned long started_waiting_at = millis();
  bool timeout = false;
  while ( !radio.available() && !timeout ) {
    if (millis() - started_waiting_at > timeoutMs ) {
      timeout = true;
    }
  }

  if ( timeout )
  {
    Serial.println(0);
    return;
  }
 
  unsigned long received_time;
  radio.read( &received_time, sizeof(unsigned long) );
  
  unsigned long roundtrip_time = millis() - start_time;
  
  if (ack) {
    Serial.println(ack_time);
  } else {
    Serial.println(roundtrip_time);
  }
}
