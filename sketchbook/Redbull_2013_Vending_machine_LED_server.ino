#include <Adafruit_NeoPixel.h>

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_RGB     Pixels are wired for RGB bitstream
//   NEO_GRB     Pixels are wired for GRB bitstream
//   NEO_KHZ400  400 KHz bitstream (e.g. FLORA pixels)
//   NEO_KHZ800  800 KHz bitstream (e.g. High Density LED strip)

const int LED_STRIP_LENGTH = 140;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_STRIP_LENGTH, 6, NEO_GRB + NEO_KHZ800);

const int SECONDS = 1000;

byte current_mode = 0;
const byte ANSWER_WRONG_MODE   = 'w';
const byte ANSWER_CORRECT_MODE = 'c';
const byte ATTRACT_MODE        = 'a';
const byte COUNTDOWN_MODE      = 'd';
const byte PULSE_MODE          = 'p';

const uint32_t BLACK = strip.Color(0, 0, 0);
const uint32_t RED   = strip.Color(255, 0, 0);
const uint32_t GREEN = strip.Color(0, 255, 0);
const uint32_t BLUE  = strip.Color(0, 0, 255);

void setup() 
{
  Serial.begin(9600);

  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  current_mode = ATTRACT_MODE;
  attract_init();
}

void loop()
{
  parse_input();
  
  switch (current_mode) {
    case (COUNTDOWN_MODE):
      countdown_update();
      break;

    case (PULSE_MODE):
      pulse_update();
      break;

    case (ATTRACT_MODE):
      attract_update();
      break;      
  }
}

void show_message(char * message)
{
  static int count = 0;

  if (strlen(message) > 0) {
    Serial.println(message);
    count = 0;
  } else {
    count ++;
    //
    //  print a "+" every 5 seconds 
    //
    if (count > 50) {
      Serial.print("+");
      count = 0;
    }
  }
  delay(100);  // one tenth of a second
}


void parse_input()
{ 
  byte inByte;

  while (Serial.available()) {
    inByte = Serial.read();
    switch (inByte) {
      case (ATTRACT_MODE):
//        show_message("Entering attract mode");
        current_mode = inByte;
        attract_init();
        break;

      case (COUNTDOWN_MODE):
//        show_message("Entering countdown mode");
        countdown_init(10);
        current_mode = inByte;
        break;

      case (ANSWER_WRONG_MODE):
        show_message("Entering wrong answer mode");
        current_mode = PULSE_MODE;
        pulse_init(1, 0, 0, 10);
        break;

      case (ANSWER_CORRECT_MODE):
//        show_message("Entering correct answer mode");
        current_mode = PULSE_MODE;
        pulse_init(0, 0, 1, 10);
        break;

//      default:
//        show_message("Invalid comm");
    }
  }
}

// *****************************************************************************
//
// attract mode
//
// *****************************************************************************


uint16_t rainbow_color_index = 0;

void attract_init()
{
  rainbow_color_index = 0;
}

void attract_update()
{
  rainbow(100);
}

void rainbow(uint8_t wait)
{
  uint16_t i;

  if (rainbow_color_index > 255) {
    rainbow_color_index = 0;
  } else {
    rainbow_color_index += 1;
  }
  
  for (i=0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, Wheel((i + rainbow_color_index) & 255));
  }
  strip.show();

  delay(wait);
}

