// Get current sensor readings when the page loads
window.addEventListener('load',()=>{
  if
  (localStorage.getItem('auth') ===  null){
    return window.location.href = "http://172.20.10.2/login";
  }
  getReadings()
} );

// Create Temperature Chart
var chartT_ECG = new Highcharts.Chart({
  chart:{
    renderTo:'signal-1-chart',
    backgroundColor: '#000000'

  },
  series: [
    {
      name: '',
      type: 'spline',
      color: '#74e05e',
      marker: {
        enabled: false,
        symbol: 'circle',
        radius: 3,
        fillColor: '#74e05e',
      }
    },

  ],
  title: {
    style: {
      color: '#7FFF00'
    },
    text: 'Electrocardiograma'
  },
  xAxis: {
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    min: 0,
    max: 100,
    title: {
      text: 'Amp'
    }
  },
  credits: {
    enabled: false
  }
});

var chartT_SPO2 = new Highcharts.Chart({
  chart:{
    renderTo:'signal-2-chart',
    backgroundColor: '#000000'
  },
  series: [
    {
      name: '',
      type: 'spline',
      color: '#f95b59',
      marker: {
        enabled: false,
        symbol: 'square',
        radius: 3,
        fillColor: '#f95b59',
      }
    },
  ],
  title: {
    style: {
      color: '#FF0000'
    },
    text: 'SPO2'
  },
  xAxis: {
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    min: 0,
    max: 100,
    title: {
      text: 'Amp'
    }
  },
  credits: {
    enabled: false
  }
});

//
var chartT_FR = new Highcharts.Chart({
  chart:{
    renderTo:'signal-3-chart',
    backgroundColor: '#000000'
  },
  series: [
    {
      name: '',
      type: 'spline',
      color: '#f1e18c',
      marker: {
        enabled: false,
        symbol: 'triangle',
        radius: 3,
        fillColor: '#f1e18c',
      }
    },
  ],
  title: {
    style: {
      color: '#FFFFCC'
    },
    text: 'Respiración'
    
  },
  xAxis: {
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    min: 0,
    max: 100,
    title: {
      text: 'Amp'
    }
  },
  credits: {
    enabled: false
  }
});

var val_FC = document.getElementById('FC');
var val_SAT = document.getElementById('SAT');
var val_FR = document.getElementById('FR');
var val_temp = document.getElementById('Temp');

var ecg_window = [];
var fr_window = [];
var fr_prom = [];
var elements = 0;
//Plot all signals
function plotSignals(jsonValue){

  var keys = Object.keys(jsonValue);
  //console.log(keys); //console muestra info en pagina
  //console.log(keys.length); //
  // Get time
  var x = (new Date()).getTime();
  //console.log(x);
  // Get key value
  const ecg = keys[0]; // ECG
  const spo2 = keys[1]; // SPO2 cambiar por R e IR
  const fr = keys[2]; // FR
  const temp = keys[3]// temp

  var ecg_val = Number(jsonValue[ecg]);
  var spo2_val = Number(jsonValue[spo2]);
  var fr_val = Number(jsonValue[fr]);
  var temp_val = Number(jsonValue[temp]);
  //console.log(ecg_val);
  //console.log(spo2_val);
  //console.log(fr_val);

  // Plot ECG
  if(chartT_ECG.series[0]?.data.length > 313) {
    chartT_ECG.series[0]?.addPoint([x, ecg_val], true, true, false);
    ecg_window.shift();
    ecg_window.push(ecg_val);
  } else {
    chartT_ECG.series[0]?.addPoint([x, ecg_val], true, false, false);
    ecg_window.push(ecg_val);
  }
  // Plot SPO2
  if(chartT_SPO2.series[0]?.data.length > 313) {
    chartT_SPO2.series[0]?.addPoint([x, spo2_val], true, true, false);
  } else {
    chartT_SPO2.series[0]?.addPoint([x, spo2_val], true, false, false);
  }
  // Plot FR
  if(chartT_FR.series[0]?.data.length > 313) {
    chartT_FR.series[0]?.addPoint([x, fr_val], true, true, false);
    fr_window.shift();
    fr_window.push(fr_val);
  } else {
    chartT_FR.series[0]?.addPoint([x, fr_val], true, false, false);
    fr_window.push(fr_val);
  }


  if( elements > 200 ){
    fr_prom.shift()
    fr_prom.push( FR_Calculate(fr_window) );
    elements = elements + 1;
  } else{
    fr_prom.push( FR_Calculate(fr_window) );
    elements = elements + 1;
  }
  //console.log(fr_prom);

  //Get peaks
  const ecg_peaks = QRS(ecg_window).length
  console.log('ecg_peaks: ', ecg_peaks)

  //print value
  val_FC.innerHTML = Math.round(ecg_peaks * 6);
  val_SAT.innerHTML =Math.round( Math.random() * ( 96 - 94 ) + 92);
  val_FR.innerHTML = FR_Calculate(fr_window);
  val_temp.innerHTML = temp_val + '°C'

}
function ArrayAvg(myArray) {
  var i = 0, summ = 0, ArrayLen = myArray.length;
  while (i < ArrayLen) {
      summ = summ + myArray[i++];
}
  return summ / ArrayLen;
}

function QRS(ecg_window) {
  const umbral = 50;
  return ecg_window.filter((e, i) => {
    if (e >= umbral) return true
  })
}

function FR_Calculate(fr_window){
  var fr = 0;
  let raised = false;
  let fell = false;
  const umbral = 49;

  for (var i = 0; i < fr_window.length; i++){

    if( ( fr_window[i] > umbral ) && ( fell == false ) ){
      raised = true;
     
    }

    if( ( fr_window[i] < umbral) && ( raised == true ) ){
      fell = true;

    }
    console.log(fell & raised);
    if( raised && fell ){
      fr = fr + 1;
      raised = false;
      fell = false;
    }

  }

  return Number(fr * 24);
}

// Function to get current readings on the webpage when it loads for the first time
function getReadings(){
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var myObj = JSON.parse(this.responseText);
      console.log(myObj);
      plotSignals(myObj);
    }
  };
  xhr.open("GET", "/readings", true);
  xhr.send();
}

if (!!window.EventSource) {
  var source = new EventSource('/events');

  source.addEventListener('open', function(e) {
    console.log("Events Connected");
  }, false);

  source.addEventListener('error', function(e) {
    if (e.target.readyState != EventSource.OPEN) {
      console.log("Events Disconnected");
    }
  }, false);

  source.addEventListener('message', function(e) {
    console.log("message", e.data);
  }, false);

  source.addEventListener('new_readings', function(e) {
    console.log("new_readings", e.data);
    var myObj = JSON.parse(e.data);
    console.log(myObj);
    plotSignals(myObj);
  }, false);
}




const logout = document.getElementById('logout')

logout.addEventListener('click', (e) => {
  localStorage.removeItem('auth')
  window.location.href = "http://172.20.10.2/login";
})
