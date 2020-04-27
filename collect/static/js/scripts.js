var canvas = document.getElementById('signature-pad');
var palm_rest_text = document.getElementById('palm-rest-text')

var signaturePad = new SignaturePad(canvas, {
    backgroundColor: 'rgba(255, 255, 255, 0)',
    penColor: 'rgb(0, 0, 0)',
    minWidth: 1.5,
    maxWidth: 1.5,
    dotSize: 1.5,
    throttle: 0,
    velocityFilterWeight: 1,
    onBegin: function () {
        palm_rest_text.style.color = "gray";
        palm_rest_text.style.opacity = "0.5";
        palm_rest_text.innerHTML = "PLEASE SIGN ABOVE";
    }
});

// For High (and low) DPI screens
function resizeCanvas() {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);
    signaturePad.clear(); // otherwise isEmpty() might return incorrect value
}

var uploadButton = document.getElementById('upload');
var cancelButton = document.getElementById('clear');

uploadButton.addEventListener('click', function (event) {
    if (signaturePad.isEmpty()) {
        palm_rest_text.style.color = "red";
        palm_rest_text.style.opacity = "1";
        palm_rest_text.innerHTML = "PLEASE FILL IN ALL FIELDS AND SIGN ABOVE";
        event.preventDefault();
    }
    else {
        var data = signaturePad.toDataURL('image/png');
        document.getElementById('id_raw_sign').value = data;
    }
});

cancelButton.addEventListener('click', function (event) {
    signaturePad.clear();
});

window.addEventListener("resize", resizeCanvas);
resizeCanvas();