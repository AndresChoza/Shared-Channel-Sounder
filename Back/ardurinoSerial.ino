//load this code to the arduino to make the serial pass through in order to use the gps
// D0 is Rx and D1 is Tx

void setup()
{
  Serial.begin(9600);	// open serial with PC
  Serial1.begin(9600);//open serial1 with device
}
void loop()
{
  while(Serial.available())
  {
	Serial1.write(Serial.read());
  }
  while(Serial1.available())
  {
	Serial.write(Serial1.read());
  }
}
