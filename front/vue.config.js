const BundleTracker = require("webpack-bundle-tracker");
const MomentLocalesPlugin = require("moment-locales-webpack-plugin");
// const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin

module.exports = {
  pages: {
    public: { entry: "./src/public.js" },
    private: { entry: "./src/private.js" },
  },
  //ここで指定した場所で展開する
  outputDir: "../templates/",
  //サーバーを起動した時のルートパス
  publicPath: process.env.NODE_ENV === "production"
    ? "/"
    : "http://localhost:8080/",
  //outputDir起点でstaticファイルを格納する場所を指定
  assetsDir: "../static/dist/",

  pwa: {
    manifestPath: "./manifest.json"
  },

  configureWebpack: {
    plugins: [
      new BundleTracker({
        filename: "../static/dist/webpack-stats.json",
        relativePath: true
      }),
      new MomentLocalesPlugin({ localesToKeep: ["ja"] }),
      // new BundleAnalyzerPlugin(),
    ],
  },
  css: {
    sourceMap: true,
    loaderOptions: {
      scss: {
        additionalData: '@import "./src/assets/sass/prepends.scss";'
      }
    }
  },
  devServer: {
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  },
};