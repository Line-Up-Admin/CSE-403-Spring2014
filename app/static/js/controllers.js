'use strict';

/* Controllers */
angular.module('LineUpApp.controllers', []).
  controller('lineUpController', function ($scope, lineUpAPIService) {
    $scope.user = {};
    $scope.queue = {};
    $scope.queueInfos = [];
    $scope.user = {};

    // Sends a request to the server to create a new queue. The request
    // contains the new queue settings.
    // Upon success: Updates the current queue model to include the new ID.
    // Upon error: TODO: Do something smart to handle the error
    $scope.createNewQueue = function () {
      lineUpAPIService.createQueue($scope.queue).
        success(function (data, status, headers, config) {
          // set the local queue to be the newly created queue
          $scope.queue = data;
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
      lineUpAPIService.getQueueSettings($scope.queue.id).
        success(function (data, status, headers, config) {
          // set the local queue to be the newly created queue
          $scope.queue = data;
          //$scope.queue.qid = data.id;
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the queue lookup request!\nStatus: " + status);
        });
    }

    // Sends a request to the server to get the information for the most popular
    // queues.
    // Upon success: Updates the current queueInfos array to store the results
    // of the request.
    // Upon error: TODO: Do something smart to handle the error
    $scope.getPopularQueues = function () {
      lineUpAPIService.getPopularQueues().
        success(function (data, status, headers, config) {
          $scope.queueInfos = data.queue_info_list;
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the popular queue request! \nStatus: " + status);
      });
    }

    // Sends a request to the server to join the queue
    // queues.
    // Upon success: Updates the current queueInfos array to store the results
    // of the request.
    // Upon error: TODO: Do something smart to handle the error
    $scope.joinQueue = function () {
      lineUpAPIService.joinQueue({ 'qid': $scope.queue.id, 'uname': $scope.user.uname }).
        success(function (data, status, headers, config) {
          console.log(data);
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the join queue request! \nStatus: " + status);
        });
    }











    //HACK STARTS HERE - REMOVE BEFORE BETA
    $scope.queueInfos = $scope.getPopularQueues();




  });