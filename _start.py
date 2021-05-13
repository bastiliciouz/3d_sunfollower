#!/usr/bin/python3.7
# -*-coding: utf-8-*-

import board
import busio
import adafruit_ads1x15.ads1115 as ads
import Adafruit_PCA9685 as pca
import functions as func                # functions.py
import database as db                   # database.py

i2c_bus = busio.I2C(board.SCL, board.SDA)       # Initialisierung I2C Bus
ad_wandler = ads.ADS1115(i2c_bus)               # Initialisierung AD-Wandler
servos = pca.PCA9685()                          # Initialisierung PWM Treiber mit Default Adresse 8x40
servos.set_pwm_freq(60)                         # Frequenz in Hz für PWM

schwellwert = 200                               # Definierter Schwellwert um Änderungen auszulösen
anzeige = True                                  # Anzeige auf Kommandozeile an = True oder aus = False

# Initialisierung aller Sensor-Objekte
sens = list(range(4))                           # Liste der Sensoren
kanaele = [ads.P0, ads.P1, ads.P2, ads.P3]      # Kanäle des AD Reihenfolge: OL = 3, OR = 0, UL = 2, UR = 1
for value in range(0, 4):                       # Erstellung der Sensor-Objekte
    nummer = value
    kanal = kanaele[value]
    sens[value] = func.Sensor(nummer, ad_wandler, kanal)

# Initialisierung aller Motor-Objekte
motoren = list(range(2))                        # Liste der Motoren, Reihenfolge: 0 = Unten, 1 = Oben
for value in range(0, 2):                       # Erstellung der Motor-Objekte
    motoren[value] = func.Motor(value, servos)

# Initiale Ausgabe auf der Konsole
print(f"""    ---Sonnenlicht-Sensor---
    Anzahl der Sensoren: {func.Sensor.anzahl} 
    Anzahl der Motoren:  {func.Motor.anzahl} 
    Initiale Werte: {[s.akt_wert() for s in sens]} 
    Zum Abbrechen: CTRL+C""")


while True:
    # Fortlaufende Anzeige der Werte auf der Konsole (falls aktiviert)
    if anzeige:
        print(f"Sensor {sens[0].nummer()}: {sens[0].akt_wert()}\
        {sens[1].nummer()}: {sens[1].akt_wert()}\
        {sens[2].nummer()}: {sens[2].akt_wert()}\
        {sens[3].nummer()}: {sens[3].akt_wert()}\
        Motor {motoren[0].__kanal}: {motoren[0].current_pos_grad}\
        {motoren[1].__kanal}: {motoren[1].current_pos_grad}")

    # Zwischenspeicherung der Positionen
    pos_temp_0, pos_temp_1 = motoren[0].current_pos_grad, motoren[1].current_pos_grad

    # Aufruf der eigentlichen Funktionen. Kern des Programms.
    # -----------------------
    motoren[0].bewegung_horizontal(sens[1], sens[3], schwellwert)       # Unterer Motor
    motoren[1].bewegung_vertikal(sens[0], sens[2], schwellwert)         # Oberer Motor
    # -----------------------

    # Abgleich der Positionen. Falls abweichend: Datenbankeintrag
    if pos_temp_0 != motoren[0].current_pos_grad or pos_temp_1 != motoren[1].current_pos_grad:
        db.aktuell(motoren[0].current_pos_grad, motoren[1].current_pos_grad)
