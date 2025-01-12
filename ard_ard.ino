#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

#define BUTTON_PIN 7

struct touch { 
   byte wasPressed = LOW; 
   byte isPressed = LOW; 
}; 
touch touch; 

char password[50] = "No data";
char ipAddress[50] = "192.168.1.1";  

unsigned long startTime;  // Variable to store the start time

void setup() { 
   pinMode(BUTTON_PIN, INPUT); 
   Serial.begin(115200); 
   lcd.begin(16, 2);

   // Display IP address immediately at startup
   lcd.setRGB(0, 0, 255); // Set a color for the display
   lcd.print(ipAddress);  // Display IP address immediately
   Serial.println("Displaying IP address");

   // Initialize the start time for the timer
   startTime = millis();  // Record the start time when the program begins

   // Read serial data for password and IP address if available
   if (Serial.available() > 0) {
      String received = Serial.readString();
      int separatorIndex = received.indexOf(',');

      // Optional: Split the received data into password and IP if separated by a comma
      if (separatorIndex != -1) {
          received.substring(0, separatorIndex).toCharArray(password, 50);  // First part is password
          received.substring(separatorIndex + 1).toCharArray(ipAddress, 50);  // Second part is IP address
      }
   }

   delay(1000); // Wait before going to loop()
} 

void loop() { 
   // Check if data is available on the serial port
   if (Serial.available() > 0) {
      String received = Serial.readString();  // Read the incoming data as a string

      // Clear LCD and display new received data (password and IP)
      lcd.clear();

      int separatorIndex = received.indexOf(',');
      if (separatorIndex != -1) {
          received.substring(0, separatorIndex).toCharArray(password, 50);  // First part is password
          received.substring(separatorIndex + 1).toCharArray(ipAddress, 50);  // Second part is IP address
      }
      lcd.print(ipAddress); // Display IP address
      Serial.println("Displaying IP address");
   }
   
   // Button handling logic to toggle between IP and password
   touch.isPressed = isTouchPressed(BUTTON_PIN); 
   if (touch.wasPressed != touch.isPressed) {
       lcd.clear(); // Clear the LCD for new message
       if (touch.isPressed == HIGH) {  
           lcd.print(password); // Display password
           Serial.println("Displaying password");
       } else {
           lcd.print(ipAddress); // Display IP address
           Serial.println("Displaying IP address");
       }
   } 
   touch.wasPressed = touch.isPressed;

   // Calculate the elapsed time from the startTime
   unsigned long elapsedTime = millis() - startTime;  // Elapsed time since program start

   // Display the elapsed time in seconds on the second row of the LCD
   lcd.setCursor(0, 1);
   lcd.print(elapsedTime / 1000);  // Display the elapsed time in seconds

   delay(100); // Short delay to allow smooth LCD updates
} 

bool isTouchPressed(int pin) { 
   return digitalRead(pin) == HIGH; 
}