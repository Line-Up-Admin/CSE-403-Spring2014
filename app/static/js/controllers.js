'use strict';

/* Controllers */
angular.module('LineUpApp.controllers', []).


  controller('headerController', function ($scope, lineUpAPIService, $location, $route) {
     // this assignment gives the headerController's $scope access to the displayHelp function
     // of whichever page loaded it.
     $scope.displayHelp = $scope.$parent.displayHelp;
    }).


  // Controller for the #/create_queue route
  controller('createQueueController', function ($scope, lineUpAPIService, $location, $route) {
    $scope.queue = {};

    // hide the edit button if we are on the create queue page
    // call on page load with ng-init="init()"
    $scope.init = function () {
      if ($route.current.loadedTemplateUrl == "partials/create_queue.html") {
        document.getElementById("edit-button").classList.add("hide");
      }
    };

    // Sends a request to the server to create a new queue. The request
    // contains the new queue settings.
    // Upon success: Updates the current queue model to include the new ID.
    // Upon error: redirect to the error page
    $scope.createNewQueue = function () {

      // clear any previous errors
      $scope.errors = {};

      // all new queues start as active
      $scope.queue.active = 1;

      // send the request
			lineUpAPIService.createQueue($scope.queue).
        success(function (data, status, headers, config) {
          if (data.SUCCESS) {
            // load the queue admin page
            $location.path('/admin/' + data.qid);
          } else {
            // display errors
            $scope.errors = data;
          }
        }).
        error(function (data, status, headers, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
    }
  }).

  // Controller for the #/login route
  controller('userLoginController', function ($scope, lineUpUserService, $location) {
    $scope.user = lineUpUserService.getUser();

    // never prepopulate the password field
    $scope.user.pw = "";
    lineUpUserService.saveUser($scope.user);

    $scope.signUp = function () {
      // save the username and password to populate the create user form
      $location.path("/create_account");
    };

    // Sends a user account login request to the server.
    // Upon success: displays the user home page with queue information
    // Upon error: TODO: Do something smart to handle the error
    $scope.login = function () {
      lineUpUserService.login($scope.user).
        success(function (data, status, headers, config) {
          if (data.SUCCESS) {
            // successful login
            $location.path("/home");
          } else {
            // login unsuccessful, display error
            $scope.error = data.error_message;
            document.getElementById('error').classList.remove('hide');
					}
        }).
        error(function (data, status, headers, config) {
          $location.path("/");
					document.getElementById('error').classList.remove('hide');
        });
    };
  }).

  // Controller for the #/create_account route
  controller('userCreateController', function ($scope, lineUpUserService, $location) {
    $scope.user = lineUpUserService.getUser();
    $scope.errors = {};

    // Sends a user account creation request to the server.
    // Upon success: Redirects the browser to the login page.
    // Upon error: TODO: Do something smart to handle the error
    $scope.createUser = function () {
      if ($scope.user.pw != $scope.user.pwx2) {
        $scope.errors = {};
        $scope.errors.pw = "Passwords do not match.";
        return;
      }

      // don't send the extra password to the server
      delete $scope.user.pwx2;
      lineUpUserService.saveUser($scope.user);

      // send the new account info to the server
      lineUpUserService.createUser($scope.user).
        success(function (data, status, headers, config) {
          console.log(data);
          // account created successfully, redirect to the login page
          if (data.SUCCESS) {
            $location.path("/");
          }
          // display the returned error messages
          $scope.errors = data;
        }).
        error(function (data, status, headers, config) {
          $location.path("/error");
        });
      }
  }).

  // Controller for the #/user_home route
  controller('userHomeController', function ($scope, lineUpAPIService, $route, $location) {

    // hide the home button if we are on the home page
    // call on page load with ng-init="init()"
    $scope.init = function () {
      if ($route.current.loadedTemplateUrl == "partials/user_home.html") {
        document.getElementById("home-button").classList.add("hide");
      }
    };

    // show the help slide-in modal
    $scope.displayHelp = function () {
            $("#help-modal").modal('toggle');
    };
		// Sends a user queue request to the server.
    // Upon success: Loads the user queues to the requisite scope fields.
    // Upon error: TODO: Do something smart to handle the error
    $scope.getUsersQueues = function () {
      lineUpAPIService.getUsersQueues().
        success(function (data, status, headers, config) {
          console.log(data);
          if (data.SUCCESS) {
            $scope.queueInfos = data;
          } else {
            console.log(data);
            $location.path("/");
          }
        }).
        error(function (data, status, headers, config) {
          console.log(data);
          $location.path("/error");
        });
    }();
  }).

  // Controller for the #/search route
  controller('searchController', function ($scope, $route, lineUpAPIService) {
    // hide the edit button if we are on the create queue page
    // call on page load with ng-init="init()"
    $scope.init = function () {
      if ($route.current.loadedTemplateUrl == "partials/search.html") {
        document.getElementById("edit-button").classList.add("hide");
      }
    };

    // Sends search query to the server and fills the search results in the
    // HTML
    $scope.search = function () {
      lineUpAPIService.search($scope.query).
        success(function (data, status, headers, config) {
            document.getElementById("results").innerHTML="Search Results";
            $scope.queueInfos = data.queue_info_list;
          }).
          error(function (data, status, headers, config) {
            console.log(data);
            alert("Something went wrong with the search request! \nStatus: " + status);
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
    }();
  }).

  // Controller for the #/queue_info route
  controller('queueInfoController', function ($scope, $route, lineUpAPIService, $routeParams) {
    $scope.optional_data = "";
    $scope.uname = "";

    // hide the edit button if we are on the create queue page
    // called on element load with ng-init="init()"
    $scope.init = function () {
      if ($route.current.loadedTemplateUrl == "partials/queue_info.html") {
        document.getElementById("edit-button").classList.add("hide");
      }
    };

    // show the help slide-in modal
    $scope.displayHelp = function () {
            $("#help-modal").modal('toggle');
    };

    $scope.queueStatus = function () {
      lineUpAPIService.queueStatus($routeParams.qid).
        success(function (data, status, headers, config) {
          $scope.queue = data;
          console.log(data);
          document.getElementById('enqueued').classList.add('hide');
          document.getElementById('notEnqueued').classList.add('hide');
          if (data.member_position == null) {
            document.getElementById('notEnqueued').classList.remove('hide');
          } else {
            document.getElementById('enqueued').classList.remove('hide');
            // if (data.member_position == data.size) {
              // document.getElementById('btn-postpone').disabled = true;
            // }
          }
        }).
        error(function (data, status, headers, config) {
          alert("Something went wrong with the queue lookup request!\nStatus: " + status);
        });
    };

    // This should load immediately when this controller is used
    $scope.queueStatus();

    // used for self-removal of user from the queue
    $scope.leaveQueue = function () {
      lineUpAPIService.leaveQueue($routeParams.qid).
      success(function (data, status, header, config) {
        if(data.SUCCESS) {
          // reset the client data and reset the page
          $scope.queue = data;
          $scope.queueStatus();
        }
      }).
      error(function (data, status, header, config) {
        alert("Something went wrong with your request to leave the queue!\n Status" + status);
      });
    };

    $scope.postpone = function () {
      lineUpAPIService.postpone($routeParams.qid).
        success(function (data, status, header, config) {
          console.log(data);
          if(data.SUCCESS) {
            $scope.queue = data;
          }
        }).
        error(function (data, status, header, config) {
          alert("Something went wrong with your request to postpone!\nStatus: " + status);
        });
    };

    $scope.promptForData = function () {
      if ($scope.queue.logged_in) {
        if ($scope.queue.prompt) {
          $("#question-modal").modal('toggle');
          //hide the name prompt
          document.getElementById("name").classList.add("hide");
        } else {
          // don't show window just join queue
          $scope.joinQueue();
        }
      } else {
          if ($scope.queue.prompt) {
            // show both the prompt and the name
            $("#question-modal").modal('toggle');
          } else {
            $("#question-modal").modal('toggle');
            // hide the prompt
            document.getElementById("prompt").classList.add("hide");
          }
      }
    }

    // Sends a request to the server to join the queue
    // Upon success: Updates the current queueInfos array to store the results
    // of the request.
    // Upon error: TODO: Do something smart to handle the error
    $scope.joinQueue = function () {
      lineUpAPIService.joinQueue({ 'qid': $scope.queue.qid, 'uname': $scope.uname, 'optional_data': $scope.optional_data }).
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

	controller('editQueueController', function($scope, lineUpAPIService, $routeParams, $location, $route) {
    // hide the edit button if we are on the create queue page
    // call on page load with ng-init="init()"
    $scope.init = function () {
      if ($route.current.loadedTemplateUrl == "partials/edit_queue.html") {
        document.getElementById("edit-button").classList.add("hide");
      }
    }
		$scope.queue = {};

		$scope.fillFormFields = function () {
			lineUpAPIService.getQueueSettings($routeParams.qid).
				success(function (data, status, headers, config) {
					console.log(data);
					$scope.queue = data;
					console.log($scope.queue);
				}).
				error(function (data, status, headers, config) {
					alert("Something went wrong with the form fill request!\nStatus: " + status);
				});
		}();

		$scope.editQueue = function () {
		lineUpAPIService.editQueue({ 'qid': $routeParams.qid, 'q_settings': $scope.queue }).
				success(function (data, status, headers, config) {
					$location.path('/admin/' + $routeParams.qid);
				}).
				error(function (data, status, headers, config) {
					alert("Something went wrong with the edit queue request!\nStatus: " + status);
				});
		}
  }).

  // Controller for the #/admin route
	controller('adminViewController', function ($scope, lineUpAPIService, $location, $routeParams, $route) {
		$scope.user = {};
		$scope.queueInfo = {};
    $scope.errors = {};
		$scope.member_list = [];
		$scope.setActiveStatusTo = "Close Queue";

		// Redirects to edit queue page.
		$scope.redirectToEditQueue = function () {
			$location.path('/edit/' + $routeParams.qid);
		}

    // show the help slide-in modal
    $scope.displayHelp = function () {
            $("#help-modal").modal('toggle');
    };

		// Sends an admin view request to the server.
    // Upon success: Shows the admin view for the given queue id.
    // Upon error: TODO: Do something smart to handle the error
		$scope.getDetailedQueueInfo = function () {
			lineUpAPIService.getDetailedQueueInfo($routeParams.qid).
				success(function (data, status, headers, config) {
					$scope.queueInfo = data.queue_info;
					$scope.member_list = data.member_list;
					document.getElementById("list-group").size = $scope.member_list.length + 1;
					var button = document.getElementById("btn-close-queue");

					if( $scope.queueInfo.active == 0 ) {
						$scope.setActiveStatusTo = "Open Queue";
						button.value = 1;
					} else {
						$scope.setActiveStatusTo = "Close Queue";
						button.value = 0;
					}
				}).
				error(function (data, status, headers, config) {
					// not an error we are prepared to handle
          $location.path("/error");
				});
		}
    $scope.getDetailedQueueInfo();

		// Sends a dequeue request to the server.
    // Upon success: Dequeues the first person in line.
    // Upon error: TODO: Do something smart to handle the error
		$scope.dequeueFirstPerson = function () {
			lineUpAPIService.dequeueFirstPerson($routeParams.qid).
				success(function (data, status, headers, config) {
          // refresh the queue data
          $scope.getDetailedQueueInfo();

          // display the dequeued user and info
					if (data.optional_data) {
						alert(data.uname + " was removed, information: " + data.optional_data);
					} else {
						alert(data.uname + " was removed.");
					}
				}).
				error(function (data, status, headers, config) {
					// not an error we are prepared to handle
          $location.path("/error");
				});
		}

		// Sends a remove request to the server.
    // Upon success: Dequeues the selected person in line.
    // Upon error: TODO: Do something smart to handle the error
		$scope.dequeueSelectPerson = function () {
			var selectIndex = document.getElementById("list-group").options.selectedIndex;
			lineUpAPIService.dequeueSelectPerson({ 'qid': $routeParams.qid, 'uid': $scope.member_list[selectIndex].uid }).
				success(function (data, status, headers, config) {
					$scope.queueInfo = data.queue_info;
					$scope.member_list = data.member_list;
					$scope.getDetailedQueueInfo();
				}).
				error(function (data, status, headers, config) {
					alert(data);
				});
		}

		// Opens a modal dialog that prompts for the name and the optional data.
    // Sends a request to the server to add that name to the queue.
    // Upon Success: the name has been added to the queue
    // Upon Error: redirect to the error page.
		$scope.adminAdd = function () {

      // ensure that we send json data with both values
      if (!$scope.user.uname) {
        $scope.user.uname = "";
      }
      if (!$scope.user.optional_data) {
        $scope.user.optional_data = "";
      }

      // send the request
			lineUpAPIService.enqueue($routeParams.qid, $scope.user).
        success(function (data, status, headers, config) {

          if (data.SUCCESS) {
            // refresh the queue
            $scope.getDetailedQueueInfo();

            // close the window
            $("#addModal").modal('toggle');
            $scope.errors = {};
            $scope.user = {};

          } else {
            // display error messages
            $scope.errors = data;
            if (data.error_message) {
              document.getElementById('error').classList.remove('hide');
            }
          }
				}).
        error(function (data, status, headers, config) {
          // this is not an error we are prepared to handle
          $location.path("/error");
        });
		}

    $scope.dismissModal = function () {
      // clear the error messsages
      $scope.errors = {};
      $scope.user = {};

      // close the modal window
      $("#addModal").modal('toggle');
    }


		$scope.demoteSelectPerson = function () {
			var selectIndex = document.getElementById("list-group").options.selectedIndex;
			lineUpAPIService.demoteSelectPerson({ 'qid': $routeParams.qid, 'uid': $scope.member_list[selectIndex].uid }).
				success(function (data, status, headers, config) {
					// refresh the queue
          $scope.getDetailedQueueInfo();
					document.getElementById("list-group").selectedIndex = selectIndex + 1;
				}).
				error(function (data, status, headers, config) {
					// this is not an error we are prepared to handle
          $location.path("/error");
				});
		}

		// Sends a request to toggle the queue's active status to the server.
    // Upon success: toggles the queue to open or closed depending on prev state.
    // Upon error: redirects to an error page.
		$scope.setActive = function() {
      // get the button
			var button = document.getElementById("btn-close-queue");
			var targetActiveStatus = button.value;

      // send the request
			lineUpAPIService.setActive($routeParams.qid, targetActiveStatus).
        success(function (data, status, headers, config) {
					if (targetActiveStatus == 0) {
            // the queue is closed
						$scope.setActiveStatusTo = "Open Queue";
						button.value = 1;
					} else {
            // the queue is open
						$scope.setActiveStatusTo = "Close Queue";
						button.value = 0;
					}
				}).
        error(function (data, status, headers, config) {
          // this is not an error we are prepared to handle
          $location.path("/error");
        });
		}

    $scope.viewDetails = function () {
      var selectedIndex = document.getElementById("list-group").options.selectedIndex;
      if (selectedIndex != -1) {
        $scope.userDetails = $scope.member_list[selectedIndex];
        $("#details-modal").modal('toggle');
      }
    }
	});