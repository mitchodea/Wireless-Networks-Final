//#include <Adafruit_BMP280.h>

struct Transmission {
    private:
        uint8_t _start_byte{0xaa};
        int8_t node_id{1};
    public:
        int8_t v1 = 0;
        int16_t v2 = 0;
        float v3 = 0.0;
    private:
        uint8_t _end_byte{0xee};
};

union hahalmao {
  Transmission t;
  uint8_t b[sizeof(Transmission)];
};

//Adafruit_BMP280 bmp; // I2C Interface
int potPin = 2;    // select the input pin for the potentiometer

hahalmao transmission{Transmission()};

int8_t test_counter{0};
float test_float{1};

void setup() {
    Serial.begin(9600);
    //bmp.begin();

    /* Default settings from datasheet. */
    // bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
    //                 Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
    //                 Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
    //                 Adafruit_BMP280::FILTER_X16,      /* Filtering. */
    //                 Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
    transmission.t.v1 = ++test_counter;
    test_float *= 1.01;
    transmission.t.v3 = test_float;
    
    Serial.write(+transmission.b, sizeof(Transmission));
    delay(1000);
}
