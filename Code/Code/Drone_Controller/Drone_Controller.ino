#include "global.h"
#include "SER.h"
//Choose either pin 2 or pin 3 because they are interrupt pins. On other boards you can use any pin that has an interrupt
#define OUTPUT_PIN 3 
#define RC_CHANNEL_MIN 990
#define RC_CHANNEL_MAX 2010

#define SBUS_MIN_OFFSET 173
#define SBUS_MID_OFFSET 992
#define SBUS_MAX_OFFSET 1811
#define SBUS_CHANNEL_NUMBER 16
#define SBUS_PACKET_LENGTH 25
#define SBUS_FRAME_HEADER 0x0f
#define SBUS_FRAME_FOOTER 0x00
#define SBUS_FRAME_FOOTER_V2 0x04
#define SBUS_STATE_FAILSAFE 0x08
#define SBUS_STATE_SIGNALLOSS 0x04
#define SBUS_UPDATE_RATE 15 //ms
int ch0 = 1500 , ch1 = 1500 , ch2 = 900, ch3 =1500, ch4 = 900, ch5 = 900, ch6 = 900;
long duration, distance;
int EchoMid = 9; // Ultrasonic sensor Echo pin
int TrigMid = 10;  // Ultrasonic sensor Trigger pin
void sbusPreparePacket(uint8_t packet[], int channels[], bool isSignalLoss, bool isFailsafe){

    static int output[SBUS_CHANNEL_NUMBER] = {0};

    /*
     * Map 1000-2000 with middle at 1500 chanel values to
     * 173-1811 with middle at 992 S.BUS protocol requires
     */
    for (uint8_t i = 0; i < SBUS_CHANNEL_NUMBER; i++) {
        output[i] = map(channels[i], RC_CHANNEL_MIN, RC_CHANNEL_MAX, SBUS_MIN_OFFSET, SBUS_MAX_OFFSET);
    }

    uint8_t stateByte = 0x00;
    if (isSignalLoss) {
        stateByte |= SBUS_STATE_SIGNALLOSS;
    }
    if (isFailsafe) {
        stateByte |= SBUS_STATE_FAILSAFE;
    }
    packet[0] = SBUS_FRAME_HEADER; //Header

    packet[1] = (uint8_t) (output[0] & 0x07FF);
    packet[2] = (uint8_t) ((output[0] & 0x07FF)>>8 | (output[1] & 0x07FF)<<3);
    packet[3] = (uint8_t) ((output[1] & 0x07FF)>>5 | (output[2] & 0x07FF)<<6);
    packet[4] = (uint8_t) ((output[2] & 0x07FF)>>2);
    packet[5] = (uint8_t) ((output[2] & 0x07FF)>>10 | (output[3] & 0x07FF)<<1);
    packet[6] = (uint8_t) ((output[3] & 0x07FF)>>7 | (output[4] & 0x07FF)<<4);
    packet[7] = (uint8_t) ((output[4] & 0x07FF)>>4 | (output[5] & 0x07FF)<<7);
    packet[8] = (uint8_t) ((output[5] & 0x07FF)>>1);
    packet[9] = (uint8_t) ((output[5] & 0x07FF)>>9 | (output[6] & 0x07FF)<<2);
    packet[10] = (uint8_t) ((output[6] & 0x07FF)>>6 | (output[7] & 0x07FF)<<5);
    packet[11] = (uint8_t) ((output[7] & 0x07FF)>>3);
    packet[12] = (uint8_t) ((output[8] & 0x07FF));
    packet[13] = (uint8_t) ((output[8] & 0x07FF)>>8 | (output[9] & 0x07FF)<<3);
    packet[14] = (uint8_t) ((output[9] & 0x07FF)>>5 | (output[10] & 0x07FF)<<6);  
    packet[15] = (uint8_t) ((output[10] & 0x07FF)>>2);
    packet[16] = (uint8_t) ((output[10] & 0x07FF)>>10 | (output[11] & 0x07FF)<<1);
    packet[17] = (uint8_t) ((output[11] & 0x07FF)>>7 | (output[12] & 0x07FF)<<4);
    packet[18] = (uint8_t) ((output[12] & 0x07FF)>>4 | (output[13] & 0x07FF)<<7);
    packet[19] = (uint8_t) ((output[13] & 0x07FF)>>1);
    packet[20] = (uint8_t) ((output[13] & 0x07FF)>>9 | (output[14] & 0x07FF)<<2);
    packet[21] = (uint8_t) ((output[14] & 0x07FF)>>6 | (output[15] & 0x07FF)<<5);
    packet[22] = (uint8_t) ((output[15] & 0x07FF)>>3);

    packet[23] = stateByte; //Flags byte
    packet[24] = SBUS_FRAME_FOOTER; //Footer
}

uint8_t sbusPacket[SBUS_PACKET_LENGTH];
int rcChannels[SBUS_CHANNEL_NUMBER];
uint32_t sbusTime = 0;



void setup() {
    rcChannels[0] = 1500;// Roll
    rcChannels[1] = 1500;// Pitch
    rcChannels[2] = 900; //Throttle
    rcChannels[3] = 1500; // Yaw
    rcChannels[4] = 900; // Aux1
    rcChannels[5] = 900; // Aux2
    rcChannels[6] = 900; // Aux2
    Serial.begin(100000, SERIAL_8E2);
    pinMode(TrigMid, OUTPUT);
    pinMode(EchoMid, INPUT);
}

void loop() {
    uint32_t currentMillis = millis();
      ser.begin();
      
      digitalWrite(TrigMid, 0);
      delayMicroseconds(2);   
      digitalWrite(TrigMid, 1);  // Send ultrasonic pulse
      delayMicroseconds(10);
      digitalWrite(TrigMid, 0);

      duration = pulseIn(EchoMid, 1); // Receive reflected pulse
      distance = duration * 0.034 / 2;   // Convert to distance in cm
    if(distance <100 ) { 
      rcChannels[0] = 1500;// Roll
      rcChannels[1] = 1500;// Pitch
      rcChannels[2] = 1500; //Throttle
      rcChannels[3] = 1500; // Yaw
      rcChannels[4] = 1850; // Aux1
      rcChannels[5] = 1100; // Aux2
      rcChannels[6] = 2000; // OB
    }
    else {
      rcChannels[0] = ch0;// Roll
      rcChannels[1] = ch1;// Pitch
      rcChannels[2] = ch2; //Throttle
      rcChannels[3] = ch3; // Yaw
      rcChannels[4] = ch4; // Aux1
      rcChannels[5] = ch5; // Aux2
      rcChannels[6] = 1000; // OB
    }
    if (currentMillis > sbusTime) {
        sbusPreparePacket(sbusPacket, rcChannels, false, false);
        Serial.write(sbusPacket, SBUS_PACKET_LENGTH);

        sbusTime = currentMillis + SBUS_UPDATE_RATE;
    }

     
      
      // If an obstacle is detected within 25 cm, stop the drone
      if (distance < 100) {
        Serial.println("Obstacle detected!");
      // delay(10);
      // hover(); 
      } else {
        Serial.println("Continue ");
      }
}