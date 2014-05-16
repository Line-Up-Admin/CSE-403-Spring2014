'use strict';

/* Controllers */
angular.module('LineUpApp.controllers', []).
  controller('lineUpController', function ($scope, lineUpAPIService, $location) {
    $scope.user = {};
		$scope.userInfos = [];
    $scope.queue = {};
    $scope.queueInfos = [];

    // Sends a request to the server to create a new queue. The request
    // contains the new queue settings.
    // Upon success: Updates the current queue model to include the new ID.
    // Upon error: TODO: Do something smart to handle the error
    $scope.createNewQueue = function () {
			//$scope.queue.active = document.getElementById("active").value;
      $scope.queue.active = 1;
			lineUpAPIService.createQueue($scope.queue).
        success(function (data, status, headers, config) {
          // set the local queue to be the newly created queue
          $scope.queue = data;
					console.log($scope.queue);
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the create request!\nStatus: " + status);
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
  }).
  controller('userAccountController', function ($scope, lineUpAPIService, $location) {

    // Sends a user account login request to the server.
    // Upon success: ???
    // Upon error: TODO: Do something smart to handle the error
    $scope.login = function () {
      lineUpAPIService.login($scope.user).
        success(function (data, status, headers, config) {
          if (data == 'Invalid username or password') {
            // login unsuccessful, display error
            $scope.error = data;
            document.getElementById('error').classList.remove('hide');
            return;
          }
          // successful login
          $location.path("/home");
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the login request!\nStatus: " + status);
        });
    }

    // Sends a user account creation request to the server.
    // Upon success: Redirects the browser to the login page.
    // Upon error: TODO: Do something smart to handle the error
    $scope.createUser = function () {
      if ($scope.user.pw != $scope.user.pwx2) {
        alert("Passwords do not match, please retype and try again.");
        return;
      }

      // don't send the extra password to the server
      delete $scope.user.pwx2;
      $scope.user.temp = 0;

      lineUpAPIService.createUser($scope.user).
        success(function (data, status, headers, config) {
          // account created successfully, redirect to the login page
          $location.path("/");
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the create account request!\nStatus: " + status);
        });
      }
  }).
  controller('queueInfoController', function ($scope, lineUpAPIService, $routeParams) {

    // Sends a request to the server to get the queue settings that match the
    // provided ID.
    // Upon success: Updates the current queue model to include the queue
    // settings.
    // Upon error: TODO: Do something smart to handle the error
    $scope.getQueueSettings = function () {

      alert("Not yet implemented.");
      // lineUpAPIService.getQueueSettings($routeParams.qid).

      //   success(function (data, status, headers, config) {
      //     // set the local queue to be the newly created queue
      //     console.log(data);
      //   }).
      //   error(function (data, status, headers, config) {
      //     alert("Something went wrong with the queue lookup request!\nStatus: " + status);
      //   });
    }();
  });