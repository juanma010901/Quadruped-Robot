void setup() {
  Serial1.begin(9600); // Inicializa la comunicación serial 1 a una velocidad de 9600 baudios

}

void loop() {

  Serial1.print("{'Id':1,'Start': 0,'TrackId': 2}"); 
  delay(1000); 
  
}