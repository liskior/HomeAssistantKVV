# HomeAssistantKVV
![alt demo](https://github.com/liskior/HomeAssistantKVV/blob/main/img/demo.png)

1. Add kvv to custom components directory

2. Reload

3. Add to configuration.yaml:
```
sensor:
  - platform: kvv
    info:
      - name_origin: "Karlsruhe, Hauptfriedhof"
        nameInfo_origin: '7000402'
        name_destination: "Karlsruhe Karl-Wilhelm-Platz"
        nameInfo_destination: '7000401'
  - platform: kvv
    info:
      - name_origin: "Karlsruhe, Hauptfriedhof"
        nameInfo_origin: '7000402'
        name_destination: "Karlsruhe Essenweinstraße"
        nameInfo_destination: '7000626'
```
4. Reload

5. Add www directory

6. Add resource /local/kvv-card.js 
