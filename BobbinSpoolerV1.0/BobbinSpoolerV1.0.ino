#include <StringSplitter.h>
const int row[5] = {A0, A1, A2, A3, A4}; // LED Matrix Row
const int col[7] = {47, 49, 51, 53, 41, 43, 45}; // LED Matrix Col
int x = 0; // x coordinate of which SSR to turn on
int y = 0; // y coordinate of which SSR to turn on
String positionXY = "";  // x,y coordinates input serial command (push:x,y)
String inputStr; // command input string

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(20);
  for (int i = 0; i < 7; i++) {
    pinMode(col[i], OUTPUT);
    digitalWrite(col[i], LOW);
  }
  for (int i = 0; i < 5; i++) {
    pinMode(row[i], OUTPUT);
    digitalWrite(row[i], HIGH);
  }
  Serial.println("For help type help?");
}

void resetOutputs() {
  digitalWrite(col[y], LOW);
  digitalWrite(row[x], HIGH);
}

void store(String input) { // serial commands
  String startStr = input.substring(0, 5); // 5 character commands
  if (startStr == "*idn?") { // request identification
    Serial.print("Bobbin Winder, V1.0");
  }
  else if (startStr == "help?") { // request identification
    Serial.print("push:x,y for button presses in matrix format");
    Serial.print("*idn? for PartNum, Ver");
  }
  else if (startStr == "push:") { //serial input relay 1
    positionXY = input.substring(5);
    StringSplitter *splitter = new StringSplitter(positionXY, ',', 2); // new StringSplitter(string_to_split, delimiter, limit)
    int itemCount = splitter->getItemCount();
    if (itemCount == 2) {
      String item1 = splitter->getItemAtIndex(0); // item index is the part in the string to display
      String item2 = splitter->getItemAtIndex(1);
      x = item1.toInt(); // getValueInt converts the string value into int
      y = item2.toInt(); // getValueInt converts the string value into int
      Serial.print("positionXY, ");
      Serial.println(positionXY);
      positionXY = "";
      digitalWrite(col[y], HIGH);
      digitalWrite(row[x], LOW);
      delay(200);
      resetOutputs();
    }
    else {
      Serial.println("error, commandFormat");
      positionXY = "";
    }
  }
}

void loop() {
  inputStr = Serial.readStringUntil('\n'); //serial input function
  store(inputStr); //serial input function
}
