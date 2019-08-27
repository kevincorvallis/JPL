<html>

<head>
        <!-- Plotly.js -->
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <!-- D3.js -->
        <script src="https://d3js.org/d3.v4.js"></script>
        <!-- J-Qeury -->
        <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.4.1.min.js"></script>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>


      </head>
      
      <body>
        
        <div id="myDiv"><!-- Plotly chart will be drawn inside this DIV --></div>
        <script>
        //   <!-- JAVASCRIPT CODE GOES HERE -->
            function makeplot() {
            Plotly.d3.csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv", function(data){ processData(data) } );
            // Plotly.d3.csv("https://github.jpl.nasa.gov/raw/kevinl/MWG/master/d3js_projects/Idletime.csv?token=AAAeGcbzA-TEoFTGCTt3AzmSi8Lae2QLks5dQhFGwA%3D%3D", function(data){ processData(data) } );

            function makeplot() {
            Plotly.d3.csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv", function(data){ processData(data) } );

            };
                
            function processData(allRows) {

              console.log(allRows);
              var x = [], y = [], standard_deviation = [];

              for (var i=0; i<allRows.length; i++) {
                row = allRows[i];
                x.push( row['AAPL_x'] );
                y.push( row['AAPL_y'] );
              }
              console.log( 'X',x, 'Y',y, 'SD',standard_deviation );
              makePlotly( x, y, standard_deviation );
              }

              function makePlotly( x, y, standard_deviation ){
                var plotDiv = document.getElementById("plot");
                var traces = [{
                    x: x, 
                    y: y
                }];

                Plotly.newPlot('myDiv', traces, 
                    {title: 'Plotting CSV data from AJAX call'});
            };
          makeplot();

            // document.write(yValue);

            // d3.csv('https://github.jpl.nasa.gov/raw/kevinl/MWG/master/d3js_projects/Idletime.csv?token=AAAeGZ0t3GRrGaOgWasf01joBUKFHkrLks5dQguZwA%3D%3D')
            // .then(function(data) {
            //     console.log(data[0]);
            // });

            // d3.csv("idletime_drive.csv", function(error, data) {
            // if (error) throw error;
            //     console.log(data);
            //     //format data if required...
            //     //draw chart
            // });   
            // let yValue = [];
            // plotly_drive.html
            // function processData(csv) {
            //     let allTextLines = csv.split('/\r\n|\n');

            //     for (let i = 0; i < allTextLines.length; i++) {
            //         let row = allTextLines[i].split(';');
            //         let col = [];
            //         for (let j = 0; j < row.length; j++){
            //             col.push(row[j]);
            //         }
            //         attendesArray.push(col);

                    
            //     }

            // }
        
            // var yValue = [20, 14, 23];

            // var trace1 = {
            // x: xValue,
            // y: yValue,
            // type: 'bar',
            // text: yValue.map(String),
            // textposition: 'auto',
            // hoverinfo: 'none',
            // marker: {
            //     color: 'rgb(158,202,225)',
            //     opacity: 0.6,
            //     line: {
            //     color: 'rgb(8,48,107)',
            //     width: 1.5
            //     }
            // }
            // };

            // var data = [trace1];

            // var layout = {
            // title: 'January 2013 Sales Report'
            // };

            // Plotly.newPlot('myDiv', data, layout);
        </script>
      </body>

      
      
      
</html>
