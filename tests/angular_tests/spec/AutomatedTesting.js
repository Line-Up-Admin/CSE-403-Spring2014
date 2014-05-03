$(document).ready(function () {

  setTimeout(function() {
    results = $('.bar.failed');
    if (results == undefined) {
      console.log("Angular Tests: All Passed");
    } else {

      console.log("Angular Tests: " + results.text());
    }
  }, 5000);
});