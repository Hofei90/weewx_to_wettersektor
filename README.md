# Vorbereitungen

# Installation Client Skripte

## Python
Es wird mindestens Python 3.5+ vorausgesetzt

## Projekt und benötigte Module installieren

```console
apt install python3-systemd
git clone https://github.com/Hofei90/weewx_to_wettersektor.git /home/pi/weewx_to_wettersektor
pip3 install -r requirements.txt
```

Bei der Installation ist gegenfalls zu achten die Module für den passenden User
zu installieren (bsp. sudo pip3 install ... oder pip3 install --user).
Die beiliegenden Service Units sind für den User root ausgelegt


## Konfiguration anpassen

```console
cp vorlage_wettersektor_export_cfg.toml wettersektor_export_cfg.toml
nano wettersektor_export_cfg.toml
```

### Zu beachten

Wird `datei` auf false gestellt, so wird zwingend das Passwort benötigt, welches zu finden ist unter WsWin einrichten. Die 
Datenabholung muss deaktiviert sein.
Wird `datei` auf true gestellt, so muss die Datenabholung aktiviert sein. Passwort von WsWin einrichten wird nicht benötigt. 
Der Pfad pfad_wettersektor_ausgabe muss einen Pfad angeben, welcher via Internet erreichbar ist damit Wettersektor
die Datei abholen kann.

## Inbetriebnahme
Da WeeWx in der Standardinstallation mit root Rechten läuft, so benötigen auch diese Skripte root Rechte 
um auf die Datenbank von WeeWx zugreifen zu können. Somit empfiehlt es sich die root Crontab zu verwenden 
(`sudo crontab -e`)

Anstelle der Verwendung der Crontab liegen im Ordner `systemd_files` eine Systemd Service Unit mit Timer Unit
bei.
Dies stellt den **moderneren** Weg dar. Hierfür  Anleitung unter dem Punkt Systemd Unit anstelle von Cronjob beachten 

### wettersektor_export.py

#### Cronjob

````console
crontab -e
````

`*/5 * * * * python3 /home/pi/weewx_to_wettersektor/wettersektor_export.py`


### Systemd Unit
Alternativ zur Crontab kann eine Systemd Unit verwendet werden.
Hierfür die zugehörigen Dateien mit der Endung .service und .timer im systemd_files Ordner nach
`/etc/systemd/system` kopieren und die Rechte anpassen

```console
cd /home/pi/weewx_to_wettersektor/systemd_files
cp * /etc/systemd/system/
chmod 644 /etc/systemd/system/wettersektor_export.* 
```

Anschließend kann das Skript manuell getestet werden mit:
```console
systemctl start wettersektor_export.service
```

Verläuft dieser Test positiv, kann der Timer gestartet werden:
```console
systemctl start wettersektor_export.timer
systemctl enable wettersektor_export.timer
```

Bei Problemen können folgende Befehle zum Lösen hilfreich sein:

* `systemctl status wettersektor_export.serve`
* `journalctl -u wettersektor_export`

    
## RAM Datenabholung (Optional)

### Ramdisk  erstellen

    sudo su

Ordner erstellen

    mkdir /media/ramdisk
    nano /etc/fstab
    
Eintragung in fstab

    tmpfs    /media/ramdisk    tmpfs    defaults      0       0

Änderungen übernehmen mit einem Neustart oder mit dem Mount Befehl. Anschließend prüfen ob die Erstellung des Ram Speichers erfolgreich
indem eine neue Datei in den Ordner erstellt wird und anschließend neu gestartet wird

    mount -a
    touch /media/ramdisk/test.txt
    ls -l /media/ramdisk
    reboot
    ls -l /media/ramdisk

Die Datei darf beim 2. Aufruf nach dem Neustart nicht mehr vorhanden sein. 

### Apache2 Konfiguration anpassen

Hat all das geklappt wird nun der Apache 
konfiguriert, zur ermittlung der Server adressen einfach den Hostname anpingen. Innerhalb des Virtual Host wird folgendes ergänzt:

    sudo su
    nano /etc/apache2/sites-available/weewx.conf
    nano /etc/apache2/apache2.conf
    

weewx.conf (Name kann vonn sites-available bei euch abweichen!)
```
# Syntax: Alias Verzeichnisname Pfad-zum-reelen-Verzeichnis
Alias /datenabholung /media/ramdisk
<Location /datenabholung>
    # verbietet allen den Zugriff und erlaubt ihn von aufgeführten Adressen
    Order deny,allow
    deny from all
    allow from 192.168 <Serveradresse>
</Location>
```
apache2.conf
```
<Directory /media/ramdisk/>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```
Anschließend muss der Apache neu gestartet werden

    systemctl restart apache2
    exit


### wettersektor_export_cfg anpassen    

Zum Abschluss noch die Konfigurationsdatei anpassen:

    nano wettersektor_export_cfg.toml
    
wettersektor_export_cfg.toml
```
pfad_wettersektor_ausgabe = "/media/ramdisk"
pfad_ausgabe = "/media/ramdisk"
```

Und schon werden die Dateien nicht mehr auf die SD Karte geschrieben sondern in den RAM

