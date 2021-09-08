const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader');
const CopyPlugin = require('copy-webpack-plugin');


module.exports = {
  devtool: 'source-map',
  
  entry: {
    main: './assets/index.js',
    ranking_browser: './assets/ranking_browser.js',
    message_popup: './assets/message_popup.js',
    contact_form: './assets/contact_form.js',
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, './dist'),
  },

  module: {

    rules: [{
      test: /\.s?css$/,
      use: [
        MiniCssExtractPlugin.loader,
        'css-loader',
        'sass-loader'
      ]
    }, {
      test: /\.vue$/,
      loader: 'vue-loader'
    }, {
      test: /\.(woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?|otf)$/,
      loader: 'url-loader',
      options: {
        mimetype: 'application/font-woff',
      }
    }, {
      test: /\.(ttf|eot|svg|ico|jpg|bmp)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
      loader: 'file-loader'
    }]
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css'
    }),
    new VueLoaderPlugin(),
    new CopyPlugin({
      patterns: [
        { from: './static', to: 'static' },
      ],
    }),
  ],

  optimization: {
    minimize: true,  // to minimize also for development
    minimizer: [
      new CssMinimizerPlugin(),
    ],
  },

};