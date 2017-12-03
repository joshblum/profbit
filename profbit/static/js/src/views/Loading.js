'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var LoadingSpinner = require('./LoadingSpinner')

module.exports = {
  view: function () {
    return <div class='preloader-container container valign-wrapper flex-center'>
      <div class='preloader-wrapper big active'>
        <LoadingSpinner color='blue' />
        <LoadingSpinner color='red' />
        <LoadingSpinner color='yellow' />
        <LoadingSpinner color='green' />
      </div>
    </div>
  }
}
