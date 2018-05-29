/**
  ******************************************************************************
  * @file    edp2in13.h
  * @author  Waveshare Team
  * @version V1.0.0
  * @date    23-January-2018
  * @brief   This file describes initialisation of 2.13 and 2.13b e-Papers
  *
  ******************************************************************************
  */
unsigned char lut_full_2in13[] =
{
    0x22, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x11, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 
    0x01, 0x00, 0x00, 0x00, 0x00, 0x00
};

char lut_partial_2in13[] =
{
    0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x0F, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

int EPD_Init_2in13() 
{
    EPD_Reset();
    EPD_Send_3(0x01, 249, 0, 0);//DRIVER_OUTPUT_CONTROL: LO(h-1), HI(h-1), GD = 0; SM = 0; TB = 0;
    EPD_Send_3(0x0C, 0xD7, 0xD6, 0x9D);//BOOSTER_SOFT_START_CONTROL
    EPD_Send_1(0x2C, 0xA8);//WRITE_VCOM_REGISTER: VCOM 7C
    EPD_Send_1(0x3A, 0x1A);//SET_DUMMY_LINE_PERIOD: 4 dummy lines per gate
    EPD_Send_1(0x3B, 0x08);//SET_GATE_TIME: 2us per line
    EPD_Send_1(0x11, 0x03);//DATA_ENTRY_MODE_SETTING: X increment; Y increment

    EPD_lut(0x32, 30, &lut_full_2in13[0]);
    return 0;
}

int EPD_Init_2in13b() 
{
    EPD_Reset();
    EPD_Send_3(0x06, 0x17, 0x17, 0x17);//BOOSTER_SOFT_START
    EPD_SendCommand(0x04);//POWER_ON
    EPD_WaitUntilIdle();
    
    EPD_Send_1(0x00, 0x8F);//PANEL_SETTING
    EPD_Send_1(0x50, 0x37);//VCOM_AND_DATA_INTERVAL_SETTING
    EPD_Send_3(0x61, 0x68, 0, 0xD4);//TCON_RESOLUTION

    EPD_SendCommand(0x10);//DATA_START_TRANSMISSION_1  
    delay(2);
    return 0;
}
