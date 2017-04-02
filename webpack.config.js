var webpack = require("webpack");

module.exports = {
    entry: "./frontend/js/site.js",
    output: {
        path: 'frontend/static',
        filename: "bundle.js"
    },
    externals: {
        // require("jquery") is external and available
        //  on the global var jQuery, which is loaded via CDN
        'jquery': 'jQuery'
    },
    module: {
        loaders: [
            { test: /\.css$/, loader: "style!css" }
        ]
    }
};