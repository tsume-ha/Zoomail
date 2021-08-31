var BundleTracker = require("webpack-bundle-tracker");
// var VueLoaderPlugin = require("vue-loader/lib/plugin");
// var MomentLocalesPlugin = require('moment-locales-webpack-plugin');

module.exports = {
    //ここで指定した場所で展開する
    outputDir: '../',
    //サーバーを起動した時のルートパス
    publicPath: process.env.NODE_ENV === 'production' 
        ? '/'
        : 'http://localhost:8080/',
    //outputDir起点でstaticファイルを格納する場所を指定
    assetsDir: 'static/dist',

    configureWebpack: {
        plugins: [
          new BundleTracker({ filename: "../static/dist/webpack-stats.json" }),
        //   new VueLoaderPlugin(),
        //   new MomentLocalesPlugin({ localesToKeep: ['ja'] }),
        //   new BundleAnalyzerPlugin(),
        ],
    },
    css: {
      sourceMap: true,
    },
    devServer: {
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    },
}