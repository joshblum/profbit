'use strict'

var m = require("mithril")
var Stats = require("../models/Stats")
var Investment = require('./Investment')
var Loading = require('./Loading')

// Order the panels
var currencies = ['total', 'BTC', 'ETH', 'LTC']

module.exports = {
  oninit: Stats.loadData,
  view: function() {
    if (!Stats.isLoaded) {
      return <Loading />
    }
    return <div class="valign-center flex-center">
            <div class="row">
              {currencies.map(function(currency) {
                  var currencyStats = Stats.data.investmentTotals[currency]
                  return <div class="col center s12 m6">
                      <div class="card white z-depth-1">
                        <div class="card-content black-text">
                          <div class="flow-text row no-margin">
                            <div class="col s6 border-right">
                              <div class="valign-wrapper flex-center">
                                <span class={currency +  "-icon currency-icon"}></span>
                                <span class="small-caps">{ currency.toLowerCase() }</span>
                              </div>
                            </div>
                            <div class="col s6 investment-container">
                              <Investment value={currencyStats.total_investment} isReturnsData={false} />
                            </div>
                            <div class="col s6 investment-container border-right">
                              <Investment value={currencyStats.return_investment} isReturnsData={true} />
                            </div>
                            <div class="col s6 investment-container">
                              <Investment value={currencyStats.return_percent} isPercent={true} isReturnsData={true} />
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
