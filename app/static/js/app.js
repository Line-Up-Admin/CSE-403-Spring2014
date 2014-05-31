'use strict';

// Declare app level module which depends on controllers, filters,
// and services etc.
// Each "when" specifies a 'controller' that will be evaluated and in scope
// for the specified 'templateUrl' html page.
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
    controller: "createQueueController"
  }).
	when("/admin/:qid", {
		templateUrl: "partials/queue_admin.html",
		controller: "adminViewController"
	}).
  when("/home", {
    templateUrl: "partials/user_home.html",
    controller: "userHomeController"
  }).
  when("/create_account", {
    templateUrl: "partials/create_account.html",
    controller: "userCreateController"
  }).
  when("/edit/:qid", {
    templateUrl: "partials/edit_queue.html",
    controller: "editQueueController"
  }).
  when("/error", {
    templateUrl: "partials/error.html"
    // No controller needed at this time
  }).
  otherwise( {
    redirectTo: '/'
  });
}]);