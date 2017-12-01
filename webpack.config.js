const path = require('path')
const staticDir = './profbit/static/js'

module.exports = {
  entry: staticDir + '/src/index.js',
  output: {
    path: path.resolve(__dirname, staticDir + '/bin'),
    filename: 'app.js',
  },
  module: {
    loaders: [{
      test: /\.js$/,
      exclude: /node_modules/,
      loader: 'babel-loader'
    }]
  }
}
