#include <LiquidCrystal.h>
#include <DHT.h>

LiquidCrystal lcd(12, 11, 10, 5, 4, 3, 2);
int ValorLDR; // Armazenar a leitura do sensor LDR
int IntensidadeLuz; // Transforma a leitura em uma escala de 0 a 100
int pinoLDR = A0; // PINO ANALÓGICO utilizado para ler o LDR


#define DHTPIN 7     
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Definição dos caracteres personalizados
byte flocoDeNeve[8] = {
  0b00100,
  0b01010,
  0b00100,
  0b11111,
  0b00100,
  0b01010,
  0b00100,
  0b00000
};

byte faceNeutra[8] = {
  0b00000,
  0b01010,
  0b00000,
  0b00000,
  0b11111,
  0b00000,
  0b00000,
  0b00000
};

byte sol[8] = {
  0b00000,
  0b10101,
  0b01110,
  0b11111,
  0b01110,
  0b10101,
  0b00000,
  0b00000
};

void setup()
{
  lcd.begin(16, 2);
  Serial.begin(9600); // Define a velocidade do monitor serial
  pinMode(pinoLDR, INPUT); // Define o pino que o LDR está ligado como entrada de dados

  // Criação dos caracteres personalizados
  lcd.createChar(0, flocoDeNeve);
  lcd.createChar(1, faceNeutra);
  lcd.createChar(2, sol);

dht.begin(); //inicia a biblioteca dht
}

void loop(){
  lcd.clear();
  ValorLDR = analogRead(pinoLDR); // Faz a leitura do sensor, em um valor que pode variar de 0 a 1023
  IntensidadeLuz = map(ValorLDR, 0, 1023, 0, 100); // Converte o valor para uma escala de 0 a 100

  lcd.setCursor(0, 0);
  lcd.print("Luz 0-1023= "); // Imprime texto “Intensidade de Luz = ” na tela
  lcd.print(ValorLDR);

  lcd.setCursor(0, 1);
  lcd.print("Luz % = ");
  lcd.print(IntensidadeLuz);
  lcd.print("%");

  // Desenhar a figura dependendo da intensidade da luz
  lcd.setCursor(14, 1); // Posiciona o cursor na coluna 14 da segunda linha
  if (IntensidadeLuz < 30) {
    lcd.write(byte(0)); // Floco de neve
  } else if (IntensidadeLuz < 66) {
    lcd.write(byte(1)); // Face neutra
  } else {
    lcd.write(byte(2)); // Sol
  }

  delay(7000); // Aguarda 5000 milissegundos para fazer nova leitura
  lcd.clear();
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  lcd.setCursor(0, 0);
  lcd.print("Humidade (%): ");
  lcd.print(humidity);

  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(temperature);

  delay(7000);
}
