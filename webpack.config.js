const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');


module.exports = {
  entry: './assets/index.js',  // path to our input file
  output: {
    filename: 'bundle.js',  // output bundle file name
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
    }],
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
      chunkFilename: "[id].css"
    })
  ],

  optimization: {
    minimize: true,  // to minimize also for development
    minimizer: [
      new CssMinimizerPlugin(),
    ],
  },

};