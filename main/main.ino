#include <due_can.h>
#define  testID     0x0A
#define  Max_len    8
#define  testMsgH   0x00000070
                    
#define  testMsgL   0x656E6973 
enum States{
  Idle,
  Send,
  Log
};
//SND 007 00000070656E6973
States state = Idle;
int counter = 0;
int start = 0;
int timeend  = 0;
int randCounter = 0;
void setup() {
  // put your setup code here, to run once:
  Can0.begin(CAN_BPS_500K);
  Can1.begin(CAN_BPS_500K);
  Serial.begin(115200);
  Serial.setTimeout(2);
}

void loop() {
  // put your main code here, to run repeatedly:
  switch(state){
    case Log: logData();
    case Idle:;//Do nothing if Idling
  }
}
/**
 * This is the method that handles decifering the messages coming through serial.
 * It is tied to the serial interrupt so it is called whenever something is sent through serial
 */
void serialEvent(){
  String msg = Serial.readString();
  String prefix = msg.substring(0,3);
  //Serial.println(prefix);
  if (prefix == "SND"){
    //Serial.println("Getting data");
    int dataLength = msg.length()/24;
    //Serial.println(String(dataLength));
    String msgData[dataLength];
    for (int k = 0; k < dataLength; k++){
      msgData[k] = msg.substring(k*24,(k+1)*24);
      //Serial.println(msgData[k]);
    }
    //Serial.println("Finished getting messages");
    for (int j = 0; j < dataLength; j++){
      String idString = msgData[j].substring(4,7);
      //TODO: Write an actual good String to hex converter
      uint32_t id = (16*16 * toByte(idString.charAt(0)) + 16 * toByte(idString.charAt(1)) + toByte(idString.charAt(2)));
      String dataString = msgData[j].substring(8);      
      uint8_t data[8];
      for (int i = 0; i < 16; i+=2){
        //This loop goes through the string and gets all the hex data      
        String stringByte = dataString.substring(i,i+2);
        //Again, write an actual good string to hex converter
        data[i/2] = (16 * toByte(stringByte.charAt(0)) + toByte(stringByte.charAt(1)));//Adds the each byte to the array.
      }
      sendData(id, data);
    }
   
  }else if (prefix == "LOG"){
    state = Log;
    logData();
  }else if (prefix == "IDL"){
    state = Idle;
  }
}
void sendData(uint32_t ID, uint8_t data[]){
  //Uses can_due to send the data
  
  CAN_FRAME outgoing;
  //uint32_t testIDvar = ID;
  //Serial.println(ID, HEX);
  outgoing.id = ID;
  outgoing.length = Max_len;
  for (int i = 0; i < 8; i++){
    outgoing.data.bytes[i] = data[i];
  }
  Can1.watchFor();
  Can0.sendFrame(outgoing);
  //Serial.println("Sent");
  
}
void logData(){
  //Continuously read data
    readCAN();
    //delay(1);
}

void readCAN(){ 
  Can0.watchFor();
  String msg = "";
  CAN_FRAME incoming;
  if(Can0.available()>0){
    Can0.read(incoming);
    Serial.print(const_char(incoming.id));
    Serial.print(" ");
    for (int i = 0; i < 8; i++){
        Serial.print(const_char(incoming.data.bytes[i]));  
    }
    Serial.print("\n");
  }
}
uint8_t toByte(char data){
  uint8_t value = 0;
  if (data >= '0' && data <= '9'){
    return data - 48;
  }else if (data >= 'A' && data <= 'F'){
    return data - 55;
  }else{
    return 0;
  }
}
String const_char(uint32_t data){
    String msg = "";  
    for (int i = 0; i < 2; i++){
        uint32_t mask = 0xF;
        uint32_t masked_data = data & mask<<(i*4);
        masked_data = masked_data>>(i*4);
        msg = String(String(masked_data, HEX) + msg);
    }
    return msg;
}
