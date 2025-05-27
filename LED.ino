#include <FastLED.h>

#define NUM_LEDS 25
#define DATA_PIN 13
#define NUM_CYCLES 3

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<WS2811, DATA_PIN, GRB>(leds, NUM_LEDS);
  pinMode(2, INPUT_PULLUP); // Set up the button pin
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "flash_white_light_3_times") {
      flash_white_light_3_times();
    } else if (command == "LED_cycle_3_times") {
      LED_cycle_3_times();
    } 
  }
}

void flash_white_light_3_times() {
  for (int flash = 0; flash < 3; flash++) {
    leds[0] = CRGB::White; // Turn on the first LED
    FastLED.show();
    delay(500);
    leds[0] = CRGB::Black; // Turn off the first LED
    FastLED.show();
    delay(500);
  }
}

void LED_cycle_3_times() {
  uint8_t hue = 0;
  for (int cycle = 0; cycle < NUM_CYCLES; cycle++) {
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CHSV(hue, 255, 255);
      if (i > 0) leds[i - 1] = CRGB::Black;
      FastLED.show();
      delay(250);
      hue += 5;
    }
    for (int i = NUM_LEDS - 1; i >= 0; i--) {
      leds[i] = CHSV(hue, 255, 255);
      if (i < NUM_LEDS - 1) leds[i + 1] = CRGB::Black;
      FastLED.show();
      delay(250);
      hue += 5;
    }
  }

  // Turn off all the lights
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
  FastLED.show();   
}



