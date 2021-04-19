# Tutoriál ako si naflashovať esp na software Tasmota
## 1. Hardware, ktorý budeme potrebovať: esp8266, USB-a na USB-mini kábel.
## 2. Software, ktorý budeme potrebovať: [driver na esp](https://www.driverscape.com/download "Driver download"), [tasmota.bin](http://ota.tasmota.com/tasmota/tasmota.bin "Download tamota.bin"), [Tasmotizer](https://github.com/tasmota/tasmotizer "Download Tasmotizer").
### Zapojíme esp8266 do počítača, pokiaľ máme problém s načítaním portov v device manageri musíme si nainštalovať driver, po nainštalovaní driveru sa nám zobrazí esp8266 v device manageri s príslušným portom. Otvoríme si flashovací program Tasmotizer, vyberieme si com-port ktorý prináleží našej doske, vyberieme BIN file:tasmota.bin a stlačíme tlačidlo Tasmotize!. Po tomto kroku máme nainštalovanú tasmotu na esp8266 doske. Pripojíme sa k nej skrz wifi sieť ![WIFI](https://tasmota.github.io/docs/_media/wificonfig2.jpg) a nastavíme jej AP1 SSid a AP1 Password.
![config](https://user-images.githubusercontent.com/5904370/68961890-a242c480-07d3-11ea-912f-b45464104f2c.png)






### Po uložení sa nám esp8266 reštartuje a automaticky pripojí ku sieti na ktorú sme ho nastavili. Už ju môžeme konfigurovať pomocou lokálnej siete. 
## MachiYm