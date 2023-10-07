
// profit monthly
var optionsprofit = {
    labels: ['Linux', 'intro to python', 'intro to arduino'],
    series: [18, 25, 20],
    chart: {
      type: 'donut',
      height: 300,
    },
    dataLabels: {
          enabled: false
    },
    legend: {
        position: 'bottom',
        fontSize: '14px',
        fontFamily: 'Rubik, sans-serif',
        fontWeight: 500,
        labels: {
          colors: ["var(--chart-text-color)"],
        },
        markers: {
          width: 6,
          height: 6,
        },
        itemMargin: {
          horizontal: 7,
          vertical: 0
        },
    },
    stroke: {
      width: 10,
      colors: ["var(--light2)"],
    },
     plotOptions: {
      pie: {
        expandOnClick: false,
        donut: {
          size: '83%',
           labels: {
              show: true,
              name: {
                offsetY: 4,
              },
              total: {
                show: true,
                fontSize: '20px',
                fontFamily: 'Rubik, sans-serif',
                fontWeight: 500,
                label: '$ 7K',
                formatter: () => 'Total Profit'
              }
            },
        }
      }
    },
    states: {
      normal: {
          filter: {
              type: 'none',
          }
      },
      hover: {
          filter: {
              type: 'none',
          }
      },
      active: {
          allowMultipleDataPointsSelection: false,
          filter: {
              type: 'none',
          }
      },
    },
    colors: ["#54BA4A", "var(--theme-deafult)", "#FFA941"],
  responsive: [{
    breakpoint: 1630,
    options: {
      chart: {
        height: 360
      },
    }
  },
  {
    breakpoint: 1584,
    options: {
      chart: {
        height: 400
      },
    }
  },
  {
    breakpoint: 1473,
    options: {
      chart: {
        height: 250
      },
    }
  },
  {
    breakpoint: 1425,
    options: {
      chart: {
        height: 270
      },
    }
  },
  {
    breakpoint: 1400,
    options: {
      chart: {
        height: 320
      },
    }
  },
  {
    breakpoint: 480,
    options: {
      chart: {
        height: 250
      },
      
    }
  }]
};

var chartprofit = new ApexCharts(document.querySelector("#profitmonthly"), optionsprofit);
chartprofit.render()
// overview chart
var optionsoverview = {
    series: [ 
  {
    name: 'Succes',
    type: 'area',
    data: [35, 30, 23, 40, 50, 35, 40, 52, 67, 50, 55]
  },
  {
    name: 'Fail',
    type: 'area',
    data: [25, 20, 15, 25, 32, 20, 30, 35, 23, 30, 20]
  },
],
    chart: {
    height: 300,
    type: 'line',
    stacked: false,
    toolbar: {
      show: false
    },
    dropShadow: {
        enabled: true,
        top: 2,
        left: 0,
        blur: 4,
        color: '#000',
        opacity: 0.08
    }
  },
  stroke: {
    width: [2, 2, 2],
    curve: 'smooth'
  },
  grid: {
    show: true,
    borderColor: 'var(--chart-border)',
    strokeDashArray: 0,
    position: 'back',
    xaxis: {
        lines: {
            show: true
        }
    },   
    padding: {
        top: 0,
        right: 0,
        bottom: 0,
        left: 0
    },  
  },
  plotOptions: {
    bar: {
      columnWidth: '50%'
    }
  },
  colors: ["#7064F5", "#54BA4A", "#FF3364"],
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'light',
      type: "vertical",
      opacityFrom: 0.4,
      opacityTo: 0,
      stops: [0, 100]
    }
  },
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
    'Aug', 'Sep', 'Oct', 'Nov'
  ],
  markers: {
    discrete: [{
        seriesIndex: 0,
        dataPointIndex: 2,
        fillColor: '#7064F5',
        strokeColor: 'var(--white)',
        size: 5,
        sizeOffset: 3
      }, {
        seriesIndex: 1,
        dataPointIndex: 2,
        fillColor: '#54BA4A',
        strokeColor: 'var(--white)',
        size: 5,
      },
      {
        seriesIndex: 2,
        dataPointIndex: 2,
        fillColor: '#FF3364',
        strokeColor: 'var(--white)',
        size: 5,
      },
      {
        seriesIndex: 0,
        dataPointIndex: 5,
        fillColor: '#7064F5',
        strokeColor: 'var(--white)',
        size: 5,
        sizeOffset: 3
      }, {
        seriesIndex: 1,
        dataPointIndex: 5,
        fillColor: '#54BA4A',
        strokeColor: 'var(--white)',
        size: 5,
      },
      {
        seriesIndex: 2,
        dataPointIndex: 5,
        fillColor: '#FF3364',
        strokeColor: 'var(--white)',
        size: 5,
      },
      {
        seriesIndex: 0,
        dataPointIndex: 9,
        fillColor: '#7064F5',
        strokeColor: 'var(--white)',
        size: 5,
        sizeOffset: 3
      }, {
        seriesIndex: 1,
        dataPointIndex: 9,
        fillColor: '#54BA4A',
        strokeColor: 'var(--white)',
        size: 5,
      },
      {
        seriesIndex: 2,
        dataPointIndex: 9,
        fillColor: '#FF3364',
        strokeColor: 'var(--white)',
        size: 5,
      },
    ],
    hover: {
      size: 5,
      sizeOffset: 0
    }
},
  xaxis: {
    type: 'category',
    tickAmount: 4,
    tickPlacement: 'between',
    tooltip: {
      enabled: false,
    },
    axisBorder: {
       color: 'var(--chart-border)',
    },
    axisTicks: {
      show: false
    }
  },
  legend: {
    show: false,
  },
  yaxis: {
    min: 0,
    tickAmount: 6,
    tickPlacement: 'between',
  },
  tooltip: {
    shared: false,
    intersect: false,
  },
  responsive: [{
    breakpoint: 1200,
    options: {
      chart: {
        height: 250,
      }
    },
  }]

};

var chartoverview = new ApexCharts(document.querySelector("#orderoverview"), optionsoverview);
chartoverview.render();





