'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var Currencies = require('./Currencies')
var PeriodIntervals = require('./PeriodIntervals')
var Utils = require('../utils/Utils')

var Stats = {
  data: null,
  loaded: null,
  pendingRequests: null,
  _getEmptyState: function () {
    var object = {total: null}
    for (let currency in Currencies) {
      currency = Currencies[currency]
      if (currency === 'total') {
        continue
      }
      object[currency] = {}
      for (let period in PeriodIntervals) {
        object[currency][period] = null
      }
    }
    return object
  },
  _setState: function (state, currency, period, value) {
    if (Stats[state] === null) {
      Stats[state] = Stats._getEmptyState()
    }
    if (currency === 'total') {
      Stats[state].total = value
    } else {
      Stats[state][currency][period] = value
    }
  },
  _getState: function (state, currency, period) {
    if (Stats[state] === null) {
      Stats[state] = Stats._getEmptyState()
    }
    if (currency === 'total') {
      return Stats[state].total
    } else {
      return Stats[state][currency][period]
    }
  },
  setPendingRequest: function (currency, period, value) {
    Stats._setState('pendingRequests', currency, period, value)
  },
  isPendingRequest: function (currency, period) {
    return Stats._getState('pendingRequests', currency, period) === true
  },
  isStatLoaded: function (currency, period) {
    return Stats._getState('loaded', currency, period) === true
  },
  setStatLoaded: function (currency, period, value) {
    Stats._setState('loaded', currency, period, value)
  },
  prefetchData: function () {
    if (!Stats.isStatLoaded('total', null)) {
      Stats.loadData('total', null)
    }
    for (let currency in Currencies) {
      currency = Currencies[currency]
      if (currency === 'total') {
        continue
      }
      for (let period in PeriodIntervals) {
        if (!Stats.isStatLoaded(currency, period)) {
          Stats.loadData(currency, period)
        }
      }
    }
  },
  _parseHistoricData: function (result, currency, period) {
    // Parse historical data
    let historicInvestmentData = result.stats[currency][period].historic_investment_data
    for (var i = 0; i < historicInvestmentData.length; i++) {
      let obj = historicInvestmentData[i]
      obj.x = new Date(obj.x * 1000)
      historicInvestmentData[i] = obj
    }
    result.stats[currency][period].historic_investment_data = historicInvestmentData
  },
  loadData: function (currency, period) {
    const routeParams = Utils.getRouteParams()
    currency = currency || routeParams.currency
    period = period || routeParams.period
    if (Stats.isPendingRequest(currency, period)) {
      return
    }
    return m.request({
      method: 'GET',
      url: '/api/stats/',
      data: {
        currency: currency,
        period: period
      },
      config: function () { Stats.setPendingRequest(currency, period, true) }
    }).then((result) => {
      Stats.setPendingRequest(currency, period, false)
      if (Stats.data === null) {
        Stats.data = {
          nativeCurrency: result.native_currency,
          nativeCurrencySymbol: result.native_currency_symbol,
          stats: {},
          totalInvestmentStats: {},
          currencyFormatter: new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: result.native_currency,
            minimumFractionDigits: 2
            // the default value for minimumFractionDigits depends on the currency
            // and is usually already 2
          })
        }
        Stats.prefetchData()
      }

      if (currency === 'total') {
        Stats.data.totalInvestmentStats = result.stats.total
      } else {
        Stats._parseHistoricData(result, currency, period)
        if (!(currency in Stats.data.stats)) {
          Stats.data.stats[currency] = {}
        }
        Stats.data.stats[currency][period] = result.stats[currency][period]
      }
      Stats.setStatLoaded(currency, period, true)
    })
    .catch(function (e) {
      Stats.setPendingRequest(currency, period, false)
      if (Stats.data === null) {
        window.location.replace('/error/')
      }
    })
  },
  formatPercent: function (value) {
    return value.toFixed(2) + '%'
  },
  formatCurrency: function (value) {
    return Stats.data.currencyFormatter.format(value)
  }
}

module.exports = Stats
