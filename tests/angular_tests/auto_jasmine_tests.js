var page = require('webpage').create();
page.open('SpecRunner.html', function() {
  phantom.exit();
});
