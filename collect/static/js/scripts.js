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