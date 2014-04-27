'use strict';

// Declare app level module which depends on filters, and services
angular.module('PrototypeApp', [
  'PrototypeApp.controllers',
  'PrototypeApp.services',
  'ngRoute'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.
	when("/user", {
    templateUrl: "partials/user.html",
    controller: "queueController"
  }).
	when("/admin", {
    templateUrl: "partials/admin.html",
    controller: "queueController"
  }).
	otherwise( {
    redirectTo: '/user'
  });
}]);