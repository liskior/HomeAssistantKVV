# HomeAssistantKVV
![alt demo](https://github.com/liskior/HomeAssistantKVV/blob/main/img/demo.png)

1. Add kvv to custom components directory

2. Reload

3. Add to configuration.yaml:
```
sensor:
  - platform: kvv
    info:
      - stop_name: "Büchiger Allee"
        direction_name: "Durlacher Tor/KIT"
```
4. Reload

5. Add www directory

6. Add resource /local/kvv-card.js 
