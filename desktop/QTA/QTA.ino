//***********************************************************************

// QUADRO DE TRANSFERENCIA AUTOMATICA

//***********************************************************************
//***********************************************************************

// Definições de tipos utilizados:
//=======================================================================

#define uint unsigned int // inteiros positivos de 16 bits.
#define ulong unsigned long // inteiros positivos de 32 bits.
#define vs1Pin A0 // Pino A0 - Leitura da Tensão
#define viPin A1 // Pino A1 - Leitura da corrente

//***********************************************************************
//***********************************************************************

// Bibliotecas utilizadas:
//=======================================================================

#include <LiquidCrystal.h> // LCD padrão.

//***********************************************************************
//***********************************************************************

// Definição das Interrupções utilizadas:
//=======================================================================

#define Vsense_INTR 2 // pino de Interrupção utilizado para se

// detectar passagem da tensão por zero.
//-----------------------------------------------------------------------

#define Isense_INTR 3 // pino de Interrupção utilizado para se
// detectar passagem da corrente por zero.

//***********************************************************************
//***********************************************************************

// Definição da Interface e tipo do LCD:
//=======================================================================

#define LCD_RS 8 // pino "R/S" do LCD.
#define LCD_E 9 // pino "E" do LCD.
#define LCD_D4 10 // pino "D4" do LCD.
#define LCD_D5 11 // pino "D5" do LCD.
#define LCD_D6 12 // pino "D6" do LCD.
#define LCD_D7 13 // pino "D7" do LCD.
//-----------------------------------------------------------------------
#define LCD_COL 20 // total de colunas no LCD utilizado.
#define LCD_LIN 4 // total de linhas no LCD utilizado.
//-----------------------------------------------------------------------

LiquidCrystal LCD_01 ( LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7 );

//***********************************************************************
//variáveis dos relés


int relePin = 6;

//--------------------------------------------------
//variaveis do fator de potência
int T1;
float FP, angulo_rad;
float FP_A=1;
int FP_aux;
byte FP_byte[4];
char data[4];


//--------------------------------------------------

//***********************************************************************
// Definição das Variáveis Globais:
//=======================================================================

volatile ulong Vsense_time_us = 0; // marcação do edge do Vsense.
volatile ulong Isense_time_us = 0; // marcação do edge do Isense.
long valorTensao;    
long volts;   
long valorCorrente;
float amper;
long amper_aux;
float potencia;
float consumo;
float consumo_aux;
float carga = 50;
float vetCorrente[300];
//--------------------------------------------------
uint FP_data;
//--------------------------------------------------

//-----------------------------------------------------------------------

ulong prev_Millis = 0; // utilizada para temporização da
// visualização dos resultados no Display.

//***********************************************************************
//***********************************************************************

// Definição das Constantes Globais:
//=======================================================================

#define AC_freq 60 // frequência da rede elétrica, em [Hz].
#define AC_ciclo_us ( 1e6 / AC_freq ) // ciclo da rede elétrica,
// em micro-segundos.

//-----------------------------------------------------------------------

#define Pi 3.141593 // valor do número "Pi" (arredondado).

//-----------------------------------------------------------------------

#define FP_view_rate 2 // taxa de atualização do FP no Display,
// em [Hz].

//***********************************************************************
//***********************************************************************

// ISR para tratamento da IRQ gerada pelo edge positivo do Vsense.
// A rotina simplesmente registra o cronômetro atual no momento da
// ocorrência do edge do Vsense.
//=======================================================================

void Vsense_ISR ()
{
Vsense_time_us = micros(); // faz a marcação do edge do Vsense.
}

//***********************************************************************
//***********************************************************************

// ISR para tratamento da IRQ gerada pelo edge positivo do Isense.
// A rotina simplesmente registra o cronômetro atual no momento da
// ocorrência do edge do Isense.
//=======================================================================

void Isense_ISR ()
{
Isense_time_us = micros(); // faz a marcação do edge do Isense.
}

//***********************************************************************
//***********************************************************************

// Inicializa o mecanismo para IRQ da detectção da tensão.
//=======================================================================

void Vsense_INTR_prep ()
{
pinMode ( Vsense_INTR, INPUT ); // seta a IRQ para detecção
// da tensão.
attachInterrupt ( digitalPinToInterrupt (Vsense_INTR), Vsense_ISR, RISING );
}


//***********************************************************************
//***********************************************************************

// Inicializa o mecanismo para IRQ da detectção da corrente.
//=======================================================================

void Isense_INTR_prep ()
{
pinMode ( Isense_INTR, INPUT ); // seta a IRQ para detecção
// da corrente.
attachInterrupt ( digitalPinToInterrupt (Isense_INTR), Isense_ISR, RISING );
}

//***********************************************************************
//***********************************************************************

// Inicializa o Sistema do LCD.
//=======================================================================


void Calcula_grandeza (){
  
  
   double maior_Valor = 0;
   double valor_Corrente = 0; 
  
  //Calculo da tensão:
    valorTensao = analogRead(vs1Pin);   // Atribui a variavel valorTensao o valor do pino vs1Pin  
    volts = valorTensao * 220/186;   // Atribui a variavel volts o valorLido * cte 
    
  //Calculo da corrente:
  for(int i = 0; i < 300; i++)
  {
    vetCorrente[i] = analogRead(viPin);
    delayMicroseconds(600);
  }  
  for(int i = 0; i < 300; i++)
  {
    if(maior_Valor < vetCorrente[i])
    {
      maior_Valor = vetCorrente[i];
    }
  }
  
  maior_Valor = maior_Valor * 0.004882812;
  valor_Corrente = maior_Valor - 2.5;
  valor_Corrente = valor_Corrente * 1000;
  valor_Corrente = valor_Corrente / 185;         //sensibilidade : 66mV/A para ACS712 30A / 185mV/A para ACS712 5A
  valor_Corrente = valor_Corrente / 1.41421356;
  amper = valor_Corrente;  

    //Calculo da Potência
  potencia = amper * volts;
  potencia = potencia / 1000;

    }
