// SerialO.h
#ifndef SER_h
#define SER_h

#include <Arduino.h>

class SER {
public:
    void begin();
    void FCComands(); // Function to retrieve the command

private:
    byte character = 0;
    String cmd = "";
    int cmdrdy = 0;
};
extern SER ser;
#endif