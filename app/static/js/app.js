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
    controller: "userLoginController"
  }).
  when("/search", {
    templateUrl: "partials/search.html",
    controller: "searchController"
  }).
  when("/queue_info/:qid", {
    templateUrl: "partials/queue_info.html",
    controller: "queueInfoController"
  }).
  when("/create_queue", {
    templateUrl: "partials/create_queue.html",
    controller: "lineUpController"
  }).
	when("/admin/:qid", {
		templateUrl: "partials/example_admin_queue_page.html",
		controller: "adminViewController"
	}).
  when("/home", {
    templateUrl: "partials/user_home.html",
    controller: "userHomeController"
  }).
  when("/anonymous", {
    templateUrl: "/index.html",
    controller: "lineUpController"
  }).
  when("/create_account", {
    templateUrl: "partials/create_account.html",
    controller: "userCreateController"
  }).
  when("/debug_q", { //SHOULD BE REMOVED BEFORE BETA RELEASE
    templateUrl: "partials/debug_queue_settings.html",
    controller: "lineUpController"
  }).
  otherwise( {
    redirectTo: '/'
  });
}]);