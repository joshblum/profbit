'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var Stats = require('../models/Stats')

module.exports = {
  view: function (vnode) {
    let value = vnode.attrs.value
    let gainsData = this.getGainsData(value)
    value = Math.abs(value)
    let formattedValue = vnode.attrs.isPercent ? Stats.formatPercent(value) : Stats.formatCurrency(value)
    let description = vnode.attrs.isReturnsData ? gainsData.returnsDescription : gainsData.investmentDescription
    return <div>
      <span class='investment-amount'>
        <span class={gainsData.cls + '-gains gains'}>{gainsData.symbol}</span>
        {formattedValue}
      </span>
      <span class='investment-description'>
        {description}
      </span>
    </div>
  },
  getGainsData: function (value) {
    let gainsData = {}
    if (value > 0) {
      gainsData.cls = 'positive'
      gainsData.symbol = '+'
      gainsData.returnsDescription = 'gained'
      gainsData.investmentDescription = 'invested'
    } else if (value < 0) {
      gainsData.cls = 'negative'
      gainsData.symbol = '-'
      gainsData.returnsDescription = 'lost'
      gainsData.investmentDescription = 'withdrawn'
    } else {
      gainsData.cls = ''
      gainsData.symbol = ''
      gainsData.returnsDescription = ''
      gainsData.investmentDescription = 'invested'
    }
    return gainsData
  }
}
