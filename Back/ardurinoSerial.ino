void setup()
{
  Serial.begin(115200);	// open serial with PC
  Serial1.begin(115200);//open serial1 with device
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