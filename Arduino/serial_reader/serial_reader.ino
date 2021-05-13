#include <Adafruit_BMP280.h>
#include <SoftwareSerial.h>
#include <XBee.h>
#include "DHT.h"
#define DHTPIN 0
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE); 
SoftwareSerial XBee(1,0); // RX, TX 

struct Transmission {
    private:
        uint8_t _start_byte{0xaa};
        int8_t node_id{1};
    public:
        float temp = 0.0;
        float humidity = 0.0;
        float smoke = 0.0;
        float pressure = 0.0;
        float altitude = 0.0;
        bool flame = false;

    private:
        uint8_t _end_byte{0xee};
};

union u_t {
  Transmission t;
  uint8_t b[sizeof(Transmission)];
};

Adafruit_BMP280 bmp;
u_t transmission{Transmission()};

void setup() {
    Xbee.begin(9600);
    bmp.begin();
    dht.begin();
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
    transmission.t.humidity = dht.readHumidity();
    transmission.t.temp = (bmp.readTemperature());
    transmission.t.pressure = (bmp.readPressure()/1000);
    transmission.t.altitude = (bmp.readAltitude(1019.66));
    transmission.t.smoke = (analogRead(A0));
    transmission.t.flame = (
    Xbee.write(+transmission.b, sizeof(Transmission));
}
