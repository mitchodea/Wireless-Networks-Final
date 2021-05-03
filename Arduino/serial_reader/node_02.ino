#include <SoftwareSerial.h>
#include <DHT.h>

struct Transmission {
    private:
        uint8_t _start_byte{0xaa};
        int8_t node_id{2};
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

const int tempHum_pin{7};
DHT tempHum(tempHum_pin, DHT11);
const int flame_pin{A5};
const int air_q_pin{A4};

u_t transmission{Transmission()};
SoftwareSerial XBee(1, 0);

void setup() {
    XBee.begin(9600);
    tempHum.begin();
}

void loop() {
    transmission.t.temp = tempHum.readTemperature();
    if (isnan(transmission.t.temp)) transmission.t.temp = 0.0f;

    transmission.t.humidity = tempHum.readHumidity();
    if (isnan(transmission.t.humidity)) transmission.t.humidity = 0.0f;

    transmission.t.flame = analogRead(flame_pin);
    transmission.t.air_quality = analogRead(air_q_pin);

    XBee.write(+transmission.b, sizeof(Transmission));
    delay(1000);
}