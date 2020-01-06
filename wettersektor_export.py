#!/usr/bin/python3

import datetime
import os
import time

import requests
import toml

import messwerte_umrechner as mwu
import setup_logging
import weewx_db_model as db_weewx
from peewee import fn


def config_laden():
    configfile = os.path.join(SKRIPTPFAD, "wettersektor_export_cfg.toml")
    with open(configfile) as file:
        return toml.loads(file.read())


SKRIPTPFAD = os.path.abspath(os.path.dirname(__file__))
CONFIG = config_laden()
LOGGER = setup_logging.create_logger("wettersektor_export", CONFIG["loglevel"])


class FehlerhafteSendung(Exception):
    def __init__(self):
        print("Übertragung Fehlerhaft")


def exportdaten_key_generieren():
    exportdaten = {}
    datenfelder = [
        "user", "timestamp", "datum", "uhrzeit", "usUnits",
        "outTemp", "inTemp",
        "luftdruck", "luftdrucktrend", "outLuftfeuchte", "inLuftfeuchte",
        "wind", "windrichtung", "windrichtung_grad", "windspitzetag",
        "regenaktuell", "regenlasth", "regen24h",
        "helligkeit", "sonnenzeit",
        "taupunkt", "temperaturaenderung", "uvindex",
        "tempminheute", "tempmaxheute",
        "windspitze24h", "regenHeute",
        "tempSchnittMonat", "regenMonat", "sonneMonat",
        "tempSchnittVormonat", "regenVormonat", "sonneVormonat",
        "eisTage", "frostTage", "kalteTage", "sommerTage", "heisseTage", "tropennaechte",
        "bodenTemp", "windboe", "windboe_richtung", "regenrate"]
    for datenfeld in datenfelder:
        exportdaten[datenfeld] = ""
    return exportdaten


def aktuelle_daten_laden(exportdaten):
    data = db_weewx.Archive.select().order_by(db_weewx.Archive.date_time.desc()).limit(1).execute()[0]
    exportdaten["timestamp"] = data.date_time
    exportdaten["usUnits"] = data.us_units
    date_time = datetime.datetime.fromtimestamp(data.date_time)
    exportdaten["datum"] = date_time.strftime("%d.%m.%Y")
    exportdaten["uhrzeit"] = date_time.strftime("%H:%M")
    if exportdaten["usUnits"] == 1:
        exportdaten["outTemp"] = mwu.temperaturumrechner(data.out_temp)
        exportdaten["inTemp"] = mwu.temperaturumrechner(data.in_temp)
        exportdaten["luftdruck"] = mwu.druckumrechner(data.barometer)
        exportdaten["wind"] = mwu.windumrechner(data.wind_speed)
        exportdaten["windboe"] = mwu.windumrechner(data.wind_gust)
        exportdaten["regenrate"] = mwu.regen_rate(data.rain_rate)
        exportdaten["regenaktuell"] = mwu.regen_menge(data.rain)
        exportdaten["taupunkt"] = mwu.temperaturumrechner(data.dewpoint)
        exportdaten["heatindex"] = mwu.temperaturumrechner(data.heatindex)
    else:
        exportdaten["outTemp"] = data.out_temp
        exportdaten["inTemp"] = data.in_temp
        exportdaten["luftdruck"] = data.barometer
        exportdaten["wind"] = data.wind_speed
        exportdaten["windboe"] = data.wind_gust
        exportdaten["regenrate"] = data.rain_rate
        exportdaten["regenaktuell"] = data.rain
        exportdaten["taupunkt"] = data.dewpoint
        exportdaten["heatindex"] = data.heatindex
    if isinstance(data.out_humidity, (int, float)):
        exportdaten["outLuftfeuchte"] = float(round(data.out_humidity, 0))
    else:
        exportdaten["outLuftfeuchte"] = None

    if isinstance(data.wind_dir, (int, float)):
        exportdaten["windrichtung_grad"] = float(round(data.wind_dir, 1))
    else:
        exportdaten["windrichtung_grad"] = None
    if isinstance(data.wind_gust_dir, (int, float)):
        exportdaten["windboe_richtung"] = float(round(data.wind_gust_dir, 1))
    else:
        exportdaten["windboe_richtung"] = None
    exportdaten["windrichtung"] = mwu.himmelsrichtungwandler(data.wind_dir)
    return exportdaten


