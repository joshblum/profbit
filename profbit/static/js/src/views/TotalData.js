'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var Stats = require('../models/Stats')
var Currencies = require('../models/Currencies')
var InvestmentData = require('./InvestmentData')
var Loading = require('./Loading')

module.exports = {
  view: function () {
    if (!Stats.isStatLoaded('total', null)) {
      Stats.loadData()
      return <Loading />
    }
    return <div class='valign-center flex-center'>
      <div class='row'>
        {Currencies.map(function (currency) {
          var currencyStats = Stats.data.totalInvestmentStats[currency]
          return <div class='col center s12 m6'>
            <div class='card white z-depth-1'>
              <div class='card-content black-text'>
                <div class='flow-text row no-margin'>
                  <div class='col s6 border-right'>
                    <div class='valign-wrapper flex-center'>
                      <span class={currency + '-icon currency-icon'} />
                      <span class='small-caps'>{ currency.toLowerCase() }</span>
                    </div>
                  </div>
                  <div class='col s6 investment-container'>
                    <InvestmentData value={currencyStats.total_investment} />
                  </div>
                  <div class='col s6 investment-container border-right'>
                    <InvestmentData value={currencyStats.return_investment} isReturnsData />
                  </div>
                  <div class='col s6 investment-container'>
                    <InvestmentData value={currencyStats.return_percent} isPercent isReturnsData />
                  </div>
                </div>
              </div>
            </div>
          </div>
        })
            }
      </div>
    </div>
  }
}
