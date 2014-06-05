(function() {
'use strict';

// round the time values to the nearest integer
var roundTimes = function (data) {
  if (data.expected_wait) {
    data.expected_wait = parseInt(data.expected_wait);
  }
  if (data.avg_wait_time) {
    data.avg_wait_time = parseInt(data.avg_wait_time);
  }
}

var roundMultipleTimes = function (data) {
  for (var i = 0; i < data.length; i++) {
    roundTimes(data[i]);
  }
}


//Permissions constants
var PERMISSION_ADMIN = 3;
var PERMISSION_MANAGER = 1;
var PERMISSION_NONE = 0;
var REFRESH_INTERVAL = 2000;

/*
This file contains all controllers for the all web pages.  A single controller
is loaded for each HTML template as defined in app.js
*/

/* Controllers */

angular.module('LineUpApp.controllers', []).

  /*
     Controller for the main header controls the data and user interaction
     for the headers which are shared by several web pages.
  */
  controller('headerController', function ($scope, lineUpAPIService, $location, $route) {
     // this assignment gives the headerController's $scope access to the displayHelp function
     // of whichever page loaded it.
     $scope.displayHelp = $scope.$parent.displayHelp;
     $scope.userInfo = {};
     $scope.getCurrentUser = function () {
       lineUpAPIService.getCurrentUser().
        success(function (data, status, headers, config) {
          if( data.SUCCESS ) {
            $scope.userInfo = data;
          }
        }).
        error(function (data, status, headers, config) {
          // not an eventuality we are prepared to handle
        });
     }
     $scope.getCurrentUser();
  }).

  // Controller for the #/create_queue route
  controller('createQueueController', function ($scope, lineUpAPIService, $location, $route) {
    $scope.queue = {};

    // show the help slide-in modal
    $scope.displayHelp = function () {
      $("#help-modal").modal('toggle');
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

  /*
   Controller for the #/login route controls data and user interaction
   for that route
  */
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
    // Upon error: redirects to an error page.
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
          // unrecoverable server error
          $location.path("/");
          document.getElementById('error').classList.remove('hide');
        });
    };
  }).

  /*
   Controller for the #/create_account route controls data and user interaction
   for that route
  */
  controller('userCreateController', function ($scope, lineUpUserService, $location) {
    $scope.user = lineUpUserService.getUser();
    $scope.errors = {};

    // Sends a user account creation request to the server.
    // Upon success: Redirects the browser to the login page.
    // Upon error: Redirect to the error page.
    $scope.createUser = function () {
      $scope.errors = {};

      if ($scope.user.pw == "") {
        $scope.errors.pw = "Please create a password.";
        return;
      }

      if ($scope.user.pw != $scope.user.pwx2) {
        $scope.errors.pw = "Passwords do not match.";
        return;
      }

      // don't send the extra password to the server
      delete $scope.user.pwx2;
      lineUpUserService.saveUser($scope.user);

      // send the new account info to the server
      lineUpUserService.createUser($scope.user).
        success(function (data, status, headers, config) {
          // account created successfully, redirect to the login page
          if (data.SUCCESS) {
            $location.path("/");
          }
          // display the returned error messages
          $scope.errors = data;
        }).
        error(function (data, status, headers, config) {
          // unrecoverable server error
          $location.path("/error");
        });
      }
  }).

  /*
   Controller for the #/user_home route controls data and user interaction
   for that route
  */
  controller('userHomeController', function ($scope, lineUpAPIService, $route, $location) {

    // hide the home button if we are on the home page
    // call on page load with ng-init="init()"
    /* $scope.init = function () {
      if ($route.current.loadedTemplateUrl == "partials/user_home.html") {
        document.getElementById("home-button").classList.add("hide");
      }
    }; */

    //clear any intervals
    //clearInterval(autoRefresh);


    // show the help slide-in modal
    $scope.displayHelp = function () {
            $("#help-modal").modal('toggle');
    };
    // Sends a user queue request to the server.
    // Upon success: Loads the user queues to the requisite scope fields.
    // Upon error: redirect to the error page.
    $scope.getUsersQueues = function () {
      lineUpAPIService.getUsersQueues().
        success(function (data, status, headers, config) {
          if (data.SUCCESS) {
            roundMultipleTimes(data.queues_in);
            roundMultipleTimes(data.queues_admin);
            roundMultipleTimes(data.queues_manager);
            if (data.queues_in.length == 0) {
              document.getElementById('empty-in').classList.remove('hide');
            }
            if (data.queues_admin.length == 0) {
              document.getElementById('empty-admin').classList.remove('hide');
            }
            if (data.queues_manager.length == 0) {
              document.getElementById('empty-manager').classList.remove('hide');
            }
            /* QueueInfos is a 3 element array.  Each element is an array.
            1. 'queues_admin' - the queues you administer
            2. 'queues_manager' - the queues you manage
            3. 'queues_in' - the queues you are in
            */
            $scope.queueInfos = data;
          } else {
            $location.path("/");
          }
        }).
        error(function (data, status, headers, config) {
          // unrecoverable server error
          $location.path("/error");
        });
    }();
  }).

  /*
   Controller for the #/search route controls data and user interaction
   for that route
  */
  controller('searchController', function ($scope, $route, lineUpAPIService) {

    $scope.errors = {};

    // show the help slide-in modal
    $scope.displayHelp = function () {
      $("#help-modal").modal('toggle');
    };

    // Sends search query to the server and fills the search results in the
    // HTML
    $scope.search = function () {
      // clear previous errors
      $scope.errors = {};
      document.getElementById('error').classList.add('hide');

      if (!$scope.query || $scope.queury == "") {
        document.getElementById("results").innerHTML="Popular Queues";
        $scope.getPopularQueues();
        return;
      }

      lineUpAPIService.search($scope.query).
        success(function (data, status, headers, config) {
            document.getElementById("results").innerHTML="Search Results";
            roundMultipleTimes(data.queue_info_list);
            $scope.queueInfos = data.queue_info_list;
          }).
          error(function (data, status, headers, config) {
            // unrecoverable server error
            $scope.errors.error_message = "Something went wrong. Search Results could not be retrieved at this time."
            document.getElementById('error').classList.remove('hide');
        });
    }

    // Sends a request to the server to get the information for the most popular
    // queues.
    // Upon success: Updates the current queueInfos array to store the results
    // of the request.
    // Upon error: redirects to an error page.
    $scope.getPopularQueues = function () {
      // clear previous errors
      $scope.errors = {};
      document.getElementById('error').classList.add('hide');

      // request the popular queues
      lineUpAPIService.getPopularQueues().
        success(function (data, status, headers, config) {
          roundMultipleTimes(data.queue_info_list);
          $scope.queueInfos = data.queue_info_list;
        }).
        error(function (data, status, headers, config) {
          // unrecoverable server error
          $scope.errors.error_message = "Something went wrong. Popular Queues could not be retrieved at this time."
          document.getElementById('error').classList.remove('hide');
      });
    };
    $scope.getPopularQueues();
  }).

  /*
   Controller for the #/queue_info route controls data and user interaction
   for that route
  */
  controller('queueInfoController', function ($scope, $route, lineUpAPIService, $routeParams, $location, $interval) {
    $scope.optional_data = "";
    $scope.uname = "";
    $scope.locationLink = "";

    // show the help slide-in modal
    $scope.displayHelp = function () {
      $("#help-modal").modal('toggle');
    };

    // Request the details of this queue from the server.
    // On success: Display the correct view based on the user being in the
    // queue or not.
    // On failure: redirect to the error page.
    $scope.queueStatus = function () {
      lineUpAPIService.queueStatus($routeParams.qid).
        success(function (data, status, headers, config) {
          roundTimes(data);
          $scope.queue = data;
          if (data.location != null) {
            var location = data.location.split(" ").join("%20");
            $scope.locationLink = "http://maps.google.com/?q=" + location;
          } else {
            $scope.locationLink = "";
          }// hide all elements
          document.getElementById('enqueued').classList.add('hide');
          document.getElementById('notEnqueued').classList.add('hide');

          if (data.member_position == null) {
            // show elements for the user that is not in the queue
            document.getElementById('notEnqueued').classList.remove('hide');
          } else {
            // show elements for the user that is in the queue
            document.getElementById('enqueued').classList.remove('hide');
            if( data.member_position + 1 == data.size ) {
              document.getElementById('btn-postpone').disabled = true;
              console.log(document.getElementById('btn-postpone').disabled);
            } else {
              document.getElementById('btn-postpone').disabled = false;
            }
            $scope.progressBar();
          }

          if (data.active == 0 ) {
            document.getElementById("btn-join").disabled = true;
            document.getElementById("closed-message").classList.remove('hide');
          }
        }).
        error(function (data, status, headers, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
    };

    $scope.progressBar = function () {
      var size = $scope.queue.size;
      var bar = document.getElementById("progress");

      while( bar.firstChild ) {
        bar.removeChild(bar.firstChild);
      }
      var width = 100.0 / size;
      var widthPercentage = width + "%";
      for(var i=0; i<size; i++) {
        var div = document.createElement("div");
        div.classList.add("progress-bar-section");
        div.style.width = widthPercentage;
        div.innerHTML = "&nbsp";
        if( size - 1 - i == $scope.queue.member_position ) {
          div.classList.add("current-user");
          if( size == 1 ) {
            div.innerHTML = "YOU'RE IN FRONT!";
          } else if( size < 5 && size >= 2 ) {
            div.innerHTML = "YOU";
          }
        }
        bar.appendChild(div);
      }
    }

    // This should load immediately when this controller is used
    $scope.queueStatus();

    // This interval will update the queue information every 2 seconds
     var autoRefresh = $interval(function() {
       $scope.queueStatus();
     } , REFRESH_INTERVAL);

    // stop the autoRefresh interval when this iFrame is destroyed
    $scope.$on('$destroy', function() {
      if (angular.isDefined(autoRefresh)) {
        $interval.cancel(autoRefresh);
        autoRefresh = undefined;
      }
    })

    // Send request to the server to remove yourself from the queue
    $scope.leaveQueue = function () {
      lineUpAPIService.leaveQueue($routeParams.qid).
        success(function (data, status, header, config) {
          if(data.SUCCESS) {
            // reset the client data and reset the page
            $scope.queueStatus();
          }
        }).
        error(function (data, status, header, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
    };

    // Send a request to the server to move back one spot in line
    $scope.postpone = function () {
      lineUpAPIService.postpone($routeParams.qid).
        success(function (data, status, header, config) {
          if(data.SUCCESS) {
            roundTimes(data);
            $scope.queue = data;
            $scope.progressBar();
            if( data.member_position + 1 == data.size ) {
              document.getElementById('btn-postpone').disabled = true;
              console.log(document.getElementById('btn-postpone').disabled);
            } else {
              document.getElementById('btn-postpone').disabled = false;
            }
          }
        }).
        error(function (data, status, header, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
    };

    // promt the user for more information needed when they join the queue.
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
    // Upon error: redirects to an error page.
    $scope.joinQueue = function () {
      $scope.errors = {};
      document.getElementById("error").classList.add('hide');
      lineUpAPIService.joinQueue({ 'qid': $scope.queue.qid, 'uname': $scope.uname, 'optional_data': $scope.optional_data }).
        success(function (data, status, headers, config) {
          if (data.SUCCESS) {
            $scope.queue = data;
            document.getElementById('notEnqueued').classList.add('hide');
            document.getElementById('enqueued').classList.remove('hide');
            roundTimes(data);
            $scope.progressBar();
          } else {
            $scope.errors = data;
            document.getElementById("error").classList.remove('hide');
          }
        }).
        error(function (data, status, headers, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
    }
  }).

  /*
   Controller for the edit/queueID route controls data and user interaction
   for that route
  */
  controller('editQueueController', function ($scope, lineUpAPIService, $routeParams, $location, $route) {
    $scope.queue = {};

    // populate the form fields with the existing queue settings
    $scope.fillFormFields = function () {
      lineUpAPIService.getQueueSettings($routeParams.qid).
        success(function (data, status, headers, config) {
          // convert the arrays of users to a string of comma seperated values
          if (data.admins) {
            var admins_str = data.admins[0];
            for (var i = 1; i < data.admins.length; i++) {
              admins_str += ", " + data.admins[i];
            }
            data.admins = admins_str;
          }

          if (data.managers) {
            var managers_str = data.managers[0];
            for (var i = 1; i < data.managers.length; i++) {
              managers_str += ", " + data.managers[i];
            }
            data.managers = managers_str;
          }

          $scope.queue = data;
        }).
        error(function (data, status, headers, config) {
          // unrecoverable server error
          alert("Something went wrong with the form fill request!\nStatus: " + status);
        });
    };
    $scope.fillFormFields();

    // send the updated settings to the server
    $scope.editQueue = function () {
      // clear any old errors
      $scope.errors = {};
      lineUpAPIService.editQueue({ 'qid': $routeParams.qid, 'q_settings': $scope.queue }).
        success(function (data, status, headers, config) {
          if (data.SUCCESS) {
            // redirect back to the admin view
            $location.path('/admin/' + $routeParams.qid);
          } else {
            $scope.errors = data;
          }
        }).
        error(function (data, status, headers, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
      }
  }).

  /*
   Controller for the #/admin route controls data and user interaction
   for that route
  */
  controller('adminViewController', function ($scope, lineUpAPIService, $location, $routeParams, $route, $interval) {
    $scope.selectedUser;
    $scope.activeStatus = "OPEN";
    $scope.user = {};
    $scope.queueInfo = {};
    $scope.errors = {};
    $scope.member_list = [];
    $scope.setActiveStatusTo = "Close Queue";
    $scope.qid = $routeParams.qid;
    $scope.close_icon = "glyphicon glyphicon-stop";

    $scope.disableDemote = function () {
      var list = document.getElementById("list-group");
      list.addEventListener("click", function () {
        var demoteButton = document.getElementById("btn-demote");
        if( list.selectedIndex + 1 == list.options.length ) {
          demoteButton.disabled = true;
        } else if( demoteButton.disabled ) {
          demoteButton.disabled = false;
        }
      });
    }
    $scope.disableDemote();

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
    // Upon error: redirects to an error page.
    $scope.getDetailedQueueInfo = function (prevIndex) {
      lineUpAPIService.getDetailedQueueInfo($routeParams.qid).
        success(function (data, status, headers, config) {
          if (data.SUCCESS) {
            // only available to admins of this queue
            roundTimes(data.queue_info);
            $scope.queueInfo = data.queue_info;
            $scope.member_list = data.member_list;

            // Hide the settings button if not an admin
            if (data.permission_level != PERMISSION_ADMIN) {
              document.getElementById('btn-settings').classList.add('disabled');
            }

            var buttons = [];
            buttons.push(document.getElementById("btn-remove-first"));
            buttons.push(document.getElementById("btn-view-details"));
            buttons.push(document.getElementById("btn-remove"));
            var dequeueButton = document.getElementById("btn-remove-first");
            if( $scope.member_list.length == 0 ) {
              for( var i = 0; i < buttons.length; i++ ) {
                buttons[i].disabled = true;
              }
            } else {
              for( var i = 0; i < buttons.length; i++ ) {
                buttons[i].disabled = false;
              }
            }

            var button = document.getElementById("btn-close-queue");
            if( $scope.queueInfo.active == 0 ) {
              $scope.setActiveStatusTo = "Open Queue";
              button.value = 1;
              $scope.close_icon = "glyphicon glyphicon-play";
              $scope.activeStatus = "CLOSED";
            } else {
              $scope.setActiveStatusTo = "Close Queue";
              $scope.close_icon = "glyphicon glyphicon-stop";
              button.value = 0;
            }
            // gets the selected user
            $scope.selectedUser = $scope.member_list[prevIndex];
          } else {
              $location.path("/home");
        }
        }).
        error(function (data, status, headers, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
    }
    $scope.getDetailedQueueInfo(0);

    // shows the window to the user offering to dequeue the person at the front
    $scope.showDequeueModal = function () {
      // get the user at the front of the queue
      $scope.userDetails = $scope.member_list[0];

      // clear previous error messages
      document.getElementById('error').classList.add('hide');

      // show the modal
      $("#dequeue-modal").modal('toggle');
    }

    // Sends a dequeue request to the server.
    // Upon success: Dequeues the first person in line.
    // Upon error: redirect to the error page.
    $scope.dequeueFirstPerson = function () {
      lineUpAPIService.dequeueFirstPerson($routeParams.qid, $scope.userDetails).
        success(function (data, status, headers, config) {
          if (data.SUCCESS) {
            // close the modal
            $("#dequeue-modal").modal('toggle');
          } else {
            // display error message
            $scope.errors = data;
            document.getElementById('dequeue-error').classList.remove('hide');
            document.getElementById('dequeue-confirm').classList.add('disabled');
          }

          // refresh the queue data
          $scope.getDetailedQueueInfo(0);
        }).
        error(function (data, status, headers, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
    }

    //
    $scope.dequeueCancel = function () {
      $scope.errors = {};
      document.getElementById('dequeue-error').classList.add('hide');
      document.getElementById('dequeue-confirm').classList.remove('disabled');
    }

    // Sends a remove request to the server.
    // Upon success: removes the selected person from the line.
    // Upon Error: redirect to the error page.
    $scope.dequeueSelectPerson = function () {
      lineUpAPIService.dequeueSelectPerson({ 'qid': $routeParams.qid, 'uid': $scope.selectedUser.uid }).
        success(function (data, status, headers, config) {
          // refresh the queue data
          $scope.getDetailedQueueInfo($scope.member_list.indexOf($scope.selectedUser));
        }).
        error(function (data, status, headers, config) {
          // not an error we are prepared to handle
          $location.path("/error");
        });
    }

    // Opens a modal dialog that prompts for the name and the optional data.
    // Sends a request to the server to add that name to the queue.
    // Upon Success: the name has been added to the queue
    // Upon Error: redirect to the error page.
    $scope.adminAdd = function () {
      $scope.errors = {};

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
            $scope.getDetailedQueueInfo($scope.member_list.indexOf($scope.selectedUser));

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

    // closes the add user modal window
    $scope.dismissAddModal = function () {
      // clear the error messsages
      $scope.errors = {};
      document.getElementById('error').classList.add('hide');
      $scope.user = {};

      // close the modal window
      $("#addModal").modal('toggle');
    }

    // sends a request to the server to move the user back one position
    $scope.demoteSelectPerson = function () {
      var selectIndex = document.getElementById("list-group").options.selectedIndex;
      if( selectIndex != $scope.member_list.length - 1 ) {
        lineUpAPIService.demoteSelectPerson({ 'qid': $routeParams.qid, 'uid': $scope.selectedUser.uid }).
          success(function (data, status, headers, config) {
            // refresh the queue
            $scope.getDetailedQueueInfo($scope.member_list.indexOf($scope.selectedUser)+1);
          }).
          error(function (data, status, headers, config) {
            // this is not an error we are prepared to handle
            $location.path("/error");
          });
      } else {
        alert("user is already at end of queue!");
      }
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
            $scope.close_icon = "glyphicon glyphicon-play";
            $scope.activeStatus = "CLOSED";
          } else {
            // the queue is open
            $scope.setActiveStatusTo = "Close Queue";
            button.value = 0;
            $scope.close_icon = "glyphicon glyphicon-stop";
            $scope.activeStatus = "OPEN";
          }
        }).
        error(function (data, status, headers, config) {
          // this is not an error we are prepared to handle
          $location.path("/error");
        });
    }

    // open the user details modal window
    $scope.viewDetails = function () {
      var selectedIndex = document.getElementById("list-group").options.selectedIndex;
      if (selectedIndex != -1) {
        $scope.userDetails = $scope.selectedUser;
        $("#details-modal").modal('toggle');
      }
    }

    // create an auto refresh interval
    var autoRefresh = $interval(function () {
       $scope.getDetailedQueueInfo($scope.member_list.indexOf($scope.selectedUser));
     } , REFRESH_INTERVAL);

    // stop the autoRefresh interval when this iFrame is destroyed
    $scope.$on('$destroy', function () {
      if (angular.isDefined(autoRefresh)) {
        $interval.cancel(autoRefresh);
        autoRefresh = undefined;
      }
    })
  });
}());