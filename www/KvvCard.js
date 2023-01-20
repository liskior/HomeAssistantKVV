class KvvCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      this.innerHTML = `
        <ha-card header="KVV">
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
    n = n.map(dep => dep['number'] + " " + dep.dateTime + " " + (dep.realDateTime ? dep.realDateTime : dep.dateTime) + " (+" + (dep.delay ? dep.delay : 0) + ") " + dep.direction + " ")
    this.content.innerHTML = ''
    for (let i=0; i < n.length; i++) {
      this.content.innerHTML += n[i]
      this.content.innerHTML += '<br>'
    }
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