def regenmenge_auslesen(timestamp):
    data = db_weewx.Archive.select(db_weewx.Archive.us_units,
                                   fn.sum(db_weewx.Archive.rain).alias("regen")).where(
        db_weewx.Archive.date_time >= timestamp).namedtuples()[0]
    if data.us_units == 1:
        regen = mwu.regen_menge(data.regen)
    else:
        regen = data.regen
    return regen


def daten_vorheriger_stunden_laden(exportdaten):
    # Berechnung des Barometertrends 3h
    # Timestamp für vor 3 Stunden
    timestamp = datetime.datetime.fromtimestamp(exportdaten["timestamp"]) - datetime.timedelta(hours=3)
    timestamp = timestamp.timestamp()

    data = db_weewx.Archive.select().where(db_weewx.Archive.date_time <= timestamp)\
        .order_by(db_weewx.Archive.date_time.desc()).limit(1).execute()[0]

    if data.us_units == 1:
        barometer = mwu.druckumrechner(data.barometer)
    else:
        barometer = data.barometer
    exportdaten["luftdrucktrend"] = round((exportdaten["luftdruck"] - barometer), 1)

    # Berechnung des Timestamp zum Begin des aktuellen Tages
    timestamp = datetime.datetime.fromtimestamp(exportdaten["timestamp"])
    timestamp = datetime.datetime(*timestamp.timetuple()[:3])  # Uhrzeit wird weggeschnitten >>Beginn 00:00Uhr
    timestamp = timestamp.timestamp()
    # Laden der Minimalen und Maximalen Temperatur und der Windspitzengeschwindigkeit des aktuellen Tages
    data = db_weewx.Archive.select(db_weewx.Archive.us_units,
                                   fn.min(db_weewx.Archive.out_temp).alias("mintemp"),
                                   fn.max(db_weewx.Archive.out_temp).alias("maxtemp"),
                                   fn.max(db_weewx.Archive.wind_gust).alias("windspitze")).where(
        db_weewx.Archive.date_time > timestamp).namedtuples()[0]
    if data.us_units == 1:
        mintemp = mwu.temperaturumrechner(data.mintemp)
        maxtemp = mwu.temperaturumrechner(data.maxtemp)
        windspitze = mwu.windumrechner(data.windspitze)
    else:
        mintemp = data.mintemp
        maxtemp = data.maxtemp
        windspitze = data.windspitze
    exportdaten["tempminheute"] = mintemp
    exportdaten["tempmaxheute"] = maxtemp
    exportdaten["windspitzetag"] = windspitze

    # Laden der Regenmenge des aktuellen Tages
    exportdaten["regenHeute"] = regenmenge_auslesen(timestamp)

    # Laden der Regenmenge der letzten Stunde
    timestamp = datetime.datetime.fromtimestamp(exportdaten["timestamp"]) - datetime.timedelta(hours=1)
    timestamp = timestamp.timestamp()
    exportdaten["regenlasth"] = regenmenge_auslesen(timestamp)

    # Laden der Regenmenge der letzten 24 Stunden
    timestamp = datetime.datetime.fromtimestamp(exportdaten["timestamp"]) - datetime.timedelta(hours=24)
    timestamp = timestamp.timestamp()
    exportdaten["regen24h"] = regenmenge_auslesen(timestamp)

    # Berechnung der Temperaturänderung der letzten Stunde
    # Timestamp für vor 1 Stunde
    timestamp = datetime.datetime.fromtimestamp(exportdaten["timestamp"]) - datetime.timedelta(hours=1)
    timestamp = timestamp.timestamp()
    data = db_weewx.Archive.select(db_weewx.Archive.us_units,
                                   db_weewx.Archive.out_temp).where(
        db_weewx.Archive.date_time <= timestamp).order_by(db_weewx.Archive.date_time.desc()).limit(1).namedtuples()[0]
    if data.us_units == 1:
        temperatur = mwu.temperaturumrechner(data.out_temp)
    else:
        temperatur = data.out_temp
    exportdaten["temperaturaenderung"] = round((exportdaten["outTemp"] - temperatur), 1)
    return exportdaten


