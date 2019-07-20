//Javascript
// d3.select();
// d3.selectAll();

// d3.select('h1').style('color', 'red')
// // .attr('class','heading').text("Update");

// // d3.select('body').append('p').text("First Paragraph");


// var dataset =[1,2,3,4,5];
// d3.select('body')
//     .selectAll('p')
//     .data(dataset)
//     .enter()
//     .append('p')
//     .text(function(d){
//         return d;
//     });
// d3.selectAll('p').style('color', 'blue');


// var dataset = [80, 100, 56, 20, 12, 100];
// var svgWidth = 500, svgHeight = 300, barPadding = 6;
// var barWidth = (svgWidth / dataset.length);

// var svg = d3.select('svg')
//     .attr('width', svgWidth)
//     .attr('height', svgHeight);

// var barChart = svg.selectAll('rect')
//     .data(dataset)
//     .enter()
//     .append('rect')
//     .attr('y', function(d){
//         return svgHeight - d
//     })
//     .attr('height', function(d) {
//         return d;
//     })
//     .attr('width', barWidth - barPadding)
//     .attr('transform', function(d, i){
//         var translate = [barWidth * i, 0];
//         return 'translate('+ translate+')';
//     });
// d3.barChart

