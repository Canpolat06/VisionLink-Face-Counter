#include <WiFi.h>
#include <WebServer.h>

// ESP32 kendi ağı
const char* ssid = " istediğiniz wifi ağı ismi";
const char* password = "12345678"; // kafana göre en az 8 karakter olmalı

WebServer server(80);
int faceCount = 0;

// Ana sayfa: yüz sayısını gösterir
void handleRoot() {
  String html = "<!DOCTYPE html><html><head><title>Yuz sayisis</title></head><body>";
  html += "<h1>Yüz Sayisi: " + String(faceCount) + "</h1>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

// Python'dan gelen sayıyı güncelle
void handleUpdate() {
  if (server.hasArg("count")) {
    faceCount = server.arg("count").toInt();
    server.send(200, "text/plain", "OK");
  } else {
    server.send(400, "text/plain", "Missing count parameter");
  }
}

void setup() {
  Serial.begin(115200);

  // ESP32 Access Point olarak başlat
  WiFi.softAP(ssid, password);
  Serial.println("Access Point başlatıldı!");
  Serial.print("IP Adresi: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.on("/update", handleUpdate);
  server.begin();
}

void loop() {
  server.handleClient();
}
