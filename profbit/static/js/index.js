(function($) {
  $(function() {
    $('.carousel.carousel-slider').carousel({
      fullWidth: true,
    });
    setInterval(function() {
      $('.carousel.carousel-slider').carousel('next');
    }, 3000);
  }); // end of document ready
})(jQuery); // end of jQuery name space
