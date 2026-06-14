// --- MOTOR PINS ---
const int DIR_L = 2; 
const int PWM_L = 5; 
const int DIR_R = 4; 
const int PWM_R = 6; 

// --- UPDATED SENSOR PINS ---
const int Line_Left  = A1; // Updated to A1
const int Line_Right = A2; // Updated to A2

void setup() {
  pinMode(DIR_L, OUTPUT); 
  pinMode(PWM_L, OUTPUT);
  pinMode(DIR_R, OUTPUT); 
  pinMode(PWM_R, OUTPUT);
  
  pinMode(Line_Left, INPUT); 
  pinMode(Line_Right, INPUT);
}

void loop() {
  // Reading digital signal: Obstacle sensors usually return 0 for Black/Detected
  int val_L = digitalRead(Line_Left);
  int val_R = digitalRead(Line_Right);

  // 1. FORWARD: Both sensors see BLACK (Line detected = 0)
  if (val_L == 0 && val_R == 0) {
    digitalWrite(DIR_L, LOW);
    digitalWrite(DIR_R, LOW);
    analogWrite(PWM_L, 120); 
    analogWrite(PWM_R, 80); 
  } 
  
  // 2. TURN LEFT: Left sees BLACK (0), Right sees WHITE (1)
  else if (val_L == 0 && val_R == 1) {
    digitalWrite(DIR_L, LOW);
    analogWrite(PWM_L, 0);      
    analogWrite(PWM_R, 100);    
  }
  
  // 3. TURN RIGHT: Right sees BLACK (0), Left sees WHITE (1)
  else if (val_L == 1 && val_R == 0) {
    digitalWrite(DIR_R, LOW);
    analogWrite(PWM_R, 0);      
    analogWrite(PWM_L, 120);    
  }

  // 4. STOP: Both sensors see WHITE (No line = 1)
  else {
    analogWrite(PWM_L, 0);
    analogWrite(PWM_R, 0);
  }
}