//Controller Tester V1.0
//Doug Gammill 3/8/22
//Linear Labs Inc.
#include <AccelStepper.h>
#include <LiquidCrystal.h>
#define stepPinX 48 // Driver X pusle pin
#define dirPinX 47 // Driver X direction pin
#define en_X 46
#define footSwitch 50
#define motorInterfaceType 1 // interface type for the accel stepper library, works with TB6600 stepper drivers​
#define stepPinY 28 // Driver Y pusle pin
#define dirPinY 29 // Driver Y direction pin
#define en_Y 30
#define manual_SwY 51
#define DT 52
#define CLK 53
#define startA 8
#define startB 9
#define startC 10
#define up 12
#define dn 11
#define Estop 13

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);
String idn = "Stator Winder, Semi-automatic, V1.0";
bool footSwitch_Val;
bool footSwitch_Index = 0;
bool indexY = 0; // to know when to move Y axis
bool startAVal;
bool phaseIndex = 0;
bool indexA = 0;
bool startBVal;
bool indexB = 0;
bool startCVal;
bool indexC = 0;
bool upVal;
bool dnVal;
bool eStopVal;
bool eStopIndex = 0;
//const long interval = 200; // interval at which to execute timing functions (milliseconds)
//unsigned long prevMillis = 0; // will store last time was updated
//unsigned long currentMillis = 0; // timing functions
String inputStr; // serial input commands
int rotation;  // encoder knop starting position
int value; // encoder knob value
bool LeftRight; // encoder knob cw or ccw
int currentPositionY; // whole number of steps to move 1 pole = 20
float carry1; // carry to add up whole number for y steps
int index;
int i;
int currentPositionX = 0;
int turns = 0; // serial input variable total number of turns per pole
bool CCW = true; // serial input variable
float firstPole = 0.0; // serial output what step were on 0.5 increments
float secondPole = 0.0; // serial output what step were on 0.5 increments
int poleNum; // example: a1, a2, a3, a4
int poleNumNot; // example: A1, A2, A3, A4
String startOK = "";
String poleLetter = "";
String poleLetterNot = "";
bool manual_SwY_Val;
bool en_manY_State = false;
bool lastButtonStateY = LOW;
bool manual_SwY_State; // the current reading from the input pin
unsigned long lastDebounceTimeY = 0; // the last time the output pin was toggled
unsigned long debounceDelayY = 50; // the debounce time; increase if the output flickers
byte Check[] = {
  B00000,
  B00001,
  B00011,
  B10110,
  B11100,
  B01000,
  B00000,
  B00000
};

AccelStepper stepperX = AccelStepper(motorInterfaceType, stepPinX, dirPinX);
AccelStepper stepperY = AccelStepper(motorInterfaceType, stepPinY, dirPinY);

