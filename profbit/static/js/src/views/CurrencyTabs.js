'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var Currencies = require('../models/Currencies')
var Stats = require('../models/Stats')
var Tabs = require('./Tabs')
var Utils = require('../utils/Utils')

module.exports = {
  oncreate: Tabs.oncreate,
  onupdate: Tabs.onupdate,
  view: function () {
    return <div class='col l8 s12'>
      <ul class='tabs'>
        {Currencies.map(function (currency) {
          let selectedCurrency = Utils.getRouteParams().currency
          let active = currency === selectedCurrency ? 'active' : ''
          let currentPrice = null
          if (Stats.data !== null) {
            currentPrice = Stats.data.totalInvestmentStats[currency].current_price
          }
          if (currentPrice !== null) {
            currentPrice = Stats.formatCurrency(currentPrice)
          }
          return <li class='tab col s3'>
            <a href={'#' + currency} class={active + ' inline-flex valign-wrapper flex-center'}
              onclick={function () { Utils.setRouteParams(currency, /* period= */null) }}>
              <span class={currency + '-icon currency-icon'} />
              <span class='current-price black-text'>
                {currentPrice}
              </span>
            </a>
          </li>
        })}
      </ul>
    </div>
  }
}
