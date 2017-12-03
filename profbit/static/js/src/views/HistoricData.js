'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var Stats = require('../models/Stats')
var Chart = require('./Chart')
var InvestmentData = require('./InvestmentData')
var Loading = require('./Loading')

module.exports = {
  oninit: Stats.loadData,
  view: function (vnode) {
    if (!Stats.isLoaded) {
      return <Loading />
    }
    const routeParams = m.route.param()
    const currency = routeParams.currency.toUpperCase()
    const period = routeParams.period.toLowerCase()

    const investmentData = Stats.data.stats[currency]
    const periodInvestmentData = investmentData[period].period_investment_data
    const historicInvestmentData = investmentData[period].historic_investment_data

    return <div>
      <div class='row small-margin center flow-text border-bottom'>
        <div class='col s4 investment-container border-right'>
          <InvestmentData
            value={periodInvestmentData.total_investment} />
        </div>
        <div class='col s4 investment-container border-right'>
          <InvestmentData
            value={periodInvestmentData.return_investment}
            isReturnsData />
        </div>
        <div class='col s4 investment-container'>
          <InvestmentData
            value={periodInvestmentData.return_percent}
            isReturnsData
            isPercent />
        </div>
      </div>
      <div class='row center'>
        <div class='col s12 small-caps'>{this.getPeriodDescription(period)}</div>
      </div>
      <div class='row'>
        <div class='chart-container col s12'>
          <Chart
            historicInvestmentData={historicInvestmentData}
            currency={currency} />
        </div>
      </div>
    </div>
  },
  getPeriodDescription: function (period) {
    return {
      'hour': 'in the past hour',
      'day': 'since yesterday',
      'week': 'since last week',
      'month': 'since last month',
      'year': 'since last year',
      'all': 'total'
    }[period]
  }
}