void setup() {
  pinMode (en_X, OUTPUT); // X Driver enable and LED
  digitalWrite(en_X, HIGH); // en_X_State is variable high or low
  pinMode(footSwitch, INPUT_PULLUP);
  pinMode(startA, INPUT_PULLUP);
  pinMode(startB, INPUT_PULLUP);
  pinMode(startC, INPUT_PULLUP);
  pinMode(up, INPUT_PULLUP);
  pinMode(dn, INPUT_PULLUP);
  pinMode(Estop, INPUT_PULLUP);
  pinMode(manual_SwY, INPUT_PULLUP);
  stepperX.setAcceleration(1000);
  stepperX.setMaxSpeed(1000);
  stepperY.setAcceleration(500);
  stepperY.setMaxSpeed(500);
  pinMode (en_Y, OUTPUT); // Y Driver enable and LED
  digitalWrite(en_Y, HIGH); // en_Y_State is variable high or low
  pinMode (CLK, INPUT);
  pinMode (DT, INPUT);
  rotation = digitalRead(CLK); // for encoder knob
  Serial.begin(57600);
  Serial.setTimeout(50); // set to 50 because it adds too much delay to relay
  lcd.begin(16, 2);                         //LCD one time set up
  lcd.createChar(0, Check);                 //lcd custom character
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Linear Labs Inc.");
  Serial.println("Enter help? for help");
}
void updateLCD() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Pole: ");
  lcd.setCursor(8, 0);
  lcd.print("Total: ");
  lcd.setCursor(14, 0);
  lcd.print(turns);
  lcd.setCursor(0, 1);
  lcd.print("Turn: ");
  if (CCW == true) {
    lcd.setCursor(5, 0);
    lcd.print(poleLetter);
    lcd.setCursor(6, 0);
    lcd.print(poleNum);
    lcd.setCursor(5, 1);
    lcd.print(firstPole);
  }
  else {
    lcd.setCursor(5, 0);
    lcd.print(poleLetterNot);
    lcd.setCursor(6, 0);
    if (poleNumNot < 9) {
      lcd.print(poleNumNot);
      lcd.setCursor(5, 1);
      lcd.print(secondPole);
    }
    else {
      lcd.print("");
      lcd.setCursor(5, 1);
      lcd.print("");
    }
  }
}
void potentiometerValue() {
  if (en_manY_State == true) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Offset: Engaged!");
  }
  while (en_manY_State == true) {
    checkEstop();
    debounceManSw();
    value = digitalRead(CLK);
    if (value != rotation) { // Use the DT pin to find out which way were turning.
      if (digitalRead(DT) != value) {  // Clockwise
        currentPositionY = currentPositionY + 4;
        LeftRight = true;
      } else { //Counterclockwise
        LeftRight = false;
        currentPositionY = currentPositionY - 4;
      }
      if (LeftRight) {
        Serial.print ("cw, ");
      } else {
        Serial.print("ccw, ");
      }
      Serial.println(currentPositionY);
    }
    rotation = value;
    stepperY.moveTo(currentPositionY);
    stepperY.run();
    if (en_manY_State == false) {
      updateLCD();
    }
  }
}
void checkEstop() {
  eStopVal = digitalRead(Estop);
  if (eStopVal == 0) {
    eStopIndex = 1;
    Serial.println("ESTOP, 1");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Estop: Engaged!!");
    en_manY_State = false;
  }
  while (eStopIndex == 1) {
    eStopVal = digitalRead(Estop);
    digitalWrite(en_X, LOW);
    digitalWrite(en_Y, LOW);
    if (eStopVal == 1) {
      Serial.println("ESTOP, 0");
      updateLCD();
      digitalWrite(en_X, HIGH);
      digitalWrite(en_Y, HIGH);
      eStopIndex = 0;
    }
  }
}
void debounceManSw() {
  manual_SwY_Val = digitalRead(manual_SwY);
  if (manual_SwY_Val != lastButtonStateY) {
    // reset the debouncing timer
    lastDebounceTimeY = millis();
  }
  if ((millis() - lastDebounceTimeY) > debounceDelayY) {
    if (manual_SwY_Val != manual_SwY_State) {
      manual_SwY_State = manual_SwY_Val;
      if (manual_SwY_State == LOW) {
        en_manY_State = !en_manY_State;
        //potInVal = analogRead(potIn);
        //potInMap = map(potInVal, 0, 1023, 0, 255);
        Serial.print("enYstate, ");
        Serial.println(en_manY_State);
      }
    }
  }
  lastButtonStateY = manual_SwY_Val;
}
void upDnButton() {
  upVal = digitalRead(up);
  dnVal = digitalRead(dn);
  if ((upVal == 0) && (turns <= 30)) {
    turns++;
    if (turns > 30) {
      turns = 1;
    }
    Serial.print("Turn, ");
    Serial.println(turns);
    updateLCD();
    delay(100);
  }

  if ((dnVal == 0) && (turns >= 1)) {
    turns--;
    if (turns < 1) {
      turns = 30;
    }
    Serial.print("Turn, ");
    Serial.println(turns);
    updateLCD();
    delay(100);
  }
}

