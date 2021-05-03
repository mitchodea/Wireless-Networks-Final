#include <SoftwareSerial.h>
#include <DHT.h>
#include <Adafruit_BMP280.h>

#define TEMP_HUM 7

#define FLAME A5
#define AIR_Q A4

#define BMP_SCK 13
#define BMP_MISO 12
#define BMP_MOSI 11 
#define BMP_CS 10

struct Transmission {
    private:
        uint8_t _start_byte{0xaa};
        int8_t node_id{1};
    public:
        float temp = 0.0f;
        float humidity = 0.0f;
        float air_quality = 0.0f;
        float flame = 0.0f;
        float elevation = 0.0f;
        float pressure = 0.0f;

    private:
        uint8_t _end_byte{0xee};
};

union u_t {
  Transmission t;
  uint8_t b[sizeof(Transmission)];
};

DHT tempHum(TEMP_HUM, DHT11);
Adafruit_BMP280 bmp(BMP_CS, BMP_MOSI, BMP_MISO,  BMP_SCK);

u_t transmission{Transmission()};
SoftwareSerial XBee(1, 0);

void setup() {
    XBee.begin(9600);
    tempHum.begin();
    bmp.begin();
}

void loop() {
    transmission.t.temp = tempHum.readTemperature();
    if (isnan(transmission.t.temp)) transmission.t.temp = 0.0f;

    transmission.t.humidity = tempHum.readHumidity();
    if (isnan(transmission.t.humidity)) transmission.t.humidity = 0.0f;

    transmission.t.flame = analogRead(FLAME);
    transmission.t.flame = (
        (transmission.t.flame == 0.0) ? 0.0 : 1.0/transmission.t.flame
    );

    transmission.t.pressure = bmp.readPressure();
    transmission.t.elevation = bmp.readAltitude();

    XBee.write(+transmission.b, sizeof(Transmission));
    delay(1000);
}