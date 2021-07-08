const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader');


module.exports = {
  entry: {
    main: './assets/index.js',
    ranking_browser: './assets/ranking_browser.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, './dist'),  // path to our Django static directory
  },

  module: {

    rules: [{
      test: /\.s?css$/,
      use: [
        MiniCssExtractPlugin.loader,
        "css-loader",
        "sass-loader"
      ]
    }, {
      test: /\.vue$/,
      loader: 'vue-loader'
    }],
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
      chunkFilename: "[id].css"
    }),
    new VueLoaderPlugin()
  ],

  optimization: {
    minimize: true,  // to minimize also for development
    minimizer: [
      new CssMinimizerPlugin(),
    ],
  },

};