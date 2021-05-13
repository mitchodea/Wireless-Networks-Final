#include <SoftwareSerial.h>
#include <DHT.h>

struct Transmission {
    private:
        uint8_t _start_byte{0xaa};
        int8_t node_id{3};
    public:
        float temp = 0.0;
        float humidity = 0.0;
        float air_quality = 0.0;
        float flame = 0.0;
        float elevation = 0.0;
        float pressure = 0.0;

    private:
        uint8_t _end_byte{0xee};
};

union u_t {
  Transmission t;
  uint8_t b[sizeof(Transmission)];
};

const int tempHum_pin{7};
DHT tempHum(tempHum_pin, DHT11);

u_t transmission{Transmission()};
SoftwareSerial XBee(1, 0);

void setup() {
    XBee.begin(9600);
    tempHum.begin();
}

void loop() {
    transmission.t.temp = tempHum.readTemperature();
    transmission.t.humidity = tempHum.readHumidity();
    XBee.write(+transmission.b, sizeof(Transmission));
    delay(1000);
}