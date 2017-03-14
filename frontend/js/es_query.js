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

/**
 * Significant terms aggregation for top keywords in a year. Will almost certainly be slow for large indices.
 * @param date
 * @returns {*}
 */
function getTermsForYear(date) {
    var year = date.getFullYear();

    var query = {
        query: {
            range: {
                date: {
                    gte: String(year),
                    lte: String(year + 1),
                    format: 'yyyy'
                }
            }
        },
        aggregations: {
            significantKeywords: {
                significant_terms: {field: 'keywords'}
            }
        }
    };

    return getData(query).then(function (res) {
        return res.aggregations.significantKeywords.buckets.map(function (item) {
            return {
                key: item.key,
                count: item.doc_count
            }
        })
    });
}

module.exports = {
    getData: getData,
    getYearCounts: getYearCounts,
    getTermsForYear: getTermsForYear
};