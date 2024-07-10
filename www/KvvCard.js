import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit-element@2.0.1/lit-element.js?module";

class KvvCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      this.innerHTML = `
        <ha-card header="`+ hass.states[this.config.entity].state + `">
          <div class="card-content"></div>
        </ha-card>
      `;
      this.content = this.querySelector('div');
    }

    const entityId = this.config.entity;
    const state = hass.states[entityId];
    let stateStr = state ? state.attributes.departures: 'unavailable';
    let n = stateStr.map(dep => dep.replace(/'/g, '"'))
    n = n.map(dep => JSON.parse(dep))
    
    
    n = n.map(dep => format(dep))
    this.content.innerHTML = ''
    for (let i=0; i < n.length; i++) {
      this.content.innerHTML += n[i]
      this.content.innerHTML += '<br>'
    }
    const style = document.createElement('style');
    style.textContent = `
            .lineNum {
              color: yellow;
              background-color: red;
              border-radius: 60px;
              padding: 4px;
              margin: 5px;
              
            }
            .time {
              position: absolute;
              left: 60px;
            }
            
            .dir {
              position: absolute;
              left: 180px;
            }
            .realTime {
              position: absolute;
              left: 110px;
              color: red;
            }
            .green {
                color: white;
                background-color: green;
            }
            .brown {
                color: white;
                background-color: #978768;
            }
            .yellow {
                color: black;
                background-color: yellow;
            }
            `
    this.content.appendChild(style)
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  getCardSize() {
    return 5;
  }
}

customElements.define('kvv-card', KvvCard);

function format(dep) {
    const time = dep.dateTime.substr(dep.dateTime.indexOf(" "))
    
    return "<div class='line'><span class='lineNum" + lineColor(dep.number) + "'>" + dep.number + "</span> <span class='time'>" + time + "</span> " + 
    (dep.delay != 0 ? " (+" + dep.delay + ") " : "") + "</span> <span class='dir'>" + dep.destination + "</span></div>"
}

function lineColor(line) {
    switch (line) {
        case "S2": return " green"
        case "4": return " yellow"
        case "3": return " brown"
        default: return ""
    }
}









