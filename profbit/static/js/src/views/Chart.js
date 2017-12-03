'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var ChartJS = require('chart.js')
var Stats = require('../models/Stats')

var Chart = {
  chart: null,
  oncreate: function (vnode) {
    const ctx = vnode.dom.getContext('2d')
    let cfg = this.getChartConfig(vnode.attrs.historicInvestmentData, vnode.attrs.currency)
    this.chart = new ChartJS(ctx, cfg)
  },
  onupdate: function (vnode) {
    const colorConfig = this.getColorConfig(vnode.attrs.currency)
    this.chart.data.datasets[0].data = vnode.attrs.historicInvestmentData
    this.chart.data.datasets[0].backgroundColor = colorConfig.background
    this.chart.data.datasets[0].borderColor = colorConfig.line
    this.chart.update()
  },
  view: function (vnode) {
    return <canvas />
  },
  getColorConfig: function (currency) {
    return {
      BTC: {
        line: '#ffb119',
        background: '#ffecc6'
      },
      ETH: {
        line: '#6f7cba',
        background: '#e4e7f2'
      },
      LTC: {
        line: '#b5b5b5',
        background: '#ececec'
      }
    }[currency]
  },
  getChartConfig: function (graphData, currency) {
    const colorConfig = this.getColorConfig(currency)
    return {
      type: 'line',
      data: {
        datasets: [{
          data: graphData,
          backgroundColor: colorConfig.background,
          borderColor: colorConfig.line,
          type: 'line',
          pointRadius: 0,
          fill: true,
          lineTension: 0,
          borderWidth: 3
        }]
      },
      options: {
        animation: {
          duration: 0 // general animation time
        },
        hover: {
          animationDuration: 0 // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 0, // animation duration after a resize
        legend: {
          display: false
        },
        tooltips: {
          intersect: false,
          position: 'nearest',
          callbacks: {
            beforeLabel: function (tooltipItem, data) {
              tooltipItem.yLabel = Stats.formatCurrency(tooltipItem.yLabel)
            }
          }
        },
        scales: {
          xAxes: [{
            type: 'time',
            gridLines: {
              display: false
            },
            distribution: 'series',
            time: {
              tooltipFormat: 'MM/DD/YYYY h:mm A'
            }
          }],
          yAxes: [{
            gridLines: {
              display: false
            },
            scaleLabel: {
              display: true,
              labelString: 'Return on investment (' + Stats.data.nativeCurrencySymbol + ')'
            },
            ticks: {
              // Include a currency sign in the ticks
              callback: function (value, index, values) {
                return Stats.formatCurrency(value)
              }
            }
          }]
        }
      }
    }
  }
}

module.exports = Chart