def meterologische_tage_berechnen(exportdaten):
    """
    Tmax ≥ 35 °C: Wüstentag
    ﻿Tmax ≥ 30 °C: Heißer Tag[2]
    ﻿Tmin ≥ 20 °C: Tropennacht[2]
    ﻿Tmax ≥ 25 °C: Sommertag[2]
    ﻿Tmed < 15 °C / 12 °C: Heiztag[3]
    Tmax < 10 °C: Kalter Tag
    ﻿Tmed ≥ 5 °C: Vegetationstag[4]
    Tmin < 0 °C: Frosttag[2]
    ﻿Tmax < 0 °C: Eistag[2]
    :param exportdaten:
    :return:
    """

    met_tage = {"wuestentag": 0,
                "heissertag": 0,
                "sommertag": 0,
                "heiztag": 0,
                "kaltertag": 0,
                "vegetationstag": 0,
                "frosttag": 0,
                "eistag": 0}

    # Timestamp von 1.1 des aktuellen Jahres erzeugen
    timestamp = datetime.datetime.now()
    timestamp = datetime.datetime(timestamp.year, 1, 1).timestamp()
    # Tmin und Tmax des aktuellen Jahres für jeden Tag laden
    data = db_weewx.ArchiveDayOutTemp.select().where(
        db_weewx.ArchiveDayOutTemp.date_time >= timestamp)
    for datensatz in data:
        tmin = mwu.temperaturumrechner(datensatz.min)
        tmax = mwu.temperaturumrechner(datensatz.max)
        tmed = round((tmin + tmax) / 2, 1)
        # Bestimmen des Tagtypens
        if tmax >= 35:  # Wüstentag
            met_tage["wuestentag"] += 1
        if tmax >= 30:  # Heißer Tag
            met_tage["heissertag"] += 1
        if tmax >= 25:  # Sommertag
            met_tage["sommertag"] += 1
        if tmed < 15:  # Heiztag
            met_tage["heiztag"] += 1
        if tmax < 10:  # Kalter Tag
            met_tage["kaltertag"] += 1
        if tmed >= 5:  # Vegetationstag
            met_tage["vegetationstag"] += 1
        if tmin < 0:  # Frosttag
            met_tage["frosttag"] += 1
        if tmax < 0:  # Eistag
            met_tage["eistag"] += 1

    exportdaten["heisseTage"] = met_tage["heissertag"]
    exportdaten["sommerTage"] = met_tage["sommertag"]
    exportdaten["kalteTage"] = met_tage["kaltertag"]
    exportdaten["frostTage"] = met_tage["frosttag"]
    exportdaten["eisTage"] = met_tage["eistag"]

    exportdaten = tropennacht_berechnen(exportdaten)

    return exportdaten


def tropennacht_berechnen(exportdaten):
    """Tmin ≥ 20 °C: Tropennacht[2]"""
    anzahl_tropennacht = 0
    now = datetime.datetime.now()
    tag = datetime.datetime(now.year, 1, 1)
    while True:
        abends = tag.replace(hour=18, minute=0, second=0, microsecond=0)
        morgens = abends + datetime.timedelta(hours=12)

        if morgens > now:
            break

        data = db_weewx.Archive.select(fn.min(db_weewx.Archive.out_temp).alias("min_temp"),
                                       db_weewx.Archive.us_units).where(
            db_weewx.Archive.date_time.between(abends.timestamp(), morgens.timestamp())).namedtuples()[0]
        if data.us_units:
            tmin = mwu.temperaturumrechner(data.min_temp)
        else:
            tmin = data.min_temp
        if tmin >= 20:  # Tropennacht
            anzahl_tropennacht += 1

        tag += datetime.timedelta(days=1)
    exportdaten["tropennaechte"] = anzahl_tropennacht
    return exportdaten


