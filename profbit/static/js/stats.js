function formatPercent(value) {
  return value.toFixed(2) + '%';
}

function formatCurrency(value, applyAbs) {
  return window.profbitContext.currencyFormatter.format(value);
}

function getColorConfig(currency) {
  return {
    BTC: {
      line: '#ffb119',
      background: '#ffecc6',
    },
    ETH: {
      line: '#6f7cba',
      background: '#e4e7f2',
    },
    LTC: {
      line: '#b5b5b5',
      background: '#ececec',
    }
  }[currency];
}

function getPeriodDescription(period) {
  return {
    'hour': 'in the past hour',
    'day': 'since yesterday',
    'week': 'since last week',
    'month': 'since last month',
    'year': 'since last year',
    'all': 'total',
  }[period];
}

function getChartConfig(graphData) {
  return {
    type: 'line',
    data: {
      datasets: [{
        data: graphData,
        type: 'line',
        pointRadius: 0,
        fill: true,
        lineTension: 0,
        borderWidth: 3,
      }]
    },
    options: {
      animation: {
        duration: 0, // general animation time
      },
      hover: {
        animationDuration: 0, // duration of animations when hovering an item
      },
      responsiveAnimationDuration: 0, // animation duration after a resize
      legend: {
        display: false,
      },
      tooltips: {
        intersect: false,
        position: 'nearest',
        callbacks: {
          beforeLabel: function(tooltipItem, data) {
            tooltipItem.yLabel = formatCurrency(tooltipItem.yLabel);
          },
        },
      },
      scales: {
        xAxes: [{
          type: 'time',
          gridLines: {
            display: false,
          },
          distribution: 'series',
          time: {
            tooltipFormat: 'MM/DD/YYYY h:mm A',
          },
        }],
        yAxes: [{
          gridLines: {
            display: false,
          },
          scaleLabel: {
            display: true,
            labelString: 'Return on investment (' + window.profbitContext.nativeCurrencySymbol + ')',
          },
          ticks: {
            // Include a currency sign in the ticks
            callback: function(value, index, values) {
              return window.profbitContext.nativeCurrencySymbol + value;
            },
          },
        }]
      }
    }
  };
}

function getGainsData(value) {
  var gainsData = {}
  if (value > 0) {
    gainsData.cls = 'positive';
    gainsData.symbol = '+';
    gainsData.description = 'gained';
  } else if (value < 0) {
    gainsData.cls = 'negative';
    gainsData.symbol = '-';
    gainsData.description = 'lost';
  } else {
    gainsData.cls = '';
    gainsData.symbol = '';
    gainsData.description = '';
  }
  gainsData.cls = gainsData.cls + '-gains gains';
  return gainsData;
}

function renderGains(selector, value, isPercent) {
  var gainsData = getGainsData(value);
  value = Math.abs(value);
  var formattedValue = isPercent ? formatPercent(value) : formatCurrency(value);
  $(selector).text(formattedValue).prepend($('<span>' + gainsData.symbol + '</span>').addClass(gainsData.cls));
  $(selector).siblings('.investment-description').text(gainsData.description);
}

function _renderCurrency(currency, periodInvestmentData) {
  var selectorId = '#' + currency;
  $(selectorId + '-Investment').text(formatCurrency(periodInvestmentData.total_investment));
  renderGains(selectorId + '-ReturnInvestment', periodInvestmentData.return_investment);
  renderGains(selectorId + '-ReturnPercent', periodInvestmentData.return_percent, /*isPercent=*/ true);
}

function renderHistoricDataContainer(currency, period) {
  var investmentData = window.profbitContext.stats[currency];
  var periodInvestmentData = investmentData[period].period_investment_data;
  var historicInvestmentData = investmentData[period].historic_investment_data;
  var colorConfig = getColorConfig(currency);

  window.profbitContext.chart.data.datasets[0].data = historicInvestmentData;
  window.profbitContext.chart.data.datasets[0].backgroundColor = colorConfig.background;
  window.profbitContext.chart.data.datasets[0].borderColor = colorConfig.line;
  window.profbitContext.chart.update();

  _renderCurrency('period', periodInvestmentData);
  $('#period-Description').text(getPeriodDescription(period));
}

function renderTotalDataContainer() {
  var stats = window.profbitContext.stats;
  var totalInvestmentData = {
    total_investment: 0,
    return_investment: 0,
    return_percent: 0,
  };
  for (var currency in stats) {
    var investmentData = stats[currency];
    var periodInvestmentData = investmentData.all.period_investment_data;
    totalInvestmentData.total_investment += periodInvestmentData.total_investment;
    totalInvestmentData.return_investment += periodInvestmentData.return_investment;
    totalInvestmentData.return_percent += periodInvestmentData.return_percent;
    _renderCurrency(currency, periodInvestmentData);
  }
  _renderCurrency('total', totalInvestmentData);
}

function render() {
  var currency = $('#currencyTabs').find('.active').data('currency');
  var period = $('#periodTabs').find('.active').data('period');
  $totalDataContainer = $('#totalDataContainer');
  $historicDataContainer = $('#historicDataContainer');
  $periodTabs = $('#periodTabs');
  if (currency === 'total') {
    $historicDataContainer.hide();
    $periodTabs.hide();
    renderTotalDataContainer();
    $totalDataContainer.show();
  } else {
    $totalDataContainer.hide();
    renderHistoricDataContainer(currency, period);
    $periodTabs.show();
    $historicDataContainer.show()
    // https://github.com/Dogfalo/materialize/issues/2102
    window.dispatchEvent(new Event('resize'));
  }
}

function getData(showLoad) {
  showLoad = showLoad || false;
  if (showLoad) {
    $('.preloader-container').show();
    $('.stats-container').hide();
  }
  $.get('/api/stats/', function(statData) {
    for (var currency in statData.stats) {
      for (var period in statData.stats[currency]) {
        var historicInvestmentData = statData.stats[currency][period].historic_investment_data;
        for (var i = 0; i < historicInvestmentData.length; i++) {
          var obj = historicInvestmentData[i];
          obj.x = new Date(obj.x * 1000);
          historicInvestmentData[i] = obj;
        }
        statData.stats[currency][period].historic_investment_data = historicInvestmentData;
      }
    }
    if (window.profbitContext) {
      window.profbitContext.stats = statData.stats;
    } else {
      window.profbitContext = {
        nativeCurrency: statData.native_currency,
        nativeCurrencySymbol: statData.native_currency_symbol,
        stats: statData.stats,
        currencyFormatter: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: statData.native_currency,
          minimumFractionDigits: 2,
          // the default value for minimumFractionDigits depends on the currency
          // and is usually already 2
        }),
      };
      var ctx = document.getElementById('historicDataChart').getContext('2d');
      cfg = getChartConfig([]);
      window.profbitContext.chart = new Chart(ctx, cfg);
    }
    render();
    if (showLoad) {
      $('.preloader-container').hide();
      $('.stats-container').show();
      // https://github.com/Dogfalo/materialize/issues/2102
      window.dispatchEvent(new Event('resize'));
    }
  });
}

$(function() {
  getData( /*showLoad=*/ true);
  $('ul.tabs').tabs({
    onShow: render,
  });
  // Poll for new data every 30seconds
  setInterval(getData, 30 * 1000);
}); // end of document ready
