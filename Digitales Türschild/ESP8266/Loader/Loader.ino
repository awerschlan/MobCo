/**
  ******************************************************************************
  * @file    Loader.h
  * @author  Waveshare Team
  * @version V1.0.0
  * @date    23-January-2018
  * @brief   The main file.
  *          This file provides firmware functions:
  *           + Initialization of Serial Port, SPI pins and server
  *           + Main loop
  *
  ******************************************************************************
  */ 

/* Includes ------------------------------------------------------------------*/
#include "srvr.h" // Server functions

/* Entry point ----------------------------------------------------------------*/
void setup() 
{
    // Serial port initialization
    Serial.begin(115200);
    delay(10);

    // Server initialization
    Srvr__setup();

    // SPI initialization
    pinMode(CS_PIN  , OUTPUT);
    pinMode(RST_PIN , OUTPUT);
    pinMode(DC_PIN  , OUTPUT);
    pinMode(BUSY_PIN,  INPUT); 
    SPI.begin();

    // Initialization is complete
    Serial.print("\r\nOk!\r\n");
}

/* The main loop -------------------------------------------------------------*/
void loop() 
{
    // The server state observation
    Srvr__loop();
}
