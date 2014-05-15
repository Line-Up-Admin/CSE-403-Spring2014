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
    controller: "userAccountController"
  }).
  when("/search", {
    templateUrl: "partials/search.html",
    controller: "lineUpController"
  }).
  when("/queue_info/:qid", {
    templateUrl: "partials/queue_info.html",
    controller: "queueInfoController"
  }).
  when("/create_queue", {
    templateUrl: "partials/create_queue.html",
    controller: "lineUpController"
  }).
  when("/home", {
    templateUrl: "partials/user_home.html",
    controller: "lineUpController"
  }).
  when("/anonymous", {
    templateUrl: "/index.html",
    controller: "lineUpController"
  }).
  when("/create_account", {
    templateUrl: "partials/create_account.html",
    controller: "userAccountController"
  }).
  when("/debug_q", { //SHOULD BE REMOVED BEFORE BETA RELEASE
    templateUrl: "partials/debug_queue_settings.html",
    controller: "lineUpController"
  }).
  otherwise( {
    redirectTo: '/'
  });
}]);