let imageData = null;

const fileInput = document.getElementById('fileInput');
const thresholdSlider = document.getElementById('threshold');
const runButton = document.getElementById('runButton');
const segMethodSelector = document.getElementById('segMethod');
const thresholdSection = document.getElementById('thresholdSection');
const calcThresholdLabel = document.getElementById('calculatedThresholdLabel');
const calcThreshold = document.getElementById('calculatedThreshold');

// Load image preview
fileInput.addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = function(e) {
    imageData = e.target.result;
    document.getElementById('preview').src = imageData;
    document.getElementById('processedPreview').src = '';
    document.getElementById('grayscaledPreview').src = '';
    document.getElementById('binaryPreview').src = '';
    hideCalcThreshold();
  };
  if (file) reader.readAsDataURL(file);
});

// Change threshold method
segMethodSelector.addEventListener('change', function() {
  resetImages();
  hideCalcThreshold();
  thresholdSection.style.display = segMethodSelector.value === 'threshold' ? 'block' : 'none';
});

// Sync slider ↔ input
thresholdSlider.addEventListener('input', () => {
  document.getElementById('thresholdInput').value = thresholdSlider.value;
});

document.getElementById('thresholdInput').addEventListener('input', () => {
  let val = parseInt(document.getElementById('thresholdInput').value);
  if (isNaN(val)) val = 0;
  val = Math.min(255, Math.max(0, val));
  thresholdSlider.value = val;
});

// Run segmentation
runButton.addEventListener('click', function () {
  if (!imageData) return alert("Please upload an image first.");

  const method = segMethodSelector.value;

  eel.grayscale_image(imageData)(res => {
    document.getElementById('grayscaledPreview').src = res;
  });

  if (method === 'threshold') {
    const t = parseInt(document.getElementById('thresholdInput').value);
    eel.process_threshold_with_boxes(imageData, t)(res => {
      document.getElementById('binaryPreview').src = res.binary;
      document.getElementById('processedPreview').src = res.boxed;
      showInfo(`Objects detected: ${res.count}`);
    });
  } else if (method === 'otsu') {
    eel.process_otsu_with_boxes(imageData)(res => {
      document.getElementById('binaryPreview').src = res.binary;
      document.getElementById('processedPreview').src = res.boxed;
      showInfo(`Otsu threshold: ${res.threshold}, Objects: ${res.count}`);
    });
  } else if (method === 'adaptiveMean') {
    eel.process_adaptive_mean_with_boxes(imageData)(res => {
      document.getElementById('binaryPreview').src = res.binary;
      document.getElementById('processedPreview').src = res.boxed;
      showInfo(`Objects detected: ${res.count}`);
    });
  }
});

function resetImages() {
  document.getElementById('grayscaledPreview').src = '';
  document.getElementById('processedPreview').src = '';
  document.getElementById('binaryPreview').src = '';
}

function hideCalcThreshold() {
  calcThreshold.style.display = 'none';
  calcThresholdLabel.style.display = 'none';
}

function showInfo(text) {
  calcThresholdLabel.style.display = 'inline-block';
  calcThreshold.style.display = 'inline-block';
  calcThreshold.textContent = text;
}
