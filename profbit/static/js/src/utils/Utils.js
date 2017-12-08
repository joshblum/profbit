'use strict'

var m = require('mithril')

module.exports = {
  getRouteParams: function () {
    const routeParams = m.route.param() || {}
    return {
      currency: (routeParams.currency || 'total').toLowerCase(),
      period: (routeParams.period || 'hour').toLowerCase()
    }
  },
  setRouteParams: function (currency, period) {
    const routeParams = this.getRouteParams()
    currency = currency || routeParams.currency
    period = period || routeParams.period
    m.route.set('/:currency/:period', {
      currency: currency,
      period: period
    })
    var Stats = require('../models/Stats')
    Stats.loadData(currency, period)
  }
}
