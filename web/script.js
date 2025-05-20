let imageData = null;

const fileInput = document.getElementById('fileInput');
const thresholdSlider = document.getElementById('threshold');
const thresholdValueLabel = document.getElementById('thresholdValue');
const runButton = document.getElementById('runButton');
const segMethodSelector = document.getElementById('segMethod');
const thresholdSection = document.getElementById('thresholdSection');
const calcThresholdLabel = document.getElementById('calculatedThresholdLabel');
const calcThreshold = document.getElementById('calculatedThreshold');

// Handle file input change
fileInput.addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = function(e) {
    imageData = e.target.result;
    document.getElementById('preview').src = imageData;
    document.getElementById('processedPreview').src = ''; 
    document.getElementById('grayscaledPreview').src = '';
    hideCalcThreshold();
  };
  if (file) reader.readAsDataURL(file);
});

// Handle segmentation method selection change
segMethodSelector.addEventListener('change', function() {
  const selectedMethod = segMethodSelector.value;
  resetImages();
  hideCalcThreshold();

  if (selectedMethod === 'threshold') {
    thresholdSection.style.display = 'block';  // Show threshold section
  } else {
    thresholdSection.style.display = 'none';   // Hide threshold section for other methods
  }
});

// Sync slider → input for threshold
thresholdSlider.addEventListener('input', () => {
  document.getElementById('thresholdInput').value = thresholdSlider.value;
});

// Sync input → slider for threshold
document.getElementById('thresholdInput').addEventListener('input', () => {
  let val = parseInt(document.getElementById('thresholdInput').value);
  if (isNaN(val)) val = 0;
  val = Math.min(255, Math.max(0, val));
  document.getElementById('thresholdInput').value = val;
  thresholdSlider.value = val;
});

// Handle segmentation button click
runButton.addEventListener('click', function () {
  if (!imageData) {
    alert("Please upload an image first.");
    return;
  }

  const method = segMethodSelector.value;

  eel.grayscale_image(imageData)(function(response) {
      document.getElementById('grayscaledPreview').src = response;
    });

  if (method === 'threshold') {
    
  
    const threshold = parseInt(document.getElementById('thresholdInput').value);
    eel.process_threshold(imageData, threshold)(function(response) {
      document.getElementById('processedPreview').src = response;
      calcThreshold.style.display = 'none';
    });
  }
  else if (method === 'otsu') {
    eel.process_otsu_threshold(imageData)(function(response) {
      document.getElementById('processedPreview').src = response[0];
      calcThresholdLabel.style.display = 'inline-block';
      calcThreshold.style.display = 'inline-block';
      calcThreshold.textContent = response[1];
    });
  } 
  else if (method == 'adaptiveMean') {
    eel.process_adaptive_mean_threshold(imageData)(function(response) {
      document.getElementById('processedPreview').src = response;
      calcThreshold.style.display = 'none';
    })
  }
  // else if (method === 'adaptive') {
  //   eel.adaptive_thresholding(imageData)(function(response) {
  //     document.getElementById('processedPreview').src = response;
  //     calcThreshold.style.display = 'block';
  //   });
  // }
});

// Initially, hide threshold section if the method is not basic thresholding
if (segMethodSelector.value !== 'threshold') {
  thresholdSection.style.display = 'none';
} else {
  hideCalcThreshold();
}

function resetImages() {
  document.getElementById('grayscaledPreview').src = '';
  document.getElementById('processedPreview').src = '';
}

function hideCalcThreshold() {
  calcThreshold.style.display = 'none';
  calcThresholdLabel.style.display = 'none';
}