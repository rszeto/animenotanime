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
			$(".display-with-results").show();
			updateChart(confidences);
			scrollToDivFn("graphSection")()

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
	$(".display-with-results").hide();

	// Define allowed file types and max file size (in bytes)
	var allowedFileTypes = ["png", "jpeg", "jpg"];
	var maxFileSize = 2097152
	if(this.files && this.files[0]) {
		// Verify that the file is a supported image type by checking extension. Assumes
		// file name is in standard format (###.EXT)
		var file = this.files[0]
		var ext = file.name.split(".").pop();
		if($.inArray(ext, allowedFileTypes) > -1) {
			// Check that file is small enough
			if(file.size < maxFileSize) {
				var reader = new FileReader();
				reader.addEventListener("load", function() {
					$("#imagePreview").attr("src", reader.result);
					$("#uploadImageSection").show();
					scrollToDivFn("uploadImageSection")()
				}, false);
				reader.readAsDataURL(this.files[0]);
			}
			else {
				showError("File is too large. Please select a file less than 2 MB.");
				resetChosenFile($("#imageSubmitFormImageInput"));
				$("#uploadImageSection").hide();
			}
		}
		else {
			showError("Unsupported file type. Please select a png, jpeg, or jpg image.");
			resetChosenFile($("#imageSubmitFormImageInput"));
			$("#uploadImageSection").hide();
		}
	}
}

function showError(message) {
	// Change and show error message
	$("#errorMessage").html(message);
	$("#errorModal").modal('show');
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

function scrollToDivFn(divId) {
	return function(e) {
		$("html, body").stop().animate({
	        scrollTop: $("#" + divId).offset().top
	    }, 1250, "easeInOutExpo");
	}
}

// Returns a handler that unmutes the given sound and removes itself
function unmuteSoundHandler(sound) {
	var ret = function() {
		sound.muted = false;
		sound.removeEventListener("ended", ret);
	}
	return ret;
}

// Play webpage sounds silently. When added to a button click handler, this forces the sounds
// to load. This hack is required to play sounds on mobile.
function playSoundsSilently() {
	var soundVars = [animeSounds, animeLowConfSounds, notAnimeSounds, notAnimeLowConfSounds];
	for(var i = 0; i < soundVars.length; i++) {
		for(var j = 0; j < soundVars[i].length; j++) {
			var curSound = soundVars[i][j];
			var unmuteCurSoundFn = unmuteSoundHandler(curSound);
			// Mute sound before playing
			curSound.muted = true;
			// Add handler that unmutes sound after it plays
			curSound.addEventListener("ended", unmuteCurSoundFn);
			// Start playing the sound
			curSound.play();
		}
	}
}

// Initialize page after document is loaded
$(function() {
	$("#tryItButton").click(scrollToDivFn("selectImageSection"));
	$("#imageSubmitFormImageInput").change(onFileChosen);
	// Load sounds by playing them silently on click
	$("#imageSubmitFormImageInput").click(playSoundsSilently);
	$("#uploadButton").click(onSubmitImage);
	$("#tryAgainButton").click(scrollToDivFn("selectImageSection"));
	animeSounds = $(".animeSound");
	animeLowConfSounds = $(".animeLowConfSound");
	notAnimeSounds = $(".notAnimeSound");
	notAnimeLowConfSounds = $(".notAnimeLowConfSound");
	chart = createChart();
	chart.render();
});