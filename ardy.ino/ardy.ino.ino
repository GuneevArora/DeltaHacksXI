#include "Wire.h"
#include "rgb_lcd.h"
#include<string.h>

rgb_lcd lcd;

#define BUTTON_PIN 7

byte wasTouched = LOW;
byte isTouched = LOW;

char password[250] = "Not Viewing Password";
int passLength = 20;
char ipAddress[50] = "No IP Address Ready";
int ipLength = 19;

unsigned long startTime = 0;
unsigned long receiveTime = 0;

int pointer = 0;
int showPassword = 0;

void resetScroll() {
  pointer = 0;
  lcd.clear();
}

void scrollText() {
  lcd.setCursor(0, 0);
  char *text;
  int length;
  if (showPassword == 1) {
    length = passLength;
    text = password;
  } else {
    length = ipLength;
    text = ipAddress;
  }

  if (length < 16) {
    lcd.print(text);
  } else {
    for (int i = pointer; (i < length) && (i - pointer < 16); i++) {
      lcd.print(text[i]);
    }
    for (int i = 0; i < length - pointer; i++) {
      lcd.print(' ');
    }
    pointer++;
    if (pointer > length) {
      pointer = 0;
    }
  }
}

void checkForSerial() {
  if (Serial.available() > 0) {
    String received = Serial.readString();
    int seperatorIndex = received.indexOf(',');
    if (seperatorIndex != -1) {
      memset(password, 0, 250);
      memset(ipAddress, 0, 50);
      received.substring(0, seperatorIndex).toCharArray(ipAddress, 50);
      ipLength = seperatorIndex-1;
      received.substring(seperatorIndex+1).toCharArray(password, 250);
      passLength = received.length() - seperatorIndex;
      lcd.print(password);
    }
    receiveTime = millis();

    resetScroll();
  }
}

void setup() {
  showPassword = 0;

  // put your setup code here, to run once:
  pinMode(BUTTON_PIN, INPUT);
  Serial.begin(115200);
  lcd.begin(16, 2);

  lcd.setRGB(0, 0, 255);
  startTime = millis();

  checkForSerial();
}


void loop() {
  // put your main code here, to run repeatedly:
  checkForSerial();
  isTouched = digitalRead(BUTTON_PIN) == HIGH;
  if (wasTouched != isTouched) {
    lcd.clear();
    if (isTouched == HIGH) {
      showPassword = 1;
    } else {
      showPassword = 0;
    }
    resetScroll();
  }
  wasTouched = isTouched;

  long show_time = (passLength * 2000) -  millis() - receiveTime;
  if (receiveTime == 0 || show_time < 0) {
    memset(password, 0, 250);
    char pbuf[] = "Not Viewing Password";
    for (int i = 0; i < 20; i++) {
      password[i] = pbuf[i];
    }
    show_time = millis() - startTime;
    receiveTime = 0;
  }

  scrollText();

  lcd.setCursor(0, 1);
  lcd.print(show_time / 1000);

  delay(1500);
}
