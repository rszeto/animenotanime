function onSubmitImage(e) {
	// Prevent reload
	e.preventDefault();

	var formData = new FormData($("#imageSubmitForm")[0]);
	$.ajax({
		url: "upload",
		type: "post",
		success: function(data) {
			var response = JSON.parse(data);
			var confidences = response.confidences;
			$("#graphSection").show();
			updateChart(confidences);

			// // Show success message
			// successMsg = "Successfully uploaded image.<br />";
			// successMsg += "Not anime confidence: " + confidences[0] + "<br />";
			// successMsg += "Anime confidence: " + confidences[1];
			// showSuccess(successMsg);

			// Play sound depending on not-anime confidence
			if(confidences[0] > 0.65) {
				var soundI = Math.floor(notAnimeSounds.length * Math.random());
				notAnimeSounds[soundI].play();
			}
			else if(confidences[0] > 0.5) {
				var soundI = Math.floor(notAnimeLowConfSounds.length * Math.random());
				notAnimeLowConfSounds[soundI].play();
			}
			else if(confidences[0] > 0.35) {
				var soundI = Math.floor(animeLowConfSounds.length * Math.random());
				animeLowConfSounds[soundI].play();
			}
			else {
				var soundI = Math.floor(animeSounds.length * Math.random());
				animeSounds[soundI].play();
			}
		},
		error: function(xhr, status, error) {
			var response = JSON.parse(xhr.responseText);

			// Set and show error message
			var status = response._status_code;
			var message = response.body;
			var traceback = response.traceback;
			var errorMsg = status + " error: " + message;
			if(traceback !== null) {
				// Replace newline with <br>
				traceback = traceback.replace(/(?:\r\n|\r|\n)/g, "<br />");
				errorMsg += "<br>" + traceback;
			}
			showError(errorMsg);
		},
		data: formData,
		cache: false,
		contentType: false,
		processData: false
	}, "json");
}

function onFileChosen(e) {
	// Hide the graph
	$("#graphSection").hide();

	// Make sure the file is a supported image type
	var allowedFileTypes = ["png", "jpeg", "jpg"];
	if(this.files && this.files[0]) {
		// Verify that the file is a supported image type by checking extension. Assumes
		// file name is in standard format (###.EXT)
		var file = this.files[0]
		var ext = file.name.split(".").pop();
		if($.inArray(ext, allowedFileTypes) > -1) {
			var reader = new FileReader();
			reader.addEventListener("load", function() {
				$("#imagePreview").attr("src", reader.result);
				$("#imagePreviewSection").show();
			}, false);
			reader.readAsDataURL(this.files[0]);
		}
		else {
			showError("Unsupported file type. Please select a png, jpeg, or jpg image.");
			resetChosenFile($("#imageSubmitFormImageInput"));
			$("#imagePreviewSection").hide();
		}
	}
}

function showError(message) {
	// Hide success message
	$("#successSection").hide();
	// Change and show error message
	$("#errorMessage").html(message);
	$("#errorSection").show();
}

function showSuccess(message) {
	// Hide error section
	$("#errorSection").hide();
	// Change and show success message
	$("#successMessage").html(message);
	$("#successSection").show();
}

// Resets given file selection elements as selected by jQuery
// E.g. resetChosenFile($("#elemId")))
// Source: http://jsfiddle.net/rPaZQ/
function resetChosenFile(e) {
	e.wrap("<form>").closest("form").get(0).reset();
	e.unwrap();
}

function createChart() {
	var chart = new CanvasJS.Chart("graph", {
		title:{
			text: "Probability of Anime"              
		},
		axisY: {
			minimum: 0,
			maximum: 1,
			interval: 0.2,
			gridThickness: 0
		},
		data: [              
		{
			type: "column",
			dataPoints: [
				{ label: "Not anime",  y: 0 },
				{ label: "Anime",  y: 0 }
			]
		}
		]
	});
	return chart;
}

function updateChart(probs) {
	// Set not-anime probability
	chart.options.data[0].dataPoints[0].y = probs[0]
	prob_str = (Math.round(probs[0] * 1000) / 10).toString() + "%"
	chart.options.data[0].dataPoints[0].indexLabel = prob_str
	// Set anime probability
	chart.options.data[0].dataPoints[1].y = probs[1]
	prob_str = (Math.round(probs[1] * 1000) / 10).toString() + "%"
	chart.options.data[0].dataPoints[1].indexLabel = prob_str
	chart.render()
}

// Initialize page after document is loaded
$(function() {
	$("#imageSubmitForm").submit(onSubmitImage);
	$("#imageSubmitFormImageInput").change(onFileChosen);
	animeSounds = $(".animeSound");
	animeLowConfSounds = $(".animeLowConfSound");
	notAnimeSounds = $(".notAnimeSound");
	notAnimeLowConfSounds = $(".notAnimeLowConfSound");
	chart = createChart();
	chart.render();
});