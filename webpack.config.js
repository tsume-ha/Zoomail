var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  mode: "development",

  context: __dirname,

  entry: {
    main: "./static/js/main.js", // エントリ名とエントリポイント
  },

  output: {
    path: path.resolve("./static/dist/"), // 出力
    filename: "[name]-[hash].js",
  },
  resolve: {
    alias: {
      vue: "vue/dist/vue.js",
    },
  },
  plugins: [new BundleTracker({ filename: "./static/dist/webpack-stats.json" })],
};
