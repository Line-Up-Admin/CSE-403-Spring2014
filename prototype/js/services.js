'use strict';

/* Services */

// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('PrototypeApp.services', []).
  service('userService', function() {
    return { displayName: "Nick", id: 7777777777 };
  }).

  service('queueService', function() {
    return [
      { displayName: "Brian Eno", id: 0987654321 },
      { displayName: "Peter Gabriel", id: 8459847589 },
      { displayName: "Phil Collins", id: 8475847584 },
      { displayName: "David Bowie", id: 1234567890 },
      { displayName: "Bryan Ferry", id: 1234512345 }
    ];
  });