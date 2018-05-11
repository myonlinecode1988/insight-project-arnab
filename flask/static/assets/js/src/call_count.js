var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function(data) {
    console.log('connected');
});
//Width and height
var w = 642;
var h = 500;

//Define map projection
var projection = d3.geo.mercator()
   .center([ -120, 37 ])
   .translate([ w/2, h/2 ])
   .scale([ w*3.3 ]);

//Define path generator
var path = d3.geo.path()
 .projection(projection);


// Create SVG Element
var svg = d3.select("#chart1").append("svg")
    .attr("width", w)
    .attr("height", h);
var y = d3.scale.sqrt()
    .domain([0, 1500])
    .range([0,325]);

// Define scale to sort data values into color buckets
//var color = d3.scale.threshold()
//    .domain([1, 2, 10, 20, 50, 100, 200, 400, 1500])
//    .range(["#d1faf4","#a3f5e9","#75f0dd","#47ebd2","#19e6c7","#16caae","#12a18b","#0d7363","#08453c","#031714"]);

var color = d3.scale.threshold()
    .domain([2, 10,  50, 200, 1500])
    .range(["#d1faf4","#75f0dd","#19e6c7","#12a18b","#08453c"]);


var yAxis = d3.svg.axis()
    .scale(y)
    .tickValues(color.domain())
    .orient("right");


d3.json("../static/json/cb_2014_us_county_5m.json", function(error, ca) {
        socket.on('test', function(data) {

data_p=JSON.parse(data)
//console.log(data_p)
         for (var i = 0; i < 58; i++) {
                var dataCounty = data_p[i].Location;
                var dataCount = parseFloat(data_p[i].Count);
                //console.log(dataCounty);
                for (var j = 0; j < ca.features.length; j++) {
                        var jsonCounty = ca.features[j].properties.NAME;
                                if (dataCounty.toUpperCase() == jsonCounty.toUpperCase()) {
                                        ca.features[j].properties.population = dataCount;
                                        break;
                                }
                }
        }

 //Bind data and c$reate one path per GeoJSON feature
 svg.selectAll("path")
 .data(ca.features)
 .enter()
 .append("path")
 .attr("d", path);

var g = svg.append("g")
    .attr("class", "key")
    .attr("transform", "translate(32, 165)")
    .call(yAxis);

g.selectAll("rect")
.data(color.range().map(function(d, i) {
    return {
        y0: i ? y(color.domain()[i - 1]) : y.range()[0],
        y1: i < color.domain().length ? y(color.domain()[i]) : y.range()[1],
        z: d
    };
}))
.enter().append("rect")
    .attr("width", 8)
    .attr("y", function(d) { return d.y0; })
    .attr("height", function(d) { return d.y1 - d.y0; })
    .style("fill", function(d) { return d.z; });

 svg.selectAll(".subunit")
     .data(ca.features)
     .enter().append("path")
     .attr("d", path)
     .style("fill", function(d) {
      //console.log(d)

 var population = d.properties.population;
     if (population) {
                return color(population);
      } else {
        return "#ddd";
      }
     })
  .on("mouseover", function(d) {
      var xPosition = d3.mouse(this)[0];
      var yPosition = d3.mouse(this)[1] - 30;

      svg.append("text")
          .attr("id", "tooltip")
          .attr("x", xPosition)
          .attr("y", yPosition)
          .attr("text-anchor", "middle")
          .attr("font-family", "sans-serif")
          .attr("font-size", "15px")
          .attr("font-weight", "bold")
          .attr("fill", "black")
          .text(d.properties.NAME+','+d.properties.population);

       d3.select(this)
          .style("fill", "#509e2f");
  })
 .on("mouseout", function(d) {
 d3.select("#tooltip").remove();
 d3.select(this)
 .transition()
 .duration(250)
 .style("fill", function(d) {
        var population = d.properties.population;
        if (population) {
                return color(population);
        } else {
        return "#ddd";
        }
  		});
		});
    });

        });
