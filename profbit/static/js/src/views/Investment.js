'use strict'

var m = require("mithril")
var Stats = require('../models/Stats')

module.exports = {
  formatPercent: function(value) {
    return value.toFixed(2) + '%';
  },
  formatCurrency: function(value) {
    return Stats.data.currencyFormatter.format(value);
  },
  getGainsData: function(value) {
    var gainsData = {}
    if (value > 0) {
      gainsData.cls = 'positive';
      gainsData.symbol = '+';
      gainsData.returnsDescription = 'gained';
      gainsData.investmentDescription = 'invested'
    } else if (value < 0) {
      gainsData.cls = 'negative';
      gainsData.symbol = '-';
      gainsData.returnsDescription = 'lost';
      gainsData.investmentDescription = 'withdrawn'
    } else {
      gainsData.cls = '';
      gainsData.symbol = '';
      gainsData.returnsDescription = '';
      gainsData.investmentDescription = 'invested'
    }
    return gainsData;
  },
  view: function(vnode) {
    var value = vnode.attrs.value
    var gainsData = this.getGainsData(value)
    value = Math.abs(value);
    var formattedValue = vnode.attrs.isPercent ? this.formatPercent(value) : this.formatCurrency(value);
    var description = vnode.attrs.isReturnsData ? gainsData.returnsDescription : gainsData.investmentDescription
    return <div>
        <span class="investment-amount">
          <span class={ gainsData.cls + "-gains gains" }>{gainsData.symbol}</span>
          {formattedValue}
        </span>
        <span class="investment-description">
          {description}
        </span>
    </div>
  }
}
