'use strict';

/* Controllers */
angular.module('LineUpApp.controllers', []).
  controller('lineUpController', function ($scope, lineUpAPIService) {
    $scope.queue = {};

    // Sends a request to the server to create a new queue. The request
    // contains the new queue settings.
    // Upon success: Updates the current queue model to include the new ID.
    // Upon error: TODO: Do something smart to handle the error
    $scope.createNewQueue = function () {
      lineUpAPIService.createQueue($scope.queue).
        success(function (data, status, headers, config) {
          // set the local queue to be the newly created queue
          $scope.queue.qid = data.id;
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the create request!\nStatus: " + status);
        });
    }

    // Sends a request to the server to get the queue settings that match the
    // provided ID.
    // Upon success: Updates the current queue model to include the queue
    // settings.
    // Upon error: TODO: Do something smart to handle the error
    $scope.getQueueSettings = function () {
      lineUpAPIService.getQueue($scope.queue.qid).
        success(function (data, status, headers, config) {
          // set the local queue to be the newly created queue
          $scope.queue = data;
          $scope.queue.qid = data.id;
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the queue lookup request!\nStatus: " + status);
        });
    }
  });