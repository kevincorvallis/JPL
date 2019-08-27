
d3.csv("https://raw.githubusercontent.com/alohia/basket_shots/master/static/2013-14_shots.csv", function(data) {
// d3.csv("data/data.txt", function(data){
    var shots = d3.select("svg")
        .selectAll("g")
        .data(data)
        .enter()
        .append("g")
            .attr("class", "shots")
            .attr("transform", function(d){
                return "translate(" + 10* d.converted_y+ "," + 10 * d.converted_x +")";
            })
        .on("mouseover", function(d){
            d3.select(this).raise()
                .append("text")
                .attr("class", "playername")
                .text(d.player)
            })
        .on("mouseout", function(d){
            d3.selectAll("text.playername").remove();
            })
    shots.append("circle")
        .attr("r", 5)
        .attr("fill", function(d) {
            if(d.result == "made"){
                return "green";
            } else {
                return "red";
            }
        })
    var players = d3.nest()                     //Grouping for selector
        .key(function(d){return d.player;})     //Key is individual player
        .rollup(function(a){return a.length})   //roll up does aggregation, takes a function
        .entries(data)                          //values is data 
    

    var selector = d3.select("#selector");
    players.unshift({"key": "ALL",
                     "value" : d3.sum(players, function(d) { return d.value; })})
    selector
        .selectAll("option")
        .data(players)
        .enter()
        .append("option")
            .text(function(d) {return d.key + ":" + d.value;})
            .attr("value", function(d){ return d.key })
        
    selector //fading other players shot
        .on("change", function(){
            console.log("Apples");
            d3.selectAll(".shot")
                .attr("opacity", 1.0);
            var value = selector.property("value");
            if (value != "ALL") {
                d3.selectAll(".shot")
                    .filter(function(d) { return d.player != value; })
                    .attr("opacity", 0.1);
            }
        })
    
    })
