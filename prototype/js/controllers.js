'use strict';

/* Controllers */

// A simple controller for managing the members of a queue
angular.module('PrototypeApp.controllers', []).
  controller('queueController', function ($scope, userService, queueService) {

    $scope.user = userService;
    $scope.queue = queueService;

    $scope.joinQueue = function () {
      $scope.queue.push({ displayName: $scope.user.displayName, id: $scope.user.id });
    };

    $scope.dequeueNext = function () {
      var nextPerson = $scope.queue.shift();
    };
  }).

  controller('headerController', function ($scope, $location) {
    $scope.isActive = function (viewLocation) {
        return viewLocation === $location.path();
    };
  });