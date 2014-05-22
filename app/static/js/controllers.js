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
					$location.path('/admin/' + $scope.queue.qid);
        }).
        error(function (data, status, headers, config) {
          alert("Database error: could not create queue.\nStatus: " + status);
        });
    }
  }).

  controller('userLoginController', function ($scope, lineUpUserService, $location) {
    $scope.user = lineUpUserService.getUser();

    // never prepopulate the password field
    $scope.user.pw = "";
    lineUpUserService.saveUser($scope.user);

    $scope.signUp = function () {
      // save the username and password to populate the create user form
      //lineUpUserService.saveUser($scope.user);
      $location.path("/create_account");
    };


    // Sends a user account login request to the server.
    // Upon success: displays the user home page with queue information
    // Upon error: TODO: Do something smart to handle the error
    $scope.login = function () {
      lineUpUserService.login($scope.user).
        success(function (data, status, headers, config) {
          if (data.SUCCESS == false) {
            // login unsuccessful, display error
						$scope.error = data.error_message;
            document.getElementById('error').classList.remove('hide');
          } else {
						// successful login
						$location.path("/home");
					}
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the login request!\nStatus: " + status);
        });
    };
  }).

  controller('userCreateController', function ($scope, lineUpUserService, $location) {
    $scope.user = lineUpUserService.getUser();

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
      lineUpUserService.saveUser($scope.user);

      console.log($scope.user);
      lineUpUserService.createUser($scope.user).
        success(function (data, status, headers, config) {
          console.log(data);
          // account created successfully, redirect to the login page
          $location.path("/");
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the create account request!\nStatus: " + status);
        });
      }
  }).

  controller('userHomeController', function ($scope, lineUpAPIService) {

		// Sends a user queue request to the server.
    // Upon success: Loads the user queues to the requisite scope fields.
    // Upon error: TODO: Do something smart to handle the error
    $scope.getUsersQueues = function () {
      lineUpAPIService.getUsersQueues().
        success(function (data, status, headers, config) {
          $scope.queueInfos = data.queue_info_list;
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the queue lookup request!\nStatus: " + status);
        });
    }();
  }).

  controller('searchController', function ($scope, lineUpAPIService) {
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
    }();
  }).

  controller('queueInfoController', function ($scope, lineUpAPIService, $routeParams) {
    $scope.queueStatus = function () {
      lineUpAPIService.queueStatus($routeParams.qid).
        success(function (data, status, headers, config) {
          $scope.queue = data;
          document.getElementById('enqueued').classList.add('hide');
          document.getElementById('notEnqueued').classList.add('hide');
          if (data.member_position == null) {
            document.getElementById('notEnqueued').classList.remove('hide');
          } else {
            document.getElementById('enqueued').classList.remove('hide');
          }
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the queue lookup request!\nStatus: " + status);
        });
    }();

    // Sends a request to the server to join the queue
    // queues.
    // Upon success: Updates the current queueInfos array to store the results
    // of the request.
    // Upon error: TODO: Do something smart to handle the error
    $scope.joinQueue = function () {
      lineUpAPIService.joinQueue({ 'qid': $scope.queue.qid, 'uname': "temp" }).
        success(function (data, status, headers, config) {
          $scope.queue = data;
          document.getElementById('notEnqueued').classList.add('hide');
          document.getElementById('enqueued').classList.remove('hide');
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the join queue request! \nStatus: " + status);
        });
    }
  }).

	controller('adminViewController', function($scope, lineUpAPIService, $routeParams, $route) {
		$scope.user = {};
		$scope.queueInfo = {};
		$scope.member_list = [];

		// Sends a employee view request to the server.
    // Upon success: Shows the employee view for the given queue id.
    // Upon error: TODO: Do something smart to handle the error
		$scope.getDetailedQueueInfo = function () {
			lineUpAPIService.getDetailedQueueInfo($routeParams.qid).
				success(function (data, status, headers, config) {
					$scope.queueInfo = data.queue_info;
					$scope.member_list = data.member_list;
				}).
				error(function (data, status, headers, config) {
					alert("Are you logged in as an existing user? If not, that might be an issue.\nStatus: " + status);
				});
		}();

		// Sends a dequeue to the server.
    // Upon success: Dequeues the first person in line.
    // Upon error: TODO: Do something smart to handle the error
		$scope.dequeueFirstPerson = function () {
			lineUpAPIService.dequeueFirstPerson($routeParams.qid).
				success(function (data, status, headers, config) {
					$scope.queueInfo = data.queue_info;
					$scope.member_list = data.member_list;
				}).
				error(function (data, status, headers, config) {
					alert("Wow you suck at this.\nStatus: " + status);
				});
		}

		// Sends an enqueue request to the server.
    // Upon success: currently, enqueues the admin and updates the admin view.
    // Upon error: TODO: Do something smart to handle the error
		$scope.adminAdd = function () {
			lineUpAPIService.joinQueue({ 'qid': $routeParams.qid, 'uname': $scope.user.uname }).
        success(function (data, status, headers, config) {

					// loads the latest queue info, then reloads the page
					lineUpAPIService.getDetailedQueueInfo($routeParams.qid).
						success(function (data, status, headers, config) {
							$scope.queueInfo = data.queue_info;
							$scope.member_list = data.member_list;
							$route.reload();
						}).
						error(function (data, status, headers, config) {
							alert("Could not load latest queue information from server.\nStatus: " + status);
						});
				}).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the join queue request! \nStatus: " + status);
        });
		}
	});