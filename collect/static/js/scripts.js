var signaturePad = new SignaturePad(document.getElementById('signature-pad'), {
    backgroundColor: 'rgba(255, 255, 255, 0)',
    penColor: 'rgb(0, 0, 0)',
    maxWidth: 2,
    dotSize: 2
    // onEnd: function () {
    //     signature = signaturePad.toDataURL("image/jpeg");
    //     document.getElementById('id_signatureHolder').value = signature;
    // }
});
var saveButton = document.getElementById('save');
var cancelButton = document.getElementById('clear');

saveButton.addEventListener('click', function (event) {
    var data = signaturePad.toDataURL('image/png');

    // Send data to server instead...
    window.open(data);
});

cancelButton.addEventListener('click', function (event) {
    signaturePad.clear();
});

// For High (and low) DPI screens
function resizeCanvas() {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);
    signaturePad.clear(); // otherwise isEmpty() might return incorrect value
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();