'use strict'

var m = require('mithril')

module.exports = {
  getRouteParams: function () {
    const routeParams = m.route.param()
    return {
      currency: (routeParams.currency || 'total').toLowerCase(),
      period: (routeParams.period || 'hour').toLowerCase()
    }
  },
  setRouteParams: function (currency, period) {
    m.route.set('/:currency/:period', {
      currency: currency || m.route.param().currency || 'total',
      period: period || m.route.param().period || 'hour'
    })
  }
}
