var page = require('webpage').create();
page.open('angular_tests/SpecRunner.html', function() {
  phantom.exit();
});
