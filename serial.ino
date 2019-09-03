char serialData;
int pin=10;

void setup() {
  pinMode(pin, OUTPUT);
  Serial.begin(9600);
}

// the loop function runs over and over and over and over forever
void loop() {
  if(Serial.available() >0)
    serialData = Serial.read();
    Serial.print(serialData);

    if(serialData == '1'){
      digitalWrite(pin, 'HIGH');}
    else if(serialData == '0'){
      digitalWrite(pin, 'LOW');}
}
