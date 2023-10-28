
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#include <WiFiUdp.h>
#include <TimeLib.h>

#define STASSID "Totonho"
#define STAPSK "27592230"
#define LED_1   2



String weekDays[7]={"Domingo", "Segunda-feira", "Terça-feira", "quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"};
String months[12]={"janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"};

// NTP Servers:
static const char ntpServerName[] = "0.br.pool.ntp.org";

const int timeZone = -3;

WiFiUDP Udp;
unsigned int localPort = 8888;  // local port to listen for UDP packets

time_t prevDisplay = 0; // when the digital clock was displayed

time_t getNtpTime();
void digitalClockDisplay();
void printDigits(int digits);
void sendNTPpacket(IPAddress &address);

void setup() {
 pinMode(LED_1, OUTPUT);
 digitalWrite(LED_1, LOW);
 Serial.begin(115200);

  Serial.println();
  Serial.println();
  Serial.println();

  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());


  Serial.print("IP number assigned by DHCP is ");
  Serial.println(WiFi.localIP());
  Serial.println("Starting UDP");
  Udp.begin(localPort);
  Serial.print("Local port: ");
  Serial.println(Udp.localPort());
  Serial.println("waiting for sync");
  setSyncProvider(getNtpTime);
  setSyncInterval(300);

}

void loop() {


  // wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) 
  {
    WiFiClient client;
    Serial.print("Conectando...");
    
  if (!client.connect("192.168.1.110", 5252)) {
      Serial.println("connection failed");
      return;
  }else
  {
    Serial.println("Conectado!");
    //client.println("Oi Servidor.");
  }
 delay(100);
  if(client.available() > 0){
    Serial.println("Servidor Mandou Algo!");
    String recebeu = "";
    String resposta ="OK";
    while(client.available()){
    recebeu += char(client.read());
    }
    Serial.println(recebeu);
    if(recebeu == "lâmpada acesa")
    {
     digitalWrite(LED_1, LOW);
     resposta ="A luz foi ligada.";
    }
    if(recebeu == "lâmpada apagada")
    {
     digitalWrite(LED_1, HIGH);
     resposta = "A luz foi desligada.";
    }
    if(recebeu == "horas")
    {
      prevDisplay = now();
      resposta = String(hour()) +":"+ String(minute());

    }
    if(recebeu == "que dia é hoje")
    {
    prevDisplay = now();

    resposta = weekDays[weekday(prevDisplay) -1];

    }
    if(recebeu == "data")
    {    
      prevDisplay = now();
      
      resposta = weekDays[weekday(prevDisplay) -1];
      resposta += ", "+ String(day()) +"/"+ String(month()) +"/"+ String(year());

    }
  
  if(Serial.available() > 0)
  {
    resposta = Serial.readString();

  }
   client.println(resposta);

  }

  Serial.println("Conexao Finalizada.");
  }

  delay(2000);
}

void printDigits(int digits)
{
  // utility for digital clock display: prints preceding colon and leading 0
  Serial.print(":");
  if (digits < 10)
    Serial.print('0');
  Serial.print(digits);
}


/*-------- NTP code ----------*/

const int NTP_PACKET_SIZE = 48; // NTP time is in the first 48 bytes of message
byte packetBuffer[NTP_PACKET_SIZE]; //buffer to hold incoming & outgoing packets

time_t getNtpTime()
{
  IPAddress ntpServerIP; // NTP server's ip address

  while (Udp.parsePacket() > 0) ; // discard any previously received packets
  Serial.println("Transmit NTP Request");
  // get a random server from the pool
  WiFi.hostByName(ntpServerName, ntpServerIP);
  Serial.print(ntpServerName);
  Serial.print(": ");
  Serial.println(ntpServerIP);
  sendNTPpacket(ntpServerIP);
  uint32_t beginWait = millis();
  while (millis() - beginWait < 1500) {
    int size = Udp.parsePacket();
    if (size >= NTP_PACKET_SIZE) {
      Serial.println("Receive NTP Response");
      Udp.read(packetBuffer, NTP_PACKET_SIZE);  // read packet into the buffer
      unsigned long secsSince1900;
      // convert four bytes starting at location 40 to a long integer
      secsSince1900 =  (unsigned long)packetBuffer[40] << 24;
      secsSince1900 |= (unsigned long)packetBuffer[41] << 16;
      secsSince1900 |= (unsigned long)packetBuffer[42] << 8;
      secsSince1900 |= (unsigned long)packetBuffer[43];
      return secsSince1900 - 2208988800UL + timeZone * SECS_PER_HOUR;
    }
  }
  Serial.println("No NTP Response :-(");
  return 0; // return 0 if unable to get the time
}

uint8_t dow(unsigned long t)
{
    return ((t / 86400) + 4) % 7;
}

// send an NTP request to the time server at the given address
void sendNTPpacket(IPAddress &address)
{
  // set all bytes in the buffer to 0
  memset(packetBuffer, 0, NTP_PACKET_SIZE);
  // Initialize values needed to form NTP request
  // (see URL above for details on the packets)
  packetBuffer[0] = 0b11100011;   // LI, Version, Mode
  packetBuffer[1] = 0;     // Stratum, or type of clock
  packetBuffer[2] = 6;     // Polling Interval
  packetBuffer[3] = 0xEC;  // Peer Clock Precision
  // 8 bytes of zero for Root Delay & Root Dispersion
  packetBuffer[12] = 49;
  packetBuffer[13] = 0x4E;
  packetBuffer[14] = 49;
  packetBuffer[15] = 52;
  // all NTP fields have been given values, now
  // you can send a packet requesting a timestamp:
  Udp.beginPacket(address, 123); //NTP requests are to port 123
  Udp.write(packetBuffer, NTP_PACKET_SIZE);
  Udp.endPacket();
}


