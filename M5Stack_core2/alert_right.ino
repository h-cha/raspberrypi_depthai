#include <M5Core2.h>
#include "BluetoothSerial.h"


BluetoothSerial bts;

const double PWM_Hz = 2000;   // PWM周波数
const uint8_t PWM_level = 8; // PWM分解能 16bit(1～256)
const uint8_t PWM_CH = 1;  // チャンネル
const int motor_pin = 32;

void setup() {
  M5.begin();
  M5.Lcd.println("Bluetooth Now right");

  Serial.begin(9600);
  bts.begin("M5Stack RIGHT");//PC側で確認するときの名前

  // vibration setting
  pinMode(motor_pin, OUTPUT);

  // チャンネルと周波数の分解能を設定
  ledcSetup(PWM_CH, PWM_Hz, PWM_level);
  // モータのピンとチャンネルの設定
  ledcAttachPin(motor_pin, PWM_CH);
}

String btsRead() {
  String receiveData = "";
  if (bts.available()) {
    receiveData = bts.readStringUntil(';');
    M5.Lcd.println(receiveData);
    // Serial.printf( "rx : %02X\n", bts.read());
    // bts.print("sendOK");
  }
  return receiveData;
}

void vibration(String message) {
  if (message == "right")
  {
    // デューティー比0.25(64/256)でPWM制御
    ledcWrite(PWM_CH, 64);
    M5.Lcd.println("close");
  }
  else
  {
    // ストップ
    ledcWrite(PWM_CH, 0);
    M5.Lcd.println("stop");
  }
}

void loop() {
  btsRead();

//   vibration(btsRead());

  //delay(1000);
}