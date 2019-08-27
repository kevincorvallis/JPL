var data;
// d3.csv("data/data.txt", function(data) {
//   console.log(data);
//   d3.select("svg")
//     .selectAll("g")
  data =[100, 81, 61, 54,47,6,59,519,654,1,60, 1000]

  // 3. Code here runs last, after the download finishes.
  var svgWidth = 500, svgHeight = 300, barPadding = 5;
  var barwidth = (svgWidth / data.length);

  var svg = d3.select('svg')
    .attr("width", svgWidth)
    .attr("height", svgHeight);
  var yScale = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, svgHeight]);
  var barChart = svg.selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("y", function(d) {
      return svgHeight - d;
    })
    .attr("height", function(d) {
      return d;
    })
    .attr("width", barwidth - barPadding)
    .attr("transform", function(d, i) {
      var translate = [barwidth *i, 0]; 
      return "translate(" +translate +")";
    })

    var text = svg.selectAll("text")
      .data(data)
      .enter()
      .append("text")
      .text(function(d) {
        return d;
      })
      .attr("y", function(d, i) {
        return svgHeight - d -2;
      })
      .attr("x", function(d, i) {
        return barwidth * i;
      }
      )

    
// });



// data =(await d3.csv("data.txt", ({category, val}) => ({name: category, value: +val,})))
//     .sort(value)