def datenmonatladen(exportdaten):
    # Berechnen des Timestamps für Beginn des aktuellen Monats
    timestamp = datetime.datetime.now()
    timestamp = datetime.datetime(timestamp.year, timestamp.month, 1).timestamp()
    # Auslesen der Regenmenge im aktuellen Monat
    data = db_weewx.ArchiveDayRain.select(fn.sum(db_weewx.ArchiveDayRain.sum)).where(
        db_weewx.ArchiveDayRain.date_time >= timestamp).scalar()
    regen_monat = mwu.regen_menge(data)
    # Auslesen und berechnen des Temperaturschnittes im aktuellen Monat
    data = db_weewx.Archive.select(db_weewx.Archive.us_units,
                                   db_weewx.Archive.out_temp).where(
        db_weewx.Archive.date_time >= timestamp)
    anzahl = 0
    temp_summe = 0
    for datensatz in data:
        if datensatz.us_units == 1:
            temp = mwu.temperaturumrechner(datensatz.out_temp)
        else:
            temp = datensatz.out_temp
        if isinstance(temp, (int, float)):
            temp_summe = temp_summe + temp
            anzahl += 1
    if anzahl != 0:
        temp_schnitt_monat = round((temp_summe / anzahl), 1)
    else:
        temp_schnitt_monat = ""
    exportdaten["tempSchnittMonat"] = temp_schnitt_monat
    exportdaten["regenMonat"] = regen_monat
    return exportdaten


def datenvormonatladen(exportdaten):
    # Berechnen des Timestamps für das Vormonat und aktueller Monat
    timestamp = datetime.datetime.now()
    monat = timestamp.month
    jahr = timestamp.year
    if monat == 1:
        vormonat = 12
        vorjahr = jahr - 1
    else:
        vormonat = monat - 1
        vorjahr = jahr
    timestampvormonat = datetime.datetime(vorjahr, vormonat, 1)
    timestampvormonat = timestampvormonat.timestamp()
    timestamp = datetime.datetime(jahr, monat, 1).timestamp()

    # Auslesen der Regenmenge und Temperaturdurchschnittes im Vormonat

    data = db_weewx.Archive.select(fn.sum(db_weewx.Archive.rain).alias("regenmenge"),
                                   fn.avg(db_weewx.Archive.out_temp).alias("durchschnittstemp"),
                                   db_weewx.Archive.us_units).where(
        db_weewx.Archive.date_time.between(timestampvormonat, timestamp)
    ).namedtuples()[0]
    if data.us_units:
        regen_vormonat = mwu.regen_menge(data.regenmenge)
        temp = mwu.temperaturumrechner(data.durchschnittstemp)
    else:
        regen_vormonat = data.regenmenge
        temp = data.durchschnittstemp
    temp_schnitt_vormonat = round(temp, 1)
    exportdaten["tempSchnittVormonat"] = temp_schnitt_vormonat
    exportdaten["regenVormonat"] = regen_vormonat
    return exportdaten


def convert_to_string(exportdaten):
    for key, value in exportdaten.items():
        if value is None:
            value = ""
        exportdaten[key] = str(value)
    return exportdaten
    
    
def datenausgabe_wettersektor_datei(exportdaten):
    exportdaten = convert_to_string(exportdaten)
    exportdaten["user"] = CONFIG["wettersektor"]["username"]
    daten_liste = [exportdaten["user"], "", exportdaten["datum"], exportdaten["uhrzeit"],
                   exportdaten["outTemp"], exportdaten["luftdruck"], exportdaten["luftdrucktrend"],
                   exportdaten["outLuftfeuchte"], exportdaten["wind"], exportdaten["windrichtung"],
                   exportdaten["windspitzetag"], exportdaten["regenaktuell"], exportdaten["regenlasth"],
                   exportdaten["regen24h"], "", "", exportdaten["helligkeit"], exportdaten["sonnenzeit"],
                   exportdaten["taupunkt"], exportdaten["temperaturaenderung"], exportdaten["uvindex"],
                   exportdaten["tempminheute"], exportdaten["tempmaxheute"], exportdaten["windspitzetag"],
                   exportdaten["regenHeute"], exportdaten["tempSchnittMonat"], exportdaten["regenMonat"],
                   exportdaten["sonneMonat"], exportdaten["tempSchnittVormonat"], exportdaten["regenVormonat"],
                   exportdaten["sonneVormonat"], exportdaten["eisTage"], exportdaten["frostTage"],
                   exportdaten["kalteTage"], exportdaten["sommerTage"], exportdaten["heisseTage"],
                   exportdaten["tropennaechte"]]
    ausgabe = ";".join(daten_liste)
    ausgabe_datei = os.path.join(CONFIG["wettersektor"]["pfad_wettersektor_ausgabe"], "daten_wettersektor.txt")
    with open(ausgabe_datei, "w") as file:
        file.write(ausgabe)


