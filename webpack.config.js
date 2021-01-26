var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");
var VueLoaderPlugin = require("vue-loader/lib/plugin");
var MomentLocalesPlugin = require('moment-locales-webpack-plugin');
var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  mode: "development",

  context: __dirname,

  entry: {
    main: "./static/js/main.js", // エントリ名とエントリポイント
  },
  output: {
    path: path.resolve("./static/dist/"), // 出力
    publicPath: '/static/dist/',// 追加
    filename: "[name]-[hash].js",
  },
  resolve: {
    alias: {
      vue: "vue/dist/vue.js",
    },
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["vue-style-loader", "css-loader"]
      },
      {
        test: /\.vue$/,
        loader: "vue-loader",
      },
    ],
  },
  plugins: [
    new BundleTracker({ filename: "./static/dist/webpack-stats.json" }),
    new VueLoaderPlugin(),
    new MomentLocalesPlugin({ localesToKeep: ['ja'] }),
    // new BundleAnalyzerPlugin(),
  ],
  resolve: {
    extensions: [".js", ".vue"],
    modules: ["node_modules"],
    alias: {
      vue: path.resolve("./node_modules/vue/dist/vue.js"),
    },
  },
};
