var key = "0MJ5v-KSNMbINd3EB5H_Ew";
var host = "http://oec-2018.herokuapp.com/api";

$( document ).ready( function() {
    // Get list of stocks
    $.getJSON(host+"/stock/list", {key: key}).done(function(data) {
        console.log(data);
        // Generate chart
        var chart = c3.generate({
            bindto: '#chart',
            data: {
                columns: []
            }
        });    
        // Get prices for each ticker and load in chart
        data["stock_tickers"].sort().forEach(ticker => {
            $("#buttons").append(`<button id="${ticker}">${ticker}</button>`);
            $(`#${ticker}`).click(function () {
                $.getJSON(host+"/stock", {ticker: ticker, key:key}).done(function(data) {
                    historical_price = [ticker].concat(data["historical_price"]);
                    chart.load({
                        columns:[historical_price]
                    });
                });
            });
        });
    });
    // Get current account status
    $.getJSON(host+"/account", {key:key}).done(function(data) {
        console.log(data);
        // Update cash on hand
        $("#cash").text(data["cash"]);
        // Update holdings status
        var total = data["cash"];
        data["holdings"].forEach(x => {
            var change = (x["market_value"] - x["book_cost"])/x["book_cost"]*100;
            var data_string = `<div><code>${x["ticker"]}: ${x["market_value"]}, Δ:${change.toFixed(2)}%</code ></div>`;
            $("#holdings").append(data_string);
            total += x["market_value"];
        });
        // Update total change
        $("#total").text(`${(((total - 10000000)/10000000)*100).toFixed(2)}%`);
    });
});