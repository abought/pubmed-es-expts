/*
 Query elasticsearch for various information
 */

function getData(queryPayload, url) {
    url = url || 'http://localhost:9200/pubmed/article/_search';
    return $.post(url, JSON.stringify(queryPayload));
}


function getYearCounts() {
    var query = {
        "size": 0,
        "aggregations": {
            "by_year": {
                "date_histogram": {
                    "field": "date",
                    "interval": "year"
                }
            }
        }
    };
    // Get the data used to draw the histogram
    return getData(query).then(function (res) {
        return res.aggregations.by_year.buckets.map(function (item) {
            return {
                date: new Date(item.key),
                count: item.doc_count
            };
        })
    })
}

module.exports = {
    getData: getData,
    getYearCounts: getYearCounts
};