const btnVolcanoPlot = document.getElementById('btnVolcanoPlot');
const btnConfigureVolcanoPlot = document.getElementById('btnConfigureVolcanoPlot'); 
const closeButtonVolcanoPlot = document.getElementById('closePopupVolcanoPlot');
const popupVolcanoPlot = document.getElementById("popupVolcanoPlot");
const pvalueInput = document.getElementById("pvalue-threshold");
const logfcInput = document.getElementById("logfc-threshold");
const threshold_pvalue = 0.05;
const threshold_logfc = 2;

const volcanoPlotlayout = {
  width: '80%',
  title: 'Volcano Plot',
  xaxis: {
    title: 'Fold Change (logFC)',
    showline: true,
    showgrid: false
  },
  yaxis: {
    title: '-log10(FDR corrected - PValue)',
    showline: true,
    showgrid: false
  },
  legend: {
    title: 'Genes Significativos'
  },
  shapes: [
    {
      type: 'line',
      x0: -threshold_logfc,
      y0: 0,
      x1: -threshold_logfc,
      y1: 30,
      line: {
        color: 'gray',
        dash: 'dash'
      }
    },
    {
      type: 'line',
      x0: threshold_logfc,
      y0: 0,
      x1: threshold_logfc,
      y1: 30,
      line: {
        color: 'gray',
        dash: 'dash'
      }
    },
    {
      type: 'line',
      x0: -10,
      y0: -1 * -threshold_pvalue,
      x1: 10,
      y1: -1 * -threshold_pvalue,
      line: {
        color: 'gray',
        dash: 'dash'
      }
    }
  ]
};

function createTrace(data, color, nameTrace) {
  return {
    x: data.map(row => row.logFC),
    y: data.map(row => -1 * Math.log10(row.PValue)),
    mode: 'markers',
    text: data.map(row => row.symbol),
    marker: {
      color: color
    },
    type: 'scatter',
    name: nameTrace,
  };
}

function updateVolcanoPlot(data, pvalueThresholdinput, logfcThresholdinput) {
  const significant_genes = data.filter(row => 
    (-1 * Math.log10(row.PValue) > pvalueThresholdinput) && 
    (Math.abs(row.logFC) > logfcThresholdinput)
  );

  const trace_non_significant = createTrace(data, 'blue', 'No significant genes');
  const trace_significant = createTrace(significant_genes,'red', 'Significant genes');

  volcanoPlotlayout.shapes[0].x0 = -logfcThresholdinput;
  volcanoPlotlayout.shapes[0].x1 = -logfcThresholdinput;
  volcanoPlotlayout.shapes[1].x1 = logfcThresholdinput;
  volcanoPlotlayout.shapes[1].x0 = logfcThresholdinput;
  volcanoPlotlayout.shapes[2].y1 = -1 * -pvalueThresholdinput;
  volcanoPlotlayout.shapes[2].y0 = -1 * -pvalueThresholdinput;

  const plotDiv = 'volcanoPlot';
  Plotly.purge(plotDiv);
  Plotly.newPlot(plotDiv, [trace_non_significant, trace_significant], volcanoPlotlayout);
}

document.addEventListener("DOMContentLoaded", function() {

  pvalueInput.value = threshold_logfc;
  logfcInput.value = threshold_pvalue;

  
  axios.get('/api/differentialExpression?studyCase=13')
    .then(response => {
      
      results = response.data.results;

      $(document).ready(function() {
        const dataTable = $('#miTabla').DataTable({
          scrollX: true,
          data: results,
          columns: [
            { data: 'gene_id' },
            { data: 'symbol' },
            { data: 'group' },
            { data: 'baseMean'},
            { data: 'logFC'},
            { data: 'lfcSE'},
            { data: 'stat'},
            { data: 'PValue'},
            { data: 'FDR'}
          ]
        });
      });

      results.sort((a, b) => a.PValue - b.PValue);
      updateVolcanoPlot(results, threshold_pvalue, threshold_logfc);

      btnVolcanoPlot.addEventListener("click", function() {
        updateVolcanoPlot(results, parseFloat(pvalueInput.value), parseFloat(logfcInput.value));
        popupVolcanoPlot.classList.remove("show");
        popupVolcanoPlot.style.display = "none";
      });

      btnConfigureVolcanoPlot.addEventListener("click", function() {
        popupVolcanoPlot.classList.add("show");
        popupVolcanoPlot.style.display = "block";
      });

      closeButtonVolcanoPlot.addEventListener("click", function() {
        popupVolcanoPlot.classList.remove("show");
        popupVolcanoPlot.style.display = "none";
    });



    })
    .catch(function(error) {
      console.error('Error al obtener los datos:', error);
    });
});
