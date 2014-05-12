'use strict';

// Declare app level module which depends on controllers, filters,
// and services etc.
angular.module('LineUpApp', [
  'LineUpApp.controllers',
  'LineUpApp.services',
  'ngRoute'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.
  when("/", {
    templateUrl: "partials/login.html",
    controller: "lineUpController"
  }).
  when("/search", {
    templateUrl: "partials/search.html",
    controller: "lineUpController"
  }).
  when("/queue_info", {
    templateUrl: "/index.html",
    controller: "lineUpController"
  }).
  when("/create", {
    templateUrl: "/index.html",
    controller: "lineUpController"
  }).
  when("/queues", {
    templateUrl: "/index.html",
    controller: "lineUpController"
  }).
  when("/anonymous", {
    templateUrl: "/index.html",
    controller: "lineUpController"
  }).
  when("/create_account", {
    templateUrl: "partials/create_account.html",
    controller: "lineUpController"
  }).
  when("/debug_q", { //SHOULD BE REMOVED BEFORE BETA RELEASE
    templateUrl: "partials/debug_queue_settings.html",
    controller: "lineUpController"
  }).
  otherwise( {
    redirectTo: '/'
  });
}]);