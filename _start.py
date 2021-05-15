#!/usr/bin/python3.7
# -*-coding: utf-8-*-

import Adafruit_PCA9685 as pca
import adafruit_ads1x15.ads1115 as ads
import board
import busio

import functions as func  # functions.py
from database import DBConnect  # database.py


class SunfollowerApplication:

    def __init__(self):
        self.__i2c_bus = busio.I2C(board.SCL, board.SDA)  # Initialisierung I2C Bus
        self.__ad_wandler = ads.ADS1115(self.__i2c_bus)  # Initialisierung AD-Wandler
        self.__servos = pca.PCA9685()  # Initialisierung PWM Treiber mit Default Adresse 8x40
        self.__servos.set_pwm_freq(60)  # Frequenz in Hz für PWM

        self.__schwellwert = 200  # Definierter Schwellwert um Änderungen auszulösen
        self.__anzeige = True  # Anzeige auf Kommandozeile an = True oder aus = False

        self.__db_connect = DBConnect()  # Datenbank Verbindung

        self.init_sensors()
        self.init_motors()
        self.print_start()
        self.run()

    def init_sensors(self):
        # Initialisierung aller Sensor-Objekte
        self.__sens = list(range(4))  # Liste der Sensoren
        kanaele = [ads.P0, ads.P1, ads.P2, ads.P3]  # Kanäle des AD Reihenfolge: OL = 3, OR = 0, UL = 2, UR = 1
        for value in range(0, 4):  # Erstellung der Sensor-Objekte
            nummer = value
            kanal = kanaele[value]
            self.__sens[value] = func.Sensor(nummer, self.__ad_wandler, kanal, self.__db_connect)

    def init_motors(self):
        # Initialisierung aller Motor-Objekte
        self.__motoren = list(range(2))  # Liste der Motoren, Reihenfolge: 0 = Unten, 1 = Oben
        for value in range(0, 2):  # Erstellung der Motor-Objekte
            self.__motoren[value] = func.Motor(value, self.__servos, self.__db_connect)

    def print_start(self):
        # Initiale Ausgabe auf der Konsole
        print(f"""    ---Sonnenlicht-Sensor---
            Anzahl der Sensoren: {func.Sensor.anzahl} 
            Anzahl der Motoren:  {func.Motor.anzahl} 
            Initiale Werte: {[s.akt_wert() for s in self.__sens]} 
            Zum Abbrechen: CTRL+C""")

    def run(self):
        while True:
            # Fortlaufende Anzeige der Werte auf der Konsole (falls aktiviert)
            if self.__anzeige:
                print(f"Sensor {self.__sens[0].nummer()}: {self.__sens[0].akt_wert()}\
                {self.__sens[1].nummer()}: {self.__sens[1].akt_wert()}\
                {self.__sens[2].nummer()}: {self.__sens[2].akt_wert()}\
                {self.__sens[3].nummer()}: {self.__sens[3].akt_wert()}\
                Motor {self.__motoren[0]._kanal}: {self.__motoren[0].current_pos_grad}\
                {self.__motoren[1]._kanal}: {self.__motoren[1].current_pos_grad}")

            # Zwischenspeicherung der Positionen
            pos_temp_0, pos_temp_1 = self.__motoren[0].current_pos_grad, self.__motoren[1].current_pos_grad

            # Aufruf der eigentlichen Funktionen. Kern des Programms.
            # -----------------------
            self.__motoren[0].bewegung_horizontal(self.__sens[1], self.__sens[3], self.__schwellwert)  # Unterer Motor
            self.__motoren[1].bewegung_vertikal(self.__sens[0], self.__sens[2], self.__schwellwert)  # Oberer Motor
            # -----------------------

            # Abgleich der Positionen. Falls abweichend: Datenbankeintrag
            if pos_temp_0 != self.__motoren[0].current_pos_grad or pos_temp_1 != self.__motoren[1].current_pos_grad:
                self.__db_connect.insert_aktuelle_position(self.__motoren[0].current_pos_grad, self.__motoren[1].current_pos_grad)


# Start Application
SunfollowerApplication()
