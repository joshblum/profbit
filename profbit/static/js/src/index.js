var m = require('mithril')
var ifvisible = require('ifvisible.js')

var CurrencyTabs = require('./views/CurrencyTabs')
var PeriodTabs = require('./views/PeriodTabs')
var HistoricData = require('./views/HistoricData')
var Layout = require('./views/Layout')
var TotalData = require('./views/TotalData')
var RefreshInterval = require('./models/RefreshInterval')
var Stats = require('./models/Stats')

var TotalView = {
  render: function () {
    return <Layout tabs={<CurrencyTabs />} data={<TotalData />} />
  }
}

m.route(document.getElementById('app'), '/total', {
  '/total': TotalView,
  '/total/:period': TotalView,
  '/:currency/:period': {
    render: function () {
      return <Layout tabs={[<CurrencyTabs />, <PeriodTabs />]} data={<HistoricData />} />
    }
  },
  '/:404...': {
    render: function () {
      window.location.replace('/404')
    }
  }
})

ifvisible.onEvery(RefreshInterval.value, Stats.prefetchData)
