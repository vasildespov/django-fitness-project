(function ($) {
  $(function () {

    $('nav ul li a:not(:only-child)').click(function (e) {
      $(this).siblings('.nav-dropdown').toggle();

      $('.nav-dropdown').not($(this).siblings()).hide();
      e.stopPropagation();
    });

    $('html').click(function () {
      $('.nav-dropdown').hide();
    });

    $('#nav-toggle').click(function () {
      $('nav ul').slideToggle();
    });

    $('#nav-toggle').on('click', function () {
      this.classList.toggle('active');
    });
  });
})(jQuery);

$('.brand-img').click(function () {
  $(location).attr("href", "/");
});

// $(window).scroll(function () {
//   sessionStorage.scrollTop = $(this).scrollTop();
// });
// $(document).ready(function () {
//   if (sessionStorage.scrollTop != "undefined") {
//     $(window).scrollTop(sessionStorage.scrollTop);
//   }
// });
function previewFunc(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#preview').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$('.card.calculator').click(function(){
  $(location).attr('href', '/features/calorie-calculator/')
})
$('.card.blog').click(function(){
  $(location).attr('href', '/blog/')
})
