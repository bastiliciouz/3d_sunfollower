#!/usr/bin/python3.7
# -*-coding: utf-8-*

import time

from adafruit_ads1x15.analog_in import AnalogIn


class Sensor:
    """Sensorklasse welche für das Auslesen der Hardwaresensoren zuständig ist"""
    anzahl = 0

    def __init__(self, nummer, ad_wandler, kanal, db_connect):
        self.__nummer = nummer  # Durchlaufende Nummer
        self.__ad_wandler = ad_wandler  # Initialisierter AD-Wandler
        self.__kanal = kanal  # Kanal des Sensors

        self.__sensor = AnalogIn(self.__ad_wandler, self.__kanal)  # Initialisierung des Kanals
        self.__sensorwert = 0  # Ausgelesener Wert
        self.__db_connect = db_connect  # Einmalig in Application initialisiert, übergeben zur Nutzung

        Sensor.anzahl += 1  # Anzahl der initialisierten Sensoren erhöhen

    def __del__(self):
        Sensor.anzahl -= 1

    def nummer(self) -> int:
        """Ausgabe der Sensor-Nummer für die Konsolenanzeige"""
        return self.__nummer

    def akt_wert(self):
        """Der aktuelle Wert wird ausgelesen und gespeichert"""
        try:
            self.__sensorwert = self.__sensor.value
            return self.__sensorwert
        except Exception as e:
            self.__db_connect.insert_error_message(e)
            return f"Sensor Error auf Kanal {self.__kanal}"


class Motor:
    """Motorklasse welche die Hardwareservos ansteuert"""
    anzahl = 0

    def __init__(self, kanal, servos, db_connect):
        self.__kanal = kanal  # Servo Kanal
        self.__current_pos = 375  # Aktuelle Position
        self.__current_pos_grad = 90  # Aktuelle Position in Grad
        self.__servos = servos  # Initialisiertes PWM-Modul
        self.__servos.set_pwm(self.__kanal, 0, self.__current_pos)  # Initiales Setzen auf 90°
        self.__db_connect = db_connect  # Einmalig in Application initialisiert, übergeben zur Nutzung

        Motor.anzahl += 1  # Anzahl der initialisierten Motoren erhöhen

    def __del__(self):
        Motor.anzahl -= 1

    def bewegung_horizontal(self, s0, s1, schwelle):
        """Bewegung des unteren Motors.
        Dafür muss die Differenz zwischen Oben Links und Unten Rechts über der Schwelle liegen.
        Je nachdem welcher Wert größer ist wird der Motor nach Links oder Rechts gedreht."""
        if abs(s0.akt_wert() - s1.akt_wert()) > schwelle:
            if s0.akt_wert() <= s1.akt_wert():
                self.bewegung_links()
            elif s0.akt_wert() >= s1.akt_wert():
                self.bewegung_rechts()

    def bewegung_vertikal(self, s0, s1, schwelle):
        """Bewegung des oberen Motors.
        Dafür muss die Differenz zwischen Oben Rechts und Unten Links über der Schwelle liegen.
        Je nachdem welcher Wert größer ist wird der Motor nach Links oder Rechts gedreht."""
        if abs(s0.akt_wert() - s1.akt_wert()) > schwelle:
            if s0.akt_wert() >= s1.akt_wert():
                self.bewegung_links()
            elif s0.akt_wert() <= s1.akt_wert():
                self.bewegung_rechts()

    def bewegung_links(self):
        """Bewegung von Motor X nach Links.
        Das Minimum liegt bei 150 = 0°, darüber hinaus keine Aktion."""
        try:
            if self.__current_pos > 150:
                self.__current_pos -= 5
                self.__current_pos_grad = self.umrechnung(self.__current_pos)  # Umrechnung in Grad
                self.__servos.set_pwm(self.__kanal, 0, self.__current_pos)  # Befehl an Motor
                time.sleep(0.15)  # Latenz der Widerstände beachten!
            # Linker Anschlag erreicht
            else:
                pass
                time.sleep(0.15)

        except Exception as e:
            self.__db_connect.insert_error_message(e)
            return f"Error auf Motor Kanal {self.__kanal}"

    def bewegung_rechts(self):
        """Bewegung von Motor X nach Rechts.
        Das Maximum liegt bei 600 = 180°, darüber hinaus keine Aktion."""
        try:
            if self.__current_pos < 600:
                self.__current_pos += 5
                self.__current_pos_grad = self.umrechnung(self.__current_pos)  # Umrechnung in Grad
                self.__servos.set_pwm(self.__kanal, 0, self.__current_pos)  # Befehl an Motor
                time.sleep(0.15)  # Latenz der Widerstände beachten!
            # Rechter Anschlag erreicht
            else:
                pass
                time.sleep(0.15)

        except Exception as e:
            self.__db_connect.insert_error_message(e)
            return f"Error auf Motor Kanal {self.__kanal}"

    def umrechnung(self, wert):
        """Simple Funktion um den Wert der Anwendung in Grad umzurechnen.
        Wert 2.5 = 1°. Dabei sind 150=0° und 600=180° das Maximum der Servos"""
        self.wert = wert
        return int((self.wert - 150) / 2.5)

    def get_current_pos_grad(self):
        return self.__current_pos

    def get_kanal(self):
        return self.__kanal
