'use strict'

var m = require('mithril')
var Currencies = require('../models/Currencies')
var Tabs = require('./Tabs')

module.exports = {
  oncreate: Tabs.oncreate,
  onupdate: Tabs.onupdate,
  view:  function() {
    return <div class="col m6 s12">
              <ul class="tabs">
                {Currencies.map(function(currency) {
                  let selectedCurrency = m.route.param().currency || ''
                  let active
                  if (currency === 'total' && (!selectedCurrency || selectedCurrency === 'total')) {
                    active = 'active'
                  } else {
                    active = currency === selectedCurrency.toUpperCase() ? 'active' : ''
                  }
                  return <li class="tab col s1 m2">
                    <a href={"#" + currency} class={active + " valign-wrapper flex-center"}
                       onclick={function() {
                         m.route.set('/:currency/:period', {
                            currency: currency,
                            period: m.route.param().period || 'hour',
                         })
                       }
                       }>
                      <span class={currency + "-icon currency-icon"}></span>
                    </a>
                  </li>
                })}
              </ul>
            </div>
  }
}
