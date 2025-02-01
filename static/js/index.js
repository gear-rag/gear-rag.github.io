window.HELP_IMPROVE_VIDEOJS = false;


/* index.js - Add this new code */
$(document).ready(function() {
	// Check for click events on the navbar burger icon

	var options = {
		slidesToScroll: 1,
		slidesToShow: 1,
		loop: true,
		infinite: true,
		autoplay: true,
		autoplaySpeed: 5000,
		duration: 750,  
	}

	// Initialize all div with carousel class
	var carousels = bulmaCarousel.attach('.carousel', options);

	bulmaSlider.attach();

  
	// Tab switching functionality
	$('.tab').click(function() {
	  // Remove active class from all tabs and content
	  $('.tab').removeClass('active');
	  $('.code-content').removeClass('active');
	  
	  // Add active class to clicked tab
	  $(this).addClass('active');
	  
	  // Show corresponding content
	  const tabId = $(this).data('tab');
	  $(`#${tabId}-content`).addClass('active');
	});
  });
