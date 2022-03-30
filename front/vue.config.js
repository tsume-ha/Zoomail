const BundleTracker = require("webpack-bundle-tracker");
const MomentLocalesPlugin = require("moment-locales-webpack-plugin");
// const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin

module.exports = {
  pages: {
    public: {
      entry: "./src/public.js",
      publicPath: "/static/dist/"
    },
    private: {
      entry: "./src/private.js",
      publicPath: "/static/dist/"
    },
  },
  //サーバーを起動した時のルートパス
  publicPath: process.env.NODE_ENV === "production"
    ? "/static/dist/"
    : "http://localhost:8080/static/dist/",
  //ここで指定した場所で展開する
  outputDir: "../static/dist/",
  //outputDir起点でstaticファイルを格納する場所を指定
  assetsDir: "./",

  pwa: {
    manifestPath: "manifest.json",
    workboxOptions: {
      runtimeCaching: [{
        urlPattern: /\/api\/.+/,
        handler: "StaleWhileRevalidate",
        options: {
          cacheName: "api",
          expiration: {
            maxAgeSeconds: 60 * 60 * 24
          },
          cacheableResponse: {
            statuses: [0, 200]
          }
        }
      }]
    },
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