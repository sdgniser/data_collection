var palm_rest_text = document.getElementById("palm-rest-text");

$(document).ready(function () {
  var signPad = $("#smoothed").signaturePad({
    drawOnly: true,
    drawBezierCurves: true,
    lineTop: 200,
    onDraw: function () {
      palm_rest_text.style.color = "gray";
      palm_rest_text.style.opacity = "0.5";
      palm_rest_text.innerHTML = "PLEASE SIGN ABOVE";
    },
  });

  $("#upload").click(function (event) {
    signArray = signPad.getSignature();
    if (!Array.isArray(signArray) || !signArray.length) {
      palm_rest_text.style.color = "#f03030";
      palm_rest_text.style.opacity = "1";
      palm_rest_text.innerHTML = "PLEASE FILL IN ALL FIELDS AND SIGN ABOVE";
      event.preventDefault();
    } else {
      var data = signPad.getSignatureImage();
      document.getElementById("id_raw_sign").value = data;
    }
  });

  $("#app-id-ajax-warn").hide();
  $("#id_app_no").change(function () {
    var app_no = $(this).val();
    $.ajax({
      url: "/collect/validate_app_no/",
      data: {
        app_no: app_no,
      },
      dataType: "json",
      success: function (data) {
        console.log(data);
        $("#app-id-ajax-warn").html(data.status);
        $("#app-id-ajax-warn").css("color", data.color);
        $("#footer-message").hide();
        $("#app-id-ajax-warn").show();
      },
    });
  });
});
