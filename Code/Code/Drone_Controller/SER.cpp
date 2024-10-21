// Serial.cpp
#include "SER.h"
#include "global.h"
SER ser;

static int index = 0; // Index for storing numbers
static String inputString = "";
void SER::begin() {
    // Define variables for storing the received numbers




  static int index = 0; // Index for storing numbers
  static String inputString = ""; // Store the incoming string

  // Check if data is available
  while (Serial.available() > 0) {
    char incomingChar = Serial.read(); // Read a character

    // If a newline character is received, process the input
    if (incomingChar == '\n') {
      if (inputString.length() > 0) {
        // Convert the string to an integer and store it in the appropriate variable
        switch (index) {
          case 0: ch0 = inputString.toInt(); break;
          case 1: ch1 = inputString.toInt(); break;
          case 2: ch2 = inputString.toInt(); break;
          case 3: ch3 = inputString.toInt(); break;
          case 4: ch4 = inputString.toInt(); break;
          case 5: ch5 = inputString.toInt(); break;
          case 6: ch6 = inputString.toInt(); break;
        }

        index++; // Move to the next variable

        // Reset the input string for the next number
        inputString = "";

        // If we have received all numbers, print them
        if (index >= 7) {
          Serial.println("Received numbers:");
          Serial.print("ch0: "); Serial.println(ch0);
          Serial.print("ch1: "); Serial.println(ch1);
          Serial.print("ch2: "); Serial.println(ch2);
          Serial.print("ch3: "); Serial.println(ch3);
          Serial.print("ch4: "); Serial.println(ch4);
          Serial.print("ch5: "); Serial.println(ch5);
          Serial.print("ch6: "); Serial.println(ch6);
          
          // Reset index for next batch
          index = 0;
        }
      }
    } else {
      inputString += incomingChar; // Append the character to the input string
    }
  }
}             
