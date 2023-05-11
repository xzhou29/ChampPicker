const webpack = require('webpack');
const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');


module.exports = merge(common, {
  mode: 'development',

  devtool: 'inline-source-map',

  devServer: {
    hot: true,
    open: true,
    port: 5000,
    historyApiFallback: false,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        secure: false,
      },
    },
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
  ],

});
