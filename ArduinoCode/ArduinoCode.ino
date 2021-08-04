#include <Servo.h>
#include <string.h>
#include <stdio.h>

Servo servoBottom;
Servo servoTop;
const int MAX_DATA = 10;
char incommingData[MAX_DATA];
int bottomServo = 90;
int topServo = 90;

void setup()
{
    Serial.begin(115200);
    servoBottom.attach(10);
    servoTop.attach(9);
}

void loop()
{
    while (Serial.available() > 1)
    {
        for (size_t i = 0; i < MAX_DATA; i++)
        {
            //Reads incomming data.
            byte ch = Serial.read();
            delay(10);
            if (isDigit(ch) || ch == ',' || ch == '-')
            {
                incommingData[i] = ch;
            }
            else
            {
                incommingData[i] = '\0';
            }
        }

        split(incommingData);
        MoveServo(bottomServo, topServo);

        Serial.print("New angle is: ");
        Serial.print(bottomServo);
        Serial.print(",");
        Serial.println(topServo);
    }
}

char split(char a[])
{
    //Splits the incoming data by ','
    const char s[2] = ",";
    char *token;
    int i = 0;
    int temp[2];

    token = strtok(a, s);
    while (token != NULL)
    {
        temp[i] = atoi(token);
        i++;
        token = strtok(NULL, s);
    }
    if (temp[0] < 999)
    {
        bottomServo = temp[0];
    }
    if (temp[1] < 999)
    {
        topServo = temp[1];
    }
}

void MoveServo(int bottom, int top)
{
    //Runs the servo motors
    if ((bottom >= 0) && (top >= 0) && (bottom <= 180) && (top <= 180))
    {
        servoBottom.write(bottom);
        servoTop.write(top);
    }
    else
    {
        if (bottom < 0 || top < 0)
        {
            Serial.println("Value is to low!");
        }
        if (bottom > 180 || top > 180)
        {
            Serial.println("Value is to high!");
        }
    }
}