void LCD_SYS_init ()
{
   LCD_01.begin ( LCD_COL, LCD_LIN ); // especifica o "tipo' do LCD.
   LCD_01.clear(); // limpa a tela do LCD.
   LCD_01.noCursor(); // "desliga" a visualização do cursor.
   LCD_01.setCursor ( 6, 0 ); // exibe informação geral.
   LCD_01.print ("***FP***");
}

//***********************************************************************
//***********************************************************************

// Verifica se é o momento de atualizar a visualização do "FP",
// conforme o período de tempo especificado (em mili-segundos).
//=======================================================================

bool FP_atualize_CHK ( uint intervalo )
{
//--------------------------------------------------

   ulong atual_Millis;
   bool atualize;

//--------------------------------------------------

   atual_Millis = millis(); // obtém valor atual do "millis".
   if ( ( atual_Millis - prev_Millis ) >= intervalo )
   {
      atualize = true; // se é o momento de atualizar o display, indica isto.
      prev_Millis = atual_Millis; // seta nova referência para
   } // próxima atualização.

   else
   {
      atualize = false; // se não é o momento de atualizar
   } // o display, indica isto.
   return (atualize); // finaliza indicando o resultado.
}

//***********************************************************************
//***********************************************************************
// Exibe no display o valor do "FP". O valor é exibido na forma
// "x.xxx", ou seja, com até 3 dígitos significativos após o ponto
// decimal.
//=======================================================================

void LCD_FP_display ( uint FP_data )
{



   LCD_01.setCursor ( 0, 3 ); // formata e exibe para
   LCD_01.print ("FP=0."); // esta condição.
   LCD_01.print (FP_data);
   

   LCD_01.setCursor ( 0, 1 ); // formata e exibe para
   LCD_01.print ("V=");   
   LCD_01.print (volts);        
   LCD_01.print (" V");    
  
   LCD_01.setCursor(0, 2);
   LCD_01.print ("I=");
   LCD_01.print (amper);
   LCD_01.print (" A");
   
   LCD_01.setCursor ( 9, 1 );
   LCD_01.print("| P=");   
   LCD_01.print(potencia);        
   LCD_01.print("KWh");    
   


   
}

//***********************************************************************
//***********************************************************************

// Inicializa todo o Sistema, e prepara os Mecanismos necessários
// para a Medição do Fator de Potência ("FP").
//=======================================================================

void setup()
{
/* Inicia a porta serial*/

   Serial.begin(9600);

/* Define os pinos como INPUT ou OUTPUT */
 
   pinMode(vs1Pin, INPUT); // define o pino 14 como entrada
   pinMode(viPin, INPUT);  // define o pino 15 como entrada
   pinMode(relePin, OUTPUT); //define o pino 1 como saida

   noInterrupts(); // inicialmente, impede interrupções.

   Vsense_INTR_prep(); // inicializa mecanismo de IRQ para a tensão.
   Isense_INTR_prep(); // inicializa mecanismo de IRQ para a corrente.

//-----------------------------------------------------------------------
   LCD_SYS_init(); // inicializa o Sistema do LCD.
//-----------------------------------------------------------------------

   interrupts(); // a partir daqui, permite interrupções.

}

//***********************************************************************
//***********************************************************************

// Loop principal do Sistema para a Medição do Fator de Potência,
// baseado em Hardware específico e utilizando a plataforma Arduíno.
//=======================================================================

void loop ()
{

   Calcula_grandeza();

   if ( FP_atualize_CHK ( 1000 / FP_view_rate ) ); // se é o momento atualizar o display:
   {

      1 = ( Isense_time_us - Vsense_time_us ); // então calcula a defasagem de tempo entre a tensão e a corrente na carga.

      if ( T1 >= 0 ) // se esta medição é válida:
      {
   //calculo do fator de potencia
   angulo_rad = (float) T1 * (2*Pi / AC_ciclo_us); // calcula o ângulo correspondente,
   // em radianos.
   FP = cos(angulo_rad); // calcula o respectivo Fator de Potência.
   FP = 1000*FP; // converte o "FP" para a escala entre 0 e 1000.
   FP_data = (uint) FP; // obtém o valor inteiro correspondente.
   LCD_FP_display(FP_data); // exibe no display, o Fator de Potência.

      //envio dos dados pela porta serial
   Serial.print(FP_data); 
   Serial.print("g");
   Serial.flush();
   Serial.print(volts);
   Serial.print("v");
   Serial.flush();
   Serial.print(amper);
   Serial.print("a");
   Serial.flush();
   Serial.print(potencia);
   Serial.print("p");
   Serial.flush();
   }
      }

//Acionamento do Rele
  
  if (FP < 0.92){
      digitalWrite(relePin, HIGH);
      //digitalWrite(relePin, LOW);
   }
   else {
   //   digitalWrite(relePin, HIGH);
      digitalWrite(relePin, LOW);
   }

}
