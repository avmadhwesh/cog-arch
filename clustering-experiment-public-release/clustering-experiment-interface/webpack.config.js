const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  mode: "development",
  output: { filename: "bundle.js" },
  target: "web",
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"]
      },
      {
        test: /\.m?js$/,
              exclude: /(node_modules|bower_components)/,
              use: { loader: 'babel-loader' }
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "index.html"
    }),
    new CopyPlugin([
      {
        from: "stimuli",
        to: "stimuli"
      }
    ])
  ],
  devServer: {
    proxy: {
      "/api": "http://localhost:5000"
    }
  },
  devtool: "source-map"
};
