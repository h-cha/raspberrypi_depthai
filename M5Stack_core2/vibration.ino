#include <M5Core2.h>

const double PWM_Hz = 2000;   // PWM周波数
const uint8_t PWM_level = 8; // PWM分解能 16bit(1～256)
const uint8_t PWM_CH = 1;  // チャンネル
const int motor_pin = 32;

void setup() {
  M5.begin();

  pinMode(motor_pin, OUTPUT); 

  // チャンネルと周波数の分解能を設定
  ledcSetup(PWM_CH, PWM_Hz, PWM_level);
  // モータのピンとチャンネルの設定
  ledcAttachPin(motor_pin, PWM_CH);
}

void loop() {
  M5.update();

  if (M5.BtnA.wasPressed())
  {
    // デューティー比0.25(64/256)でPWM制御
    ledcWrite(PWM_CH,64);
      M5.Lcd.println("A");
  }
  else if (M5.BtnC.wasPressed())
  {
    // ストップ
    ledcWrite(PWM_CH,0);
      M5.Lcd.println("C");
  }

  delay(10); 
}
