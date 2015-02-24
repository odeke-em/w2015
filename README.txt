Author: Emmanuel Odeke
Section: LBL EBL2 W-F

Way finding:
============

Implementing the way finding project that entails client to server communication
over a serial port from an Arduino to a port opener running on a native machine.


Wiring:
    + Following the wiring provided in client_soln_base_part2 which when
      re-iterated is:
        AdaFruit Display:

        Display Pin     Arduino Mega Pin         
        1 GND           BB GND bus
        2 Vcc           BB Vcc (+ive) bus
        3 RESET         Pin 8
        4 D/C           Pin 7
            Data/Command
        5 CARD_CS       Pin 5
            Card Chip Select 
        6 TFT_CS        Pin 6
            TFT/screen Chip Select
        7 MOSI          Pin 51
            Master Out Slave In 
        8 SCK (Clock)   Pin 52
        9 MISO          Pin 50
            Master In Slave Out 
        10 LITE         BB Vcc (+ive) bus
            Backlite

        Zoom in and out buttons:

        1. a 560 Ohm (Grn Blu Red) resistor to connect one side of the button
            to GND
        2. connect the other side of the button to the input pin on the Arduino

        Button          Arduino Mega Pin
        Zoom In         Pin 3
        Zoom Out        Pin 2

    Joystick connections:
    
        Turn on pullup resistor

        Joystick Pin    Arduino Mega Pin
        Vcc             Vcc
        GND             GND
        Horizontal      Analog 0
        Vertical        Analog 1
        Button          Pin 4

        Button --- 560 Ohm Resistor ---|--- 1 uF capacitor --- GND
                                   |
                                   Pin 4

        + For the purposes of debugging start and stop clicks,
        I have wired up two leds, one connected to digital pin 11, and the other
        12. 11 when lit shows the start was toggled, 12 shows stop.

Discussion:
    + Given the code base from the instructions, I built on the solution
    where the client can be run by `python3 comm.py`.
    `comm.py` builds upon the textserial class and integrates the repl
    that I built in part 1.
    I had to modify and add in encoding ISO-8859-1 as quoted from this
    StackOverflow answer: `http://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte` since I was getting tripped out whenever
    any non-ascii content was printed to the Serial port by the Arduino.

    + To aid in debugging on the server side, the Arduino client sends out
    content printed as comments such as:
        '# This is a comment'
    and such lines are ignored.

Running the client:
    To run the client go to the main directory:
    $ make upload

Running the server:
    To run the server go to the main directory:
    $ python3 comm.py

References:
    http://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte
