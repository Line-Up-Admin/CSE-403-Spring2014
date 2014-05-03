var page = require('webpage').create();
page.open('file:///var/www/lineup/tests/angular_tests/SpecRunner.html', function(status) {

  // var title = page.evaluate(function() {
  //   return document.title;
  // });
  // console.log('Page title is ' + title);

  results = page.evaluate(function() {
    element = document.getElementsByClassName('bar');
    return element[0].textContent;
    }
  });

  console.log("Angular Tests: " + results);
  phantom.exit();
});