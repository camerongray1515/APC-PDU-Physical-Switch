// Read the status of a digital input and output this over serial whenever it changes
// Value must remain the same for 10 loop iterations to prevent "bouncing" due to a
// dodgy switch contact

// The switch status will be printed to serial every 10 seconds or instantly when
// the switch status changes

int switchPin = 2;
int switchStatus;
int seenSame = 0;
int seenSameThreshold = 10;
int lastSentStatus;

void setup() {
  pinMode(switchPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  int val = digitalRead(switchPin);
  if (val == switchStatus && seenSame < seenSameThreshold) {
    seenSame += 1;
  } else if (val != switchStatus) {
    seenSame = 0;
  }
  
  if (seenSame == seenSameThreshold) {
    if(lastSentStatus != switchStatus || millis() % 10000 == 0) {
      if(switchStatus) {
        Serial.write("on\n");
      } else {
        Serial.write("off\n");
      }
      lastSentStatus = switchStatus;
    }
  }
  
  switchStatus = val;
  delay(1);
}