//
// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
//
uint32_t Wheel(byte WheelPos)
{
  if (WheelPos < 85) {
   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if (WheelPos < 170) {
   WheelPos -= 85;
   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}


// *****************************************************************************
//
//  Countdown
//
// *****************************************************************************

unsigned long countdown_start_time = 0;
unsigned long countdown_end_time = 0;

void countdown_init(int seconds)
{
  for (int led_index = 0; led_index < LED_STRIP_LENGTH; led_index ++) {
    strip.setPixelColor(led_index, RED);
  }

//  do {
    countdown_start_time = millis();
    countdown_end_time = countdown_start_time + seconds * 1000;
//  } while (countdown_start_time > countdown_end_time);

//  Serial.println("Setting countdown variables:");
  
//  Serial.print("seconds ");
//  Serial.println(seconds);
//  Serial.print("countdown_start_time ");
//  Serial.println(countdown_start_time);
//  Serial.print("countdown_end_time ");
//  Serial.println(countdown_end_time);

  strip.show();
}

void countdown_update()
{
  int leds_lit = map(millis(), countdown_start_time, countdown_end_time, LED_STRIP_LENGTH, 0);

  if (leds_lit > 0) {
    for (int led_index = 0; led_index < LED_STRIP_LENGTH; led_index ++) {
      strip.setPixelColor(led_index, strip.Color((led_index < leds_lit ? 255 : 0), 0, 0));
    }
  } else {
    //
    // wrong answer mode
    //
    current_mode = PULSE_MODE;
    pulse_init(1, 0, 0, 10);
  }
  strip.show();
}

// *****************************************************************************
//
// pulse
//
// *****************************************************************************

int pulse_direction_red   = 0;
int pulse_direction_green = 0;
int pulse_direction_blue  = 0;
int pulse_current_red   = 0;
int pulse_current_green = 0;
int pulse_current_blue  = 0;
int pulse_wait      = 0;

void pulse_init(int red, int blue, int green, int wait)
{
  pulse_direction_red   = red;
  pulse_direction_green = green;
  pulse_direction_blue  = blue;

  pulse_current_red     = 0;
  pulse_current_green   = 0;
  pulse_current_blue    = 0;

  pulse_wait = wait;

  for (int led_position = 0; led_position < strip.numPixels(); led_position++) {
      strip.setPixelColor(led_position, BLACK);
  }
  strip.show();
}

void pulse_update()
{
  pulse_increment();
  if (pulse_color_out_of_range()) {
    pulse_reverse();
    pulse_increment();
    pulse_increment();
  }
  for (int led_position = 0; led_position < strip.numPixels(); led_position++) {
    strip.setPixelColor(led_position, strip.Color(pulse_current_red, pulse_current_green, pulse_current_blue));
  }
  strip.show();
}

void pulse_increment()
{
  pulse_current_red   += pulse_direction_red;
  pulse_current_green += pulse_direction_green;
  pulse_current_blue  += pulse_direction_blue;
}

void pulse_reverse()
{
  pulse_direction_red   = -pulse_direction_red;
  pulse_direction_green = -pulse_direction_green;
  pulse_direction_blue  = -pulse_direction_blue;
}

int pulse_color_out_of_range()
{
  return (
    pulse_current_red   < 0 || pulse_current_red   > 255 || 
    pulse_current_green < 0 || pulse_current_green > 255 || 
    pulse_current_blue  < 0 || pulse_current_blue  > 255);
}

// *****************************************************************************
//
// Fill the dots one after the other with a color
//
// *****************************************************************************

void colorWipe(uint32_t color, uint8_t wait)
{
  for (int led_position = 0; led_position < strip.numPixels(); led_position++) {
    strip.setPixelColor(led_position, color);
    strip.show();
    delay(wait);
  }
}

/*
// *****************************************************************************
//
//  Chase
//
// worked for the Red Bull sheild
// *****************************************************************************
int Chase_Red   = 0,  Chase_Red_Direction   = 0;
int Chase_Blue  = 0,  Chase_Blue_Direction  = 0;
int Chase_Green = 0,  Chase_Green_Direction = 0;

void set_initial_comet_chase()
{
  if (Chase_Red == 0 and Chase_Green == 0 and Chase_Blue == 0) {
    switch (random(1, 3)) {
      case 1:
        Chase_Red = 255;
        Chase_Red_Direction = -1;
        if (random(1, 2) == 2) {
          Chase_Green_Direction = 1;
        } else {
          Chase_Blue_Direction = 1;
        }
        break;
               
      case 2:
        Chase_Green = 255;
        Chase_Green_Direction = -1;
        if (random(1, 2) == 2) {
          Chase_Red_Direction = 1;
        } else {
          Chase_Blue_Direction = 1;
        }
        break;

      case 3:
        Chase_Blue = 255;
        Chase_Blue_Direction = -1;
        if (random(1, 2) == 2) {
          Chase_Red_Direction = 1;
        } else {
          Chase_Green_Direction = 1;
        }
        break;
    }
  }
  update_comet_chase_color();
}

void update_comet_chase_color()
{
  Chase_Red += Chase_Red_Direction;
  Chase_Blue += Chase_Blue_Direction;
  Chase_Green += Chase_Green_Direction;

  if (Chase_Red <= 0 or Chase_Blue <= 0 or Chase_Green <= 0) {
    switch (random(1, 3)) {
      case 1:
        Chase_Red_Direction = -Chase_Red_Direction;
        if (Chase_Red_Direction == 0
          Chase_Red_Direction = (Chase_Red > 127) ? -1 : 1;
        }
        break;
               
      case 2:
        Chase_Green_Direction = -Chase_Green_Direction;
        if (Chase_Green_Direction == 0) {
          Chase_Green_Direction = (Chase_Green > 127) ? -1 : 1;
        }
        break;

      case 3:
        Chase_Blue_Direction = -Chase_Blue_Direction;
        if (Chase_Blue_Direction == 0) {
          Chase_Blue_Direction = (Chase_Blue > 127) ? -1 : 1;
        }
        break;
    }
  }
}
*/
