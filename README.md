# Smartschool
## Web application displaying data from local sensors at our school classrooms

## Server
Based on Python/Flask framework

#Authors
jozef-sabo , KlaraHirm

## Web
Based on HTML, CSS.

#Authors
ErikB17 

## Our architecture:
![unnamed](https://user-images.githubusercontent.com/70195350/128141327-cf56d354-5d90-449a-bfff-03e0aa7d969b.png)

## Demonstration:
![GIF3](https://user-images.githubusercontent.com/70195350/128141351-01841a4f-af0a-467c-8141-2bd0c1e6cc7e.gif)

## Tutoriál ako si naflashovať esp na software Tasmota
### 1. Hardware, ktorý budeme potrebovať: esp8266, USB-a na USB-mini kábel.
### 2. Software, ktorý budeme potrebovať: [driver na esp](https://www.driverscape.com/download "Driver download"), [tasmota.bin](http://ota.tasmota.com/tasmota/tasmota.bin "Download tamota.bin"), [Tasmotizer](https://github.com/tasmota/tasmotizer "Download Tasmotizer").
### Zapojíme esp8266 do počítača, pokiaľ máme problém s načítaním portov v device manageri musíme si nainštalovať driver, po nainštalovaní driveru sa nám zobrazí esp8266 v device manageri s príslušným portom. Otvoríme si flashovací program Tasmotizer, vyberieme si com-port ktorý prináleží našej doske, vyberieme BIN file:tasmota.bin a stlačíme tlačidlo Tasmotize!.
![tasmotizer](https://tasmota.github.io/docs/_media/tasmotizer1.png)




### Po tomto kroku máme nainštalovanú tasmotu na esp8266 doske. Pripojíme sa k nej skrz wifi sieť ![WIFI](https://tasmota.github.io/docs/_media/wificonfig2.jpg) a nastavíme jej AP1 SSid a AP1 Password.
![config](https://user-images.githubusercontent.com/5904370/68961890-a242c480-07d3-11ea-912f-b45464104f2c.png)






### Po uložení sa nám esp8266 reštartuje a automaticky pripojí ku sieti na ktorú sme ho nastavili. Už ju môžeme konfigurovať pomocou lokálnej siete. 

#Authors
MachiYm

# Smartaquarium
## Web application displaying data and controlling local sensors in a turtle aquarium

## Our architecture:
![arcgh](https://user-images.githubusercontent.com/70195350/128142682-c7ea4688-f724-449d-9312-383084c93748.png)

## 3D printed feeder with an An Archimedes' screw:
![krmidlo](https://user-images.githubusercontent.com/70195350/128142827-6232547d-eb0c-4d19-baac-4a12b9f33cb7.jpg)

## Demonstration:
![GIF1](https://user-images.githubusercontent.com/70195350/128142856-12d7e71b-583f-495f-b9a3-d41b6367525d.gif)

#Authors:
ErikB17 , jozef-sabo , KlaraHirm
