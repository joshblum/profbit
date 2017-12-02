'use strict'

var m = require('mithril')

var Stats = {
  formatPercent: function(value) {
    return value.toFixed(2) + '%';
  },
  formatCurrency: function(value) {
    return Stats.data.currencyFormatter.format(value);
  },
  getReturnPercent: function(investment, returnInvestment) {
    let returnPercent
    if (investment == 0) {
      returnPercent = 0;
    } else {
      returnPercent = returnInvestment / investment;
    }
    return returnPercent * 100;
  },
  isLoaded: false,
  data: {},
  loadData: function() {
    return m.request({
      method: 'GET',
      url: '/api/stats'
    }).then((result) => {
      // Parse historical data
      for (var currency in result.stats) {
        for (var period in result.stats[currency]) {
          let historicInvestmentData = result.stats[currency][period].historic_investment_data
          for (var i = 0; i < historicInvestmentData.length; i++) {
            let obj = historicInvestmentData[i]
            obj.x = new Date(obj.x * 1000)
            historicInvestmentData[i] = obj
          }
          result.stats[currency][period].historic_investment_data = historicInvestmentData
        }
      }
      // Parse totals data
      let totalInvestmentData = {
        total_investment: 0,
        return_investment: 0,
        return_percent: 0,
      }
      let investmentTotals = {}
      for (var currency in result.stats) {
        let investmentData = result.stats[currency]
        let periodInvestmentData = investmentData.all.period_investment_data
        investmentTotals[currency] = periodInvestmentData
        totalInvestmentData.total_investment += periodInvestmentData.total_investment
        totalInvestmentData.return_investment += periodInvestmentData.return_investment
      }
      totalInvestmentData.return_percent = Stats.getReturnPercent(totalInvestmentData.total_investment, totalInvestmentData.return_investment)
      investmentTotals.total = totalInvestmentData

      if (Stats.isLoaded) {
        Stats.data.stats = result.stats
        Stats.data.investmentTotals = investmentTotals
      } else {
        Stats.data = {
          nativeCurrency: result.native_currency,
          nativeCurrencySymbol: result.native_currency_symbol,
          stats: result.stats,
          investmentTotals: investmentTotals,
          currencyFormatter: new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: result.native_currency,
            minimumFractionDigits: 2,
            // the default value for minimumFractionDigits depends on the currency
            // and is usually already 2
          }),
        }
      }
      Stats.isLoaded = true
    }).catch(function(e) {
      if (!Stats.isLoaded) { // Some HTTP error but not net disconnect.
        window.location.replace('/error');
      }
    })
  }
}

module.exports = Stats