void startButton() {
  startAVal = digitalRead(startA);
  startBVal = digitalRead(startB);
  startCVal = digitalRead(startC);
  if ((startAVal == 0) && (indexA == 0)) {
    indexA = 1;
    startOK = "a";
    start();
  }
  else if ((startAVal == 1) && (indexA == 1)) {
    indexA = 0;
  }
  else if ((startBVal == 0) && (indexB == 0)) {
    indexB = 1;
    startOK = "B";
    start();
  }
  else if ((startBVal == 1) && (indexB == 1)) {
    indexB = 0;
  }
  else if ((startCVal == 0) && (indexC == 0)) {
    indexC = 1;
    startOK = "c";
    start();
  }
  else if ((startCVal == 1) && (indexC == 1)) {
    indexC = 0;
  }
}
void store(String input) {
  String startStr = input.substring(0, 5);
  if (startStr == "turn:") {
    turns = input.substring(5).toInt();
    Serial.print("Turn, ");
    Serial.println(turns);
    updateLCD();
  }
  else if (startStr == "strt:") { // serial input start variable
    startOK = input.substring(5);
    startOK.remove(1, 2); // remove "\r"
    start();
  }
  else if (startStr == "help?") { // serial input help variable
    Serial.println("turn: enter this plus number of turns per pole");
    Serial.println("strt: enter this plus letter of the phase you are winding");
    Serial.println("*idn? for unit ID");
  }
  else if (startStr == "*idn?") { // serial input ID variable
    Serial.println(idn);
  }
}
void start() { // run cycle
  firstPole = 0.5;
  secondPole = 0.5;
  CCW = true;
  carry1 = 0; // on a new job set carry to 0
  currentPositionY = 0;
  currentPositionX = 0;
  poleNum = 1; // example: a1, a2, a3, a4
  poleNumNot = 1; // example: A1, A2, A3, A4
  stepperX.setCurrentPosition(0);
  stepperY.setCurrentPosition(0);
  if ((startOK == "a") || (startOK == "A")) {
    poleLetter = "a";
    poleLetterNot = "A";
  }
  else if ((startOK == "b") || (startOK == "B")) {
    poleLetter = "B";
    poleLetterNot = "b";
  }
  else if ((startOK == "c") || (startOK == "C")) {
    poleLetter = "c";
    poleLetterNot = "C";
  }
  else {
    Serial.println("Pole, wrong pole");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Pole:");
    lcd.setCursor(5, 0);
    lcd.print("wrong pole");
    poleLetter = "";
    poleLetterNot = "";
    startOK = "";
  }
  if ((startOK != "") && (turns > 0) && (turns < 31)) {
    Serial.print(poleLetter);
    Serial.print(poleNum);
    Serial.print(", ");
    Serial.println(firstPole + 0.5);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Pole: ");
    lcd.setCursor(8, 0);
    lcd.print("Total: ");
    lcd.setCursor(14, 0);
    lcd.print(turns);
    lcd.setCursor(0, 1);
    lcd.print("Turn: ");
    if (CCW == true) {
      lcd.setCursor(5, 0);
      lcd.print(poleLetter);
      lcd.setCursor(6, 0);
      lcd.print(poleNum);
      lcd.setCursor(5, 1);
      lcd.print(firstPole + 0.5);
    }
  }
  else if (startOK != "") {
    if ((turns <= 0) || (turns >= 31)) {
      Serial.println("Turn, 0");
      poleLetter = "";
      poleLetterNot = "";
      startOK = "";
      turns = 0;
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Pole: ");
      lcd.setCursor(5, 0);
      lcd.print(poleLetterNot);
      lcd.setCursor(6, 0);
      lcd.print(poleNumNot);
      lcd.setCursor(8, 0);
      lcd.print("Total:");
      lcd.setCursor(14, 0);
      lcd.print(turns);
      lcd.setCursor(0, 1);
      lcd.print("Turn:");
      lcd.setCursor(5, 1);
      lcd.print("Set Turns!");
    }
  }
}
void moveY() { // can only move whole number of steps need to use carry; 1 pole = 20.83 steps
  i = 0;
  if (CCW == true) {
    if ((poleNumNot == 2) || (poleNumNot == 4) || (poleNumNot == 6)) {
      if (phaseIndex == 0) {
        index = 9; // moves 9 poles
        phaseIndex = !phaseIndex;
        CCW = !CCW;
        poleNumNot = poleNumNot + 1;
      }
      else {
        index = 1; // moves 1 pole
        poleNumNot = poleNumNot + 1;
      }
    }
    else { // update poleNumNot (A, b, C, if y axis is short run)
      index = 1; // moves 1 pole
      poleNumNot = poleNumNot + 1;

    }
  }
  else if (CCW == false) {
    if ((poleNum == 2) || (poleNum == 4) || (poleNum == 6)) {
      if (phaseIndex == 1) {
        index = 9; // moves 9 poles
        phaseIndex = !phaseIndex;
        CCW = !CCW;
        poleNum = poleNum + 1;
      }
      else {
        index = 1; // moves 1 pole
        poleNum = poleNum + 1;
      }
    }
    else { // update poleNum (a, B, c, if y axis is short run)
      index = 1; // moves 1 pole
      poleNum = poleNum + 1;
    }
  }

  while (i != index) {
    checkEstop();
    carry1 = carry1 + 0.83; // number of carried steps = 0.83
    if (carry1 >= 1) {
      currentPositionY = currentPositionY + 1;
      carry1 = carry1 - 1;
    }
    currentPositionY = currentPositionY + 20; // 20.83 steps = 1 pole
    stepperY.runToNewPosition(currentPositionY);
    i++;
  }
  indexY = 0;
  lcd.setCursor(10, 1);
  lcd.write("     ");
}
void FootSw() {
  footSwitch_Val = digitalRead(footSwitch);
  if ((footSwitch_Val == 0) && (footSwitch_Index == 0) && (startOK != "")) {
    footSwitch_Index = 1; // foot switch will only engage once when pressed down
    if ((poleLetter == "a") || (poleLetter == "B") || (poleLetter == "c")) { // starts at half of a turn
      if ((poleNum == 1) && (firstPole == 0.5)) {
        firstPole = firstPole + 0.5;
        phaseIndex = 0;
      }
    }
    if (indexY == 1) { // move Y here
      moveY();
      if ((CCW == false) && ( poleNumNot < 9)) {
        Serial.print(poleLetterNot);
        Serial.print(poleNumNot);
        Serial.print(", ");
        Serial.println(secondPole);
        updateLCD();
      }
      if (CCW == true) {
        Serial.print(poleLetter);
        Serial.print(poleNum);
        Serial.print(", ");
        Serial.println(firstPole);
        updateLCD();
      }
    }
    else if ((CCW == true) && (firstPole != turns) && (indexY == 0)) { // do not move y
      currentPositionX = currentPositionX + 400; // 400 steps = 180deg rotation
      stepperX.runToNewPosition(currentPositionX);
      firstPole = firstPole + 0.5;
      Serial.print(poleLetter);
      Serial.print(poleNum);
      Serial.print(", ");
      Serial.println(firstPole);
      updateLCD();
    }
    else if ((CCW == false) && (secondPole != turns) && (indexY == 0)) { // do not move Y
      currentPositionX = currentPositionX - 400; // 400 steps = 180deg rotation
      stepperX.runToNewPosition(currentPositionX);
      secondPole = secondPole + 0.5;
      Serial.print(poleLetterNot);
      Serial.print(poleNumNot);
      Serial.print(", ");
      Serial.println(secondPole);
      updateLCD();
    }
    else if ((firstPole == turns) && (CCW == true) && (indexY == 0)) { // move Y after this
      currentPositionX = currentPositionX + 400; // 400 steps = 180deg rotation
      stepperX.runToNewPosition(currentPositionX);
      CCW = !CCW; // changes the next rotation to CW
      indexY = 1;
      firstPole = 0.5;
      secondPole = 0.5;
      Serial.print(poleLetter);
      Serial.print(poleNum);
      Serial.println(", 0");
      lcd.setCursor(10, 1);
      lcd.write("moveY");
    }
    else if ((secondPole == turns) && (CCW == false) && (indexY == 0)) { // move Y after this
      currentPositionX = currentPositionX - 400; // 400 steps = 180deg rotation
      stepperX.runToNewPosition(currentPositionX);
      CCW = !CCW; // changes the next rotation to CCW
      indexY = 1;
      secondPole = 0.5;
      firstPole = 0.5;
      Serial.print(poleLetterNot);
      Serial.print(poleNumNot);
      Serial.println(", 0");
      lcd.setCursor(10, 1);
      lcd.write("moveY");
    }
  }
  if ((footSwitch_Val == 1) && (footSwitch_Index == 1)) {
    footSwitch_Index = 0; // foot switch will only engage once when pressed down
    if (poleNum == 9) { // end test
      Serial.println("Pass, 1");
      lcd.setCursor(15, 1);
      lcd.write(byte(0)); // prints checkmarks for done
      startOK = "";
      poleLetter = "";
      poleLetterNot = "";
    }
  }
}
void loop() {
  //currentMillis = millis();
  inputStr = Serial.readStringUntil('\n'); // serial input function
  store(inputStr); // serial input function
  checkEstop();
  startButton();
  debounceManSw();
  potentiometerValue();
  upDnButton();
  FootSw();
}
