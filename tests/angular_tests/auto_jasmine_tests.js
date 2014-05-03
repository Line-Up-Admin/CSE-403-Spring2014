var page = require('webpage').create();
page.open('/var/www/lineup/tests/angular_tests/SpecRunner.html', function(status) {

  var title = page.evaluate(function() {
    return document.title;
  });
  console.log('Page title is ' + title);


  results = page.evaluate(function() {
    element = $('.bar.failed').text();
    if (element == undefined) {
      return "All Passed";
    } else {
      return element.text();
    }
    console.log("Angular Tests: " + results);

  phantom.exit();
});
