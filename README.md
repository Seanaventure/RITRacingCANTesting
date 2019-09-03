# RITFormulaTesting
## About
This is a tool used by the RIT Formula SAE team to test the electronics of the cars. It is a hardware in loop testing tool
which means it plugs into the car and directly tests things. This specific tool test the CAN communication in the car. All
the microcontrollers in the car communicate via the CAN bus, which is a communication protocol. This tool plugs into the CAN
bus and can read and send messages. This is useful because it allows us to peek into the car and see what all the microcontrollers
are telling each other. In addition it allows us to send messages to the CAN bus. This effectivley allows us to "spoof" CAN messages
from other components to see how the car reacts. For example, we can send a message telling the car the RPMs are at 7000, and then read 
the corresponding CAN messages to see what happends. In addition, all tests can be automated. So you can tell it to send a sequence of
messages and then wait for certain messages to be sent back.
## How to use
### Installation
To run the program naviagate to the main directory and type `python GUI_controller gui COM BAUD` where COM represents which com port
the arduino is plugged into and BAUD is the baud rate, 115200 by default. Also, `gui` can be replaced by `cmd` to run a command line version.
#### Required dependencies
Tkinter is the graphics engine, which should be included when you download python. In additoin pyserial is required.
### Usage
Once the program is started the interface is quite simple. The log pan on the left is simply an output of the CAN messages/system status. The 
middle column contains the buttons start/stop logging. These, as you would imagine, start and stop logging messages. Next there are 2 fields
for an ID and message. The ID is the ID for the can message, and the message box is for the message of the CAN message you want to send.
The message box also has other functionalities. By putting in a file you can either send a list of messages, or run tests, which will be
discussed in the next section. Next comes the filter functionality. This allows you to either filter to only see CAN messages with certain IDs
or message contents. 

### Tests
Tests are an easy way to verify that things work correctly. For an example of tests you can look at the test file included.

To create your own test you simply need to create a new text file and use the following markup:
`<test,testname="Foo"> ... <\test>` will create a test named Foo. Note: no space between the end of the comma and the name.

To send messages start with the `<send> ... <\send>` commands. Put all the messages you would like to send inside of this block.
Note: you must put `SND` before each message.

To check to received messages use `<check,timeout=5> ... <\check>` to check a group of messages. It will wait for 5 seconds before failing
the test. Thats it! The only caveats are: For each test it will send all the messages first and then check the response, and to make sure
you have the correct number of bits (11 for ID, 16 for message).

Thats it!

## Credits
Created by Sean Bonaventure and Yoon Kim