def datenausgabe_wettersektor_url(exportdaten):
    exportdaten = convert_to_string(exportdaten)
    exportdaten["user"] = CONFIG["wettersektor"]["username"]
    exportdaten["pw"] = CONFIG["wettersektor"]["pw"]
    daten_liste = [exportdaten["user"], exportdaten["pw"], exportdaten["datum"], exportdaten["uhrzeit"],
                   exportdaten["outTemp"], exportdaten["luftdruck"], exportdaten["luftdrucktrend"],
                   exportdaten["outLuftfeuchte"], exportdaten["wind"], exportdaten["windrichtung"],
                   exportdaten["windspitzetag"], exportdaten["regenaktuell"], exportdaten["regenlasth"],
                   exportdaten["regen24h"], "", "", exportdaten["helligkeit"], exportdaten["sonnenzeit"],
                   exportdaten["taupunkt"], exportdaten["temperaturaenderung"], exportdaten["uvindex"],
                   exportdaten["tempminheute"], exportdaten["tempmaxheute"], exportdaten["windspitzetag"],
                   exportdaten["regenHeute"], exportdaten["tempSchnittMonat"], exportdaten["regenMonat"],
                   exportdaten["sonneMonat"], exportdaten["tempSchnittVormonat"], exportdaten["regenVormonat"],
                   exportdaten["sonneVormonat"], exportdaten["eisTage"], exportdaten["frostTage"],
                   exportdaten["kalteTage"], exportdaten["sommerTage"], exportdaten["heisseTage"],
                   exportdaten["tropennaechte"]]
    daten = ";".join(daten_liste)
    url = "http://wettersektor.de/getwett.php?val={daten}".format(daten=daten)
    server_antwort = requests.get(url)
    inhalt = server_antwort.content.decode("utf-8")
    erg = inhalt.find("S")
    if erg == -1:
        raise FehlerhafteSendung


def main():
    # Verzögerung aufgrund vom Cronjob, >>alle 5Minute, damit es nicht mit der Erstellung von Weewx kolidiert
    time.sleep(CONFIG["weewx"]["sleeptime"])

    db_adapter = CONFIG["weewx"]["db"]
    db = db_weewx.init_db(CONFIG["weewx"][db_adapter]["database"], db_adapter, CONFIG["weewx"].get(db_adapter))
    db_weewx.database.initialize(db)

    exportdaten = exportdaten_key_generieren()
    exportdaten = aktuelle_daten_laden(exportdaten)
    exportdaten = daten_vorheriger_stunden_laden(exportdaten)
    exportdaten = meterologische_tage_berechnen(exportdaten)
    exportdaten = datenmonatladen(exportdaten)
    exportdaten = datenvormonatladen(exportdaten)
    if CONFIG["wettersektor"]["datei"]:
        datenausgabe_wettersektor_datei(exportdaten)
    else:
        datenausgabe_wettersektor_url(exportdaten)


if __name__ == "__main__":
    start = datetime.datetime.now()
    LOGGER.debug("Start: ", start)
    try:
        main()
    except KeyboardInterrupt:
        LOGGER.info("Durch Benutzer abgebrochen")
    else:
        LOGGER.info("Export erfolgreich")
    ende = datetime.datetime.now()
    LOGGER.debug("Ende: ", ende)
    LOGGER.debug("Dauer: ", ende - start)
