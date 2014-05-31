'use strict';

/* Services */
/*
 These services are used to encapsulate communication with the server
 Each function defined for the LineupAPI service object can be called
 from the angular controllers without having to specify get, post, etc
 not server 'routes' like "/createQueue" and "/modifyQueue"
*/
angular.module('LineUpApp.services', []).
  service('lineUpAPIService', function($http) {

    var lineUpAPI = {};

    /*
    param: 
    'queue' is an object dictionary that containes all
    of the fields set by the user from the create_queue.html page.
    It will contain at minimum 2 fields:
      1. 'qname' - the name associated with the queue
      2. 'active' - an integer that represents whether or not the 
          queue is active (0 = not active, 1 = active)
          but all others may or may not be present.
    */
    lineUpAPI.createQueue = function (queue) {
      return $http.post('/createQueue', queue);
    }

    /*
    param: 
    'queue' is a dictionary that contains 2 fields:
     1. 'qid' - a unique number identifier of a queue
     2. 'q_settings' - a dictionary that contains all of 
         the fields entered by the user from the 
         edit_queue.html page.

    */
		lineUpAPI.editQueue = function (queue) {
			return $http.post('/editQueue', queue);
		}

    /*
      param:
      'qid' - a unique number identifier of a queue
    */
    lineUpAPI.getQueueSettings = function (qid) {
      return $http.post('/getQueueSettings', qid);
    }

   // lineUpAPI.modifyQueue = function (queueSettings) {
   //   return $http.post('/modifyQueue', queueSettings);
   // }

    /*
      param:
      'qid' - a unique number identifier of a queue
    */
		lineUpAPI.getDetailedQueueInfo = function (qid) {
			return $http.post('/managerView/' + qid);
		}

    /* FINSISH COMMENTING THIS ONCE CHANGES ARE COMMITTED
      param:
      'qid' - a unique number identifier of a queue
      'userDetails' - a dictionary with 3 fields:
        1. username - 
        2. optionaldata - 
        3. uid - 
    */
		lineUpAPI.dequeueFirstPerson = function (qid, userDetails) {
			return $http.post('/dequeue/' + qid, userDetails);
		}

    /*
      param:
      'data' - a dictionary with 2 fields:
        1. 'qid' - a unique number identifier of a queue
        2. 'uid' - a unique number identifier of a user
    */
		lineUpAPI.dequeueSelectPerson = function (data) {
			return $http.post('/remove', data);
		}

    lineUpAPI.getPopularQueues = function () {
      return $http.get('/popular');
    }

    /*
      param:
      'query' - a string containing search words
    */
    lineUpAPI.search = function (query) {
      return $http.post('/search', query);
    }

    /*
      param:
      'qid' - a unique number identifier of a queue
      'data' - an int that represents the queue's active status
      (0 = not active, 1 = active)
    */
		lineUpAPI.setActive = function (qid, data) {
			return $http.post('/setActive/' + qid, data);
		}

      /*
      param:
      'data' - a dictionary with three objects
        1. 'qid' - a unique number identifier of a queue
        2. 'uname' - the user's name
        3. 'optional_data' - a string of optional information
           provided by the user
    */
    lineUpAPI.joinQueue = function (data) {
      return $http.post('/join', data);
    }

    /*
      param:
      'user' - a dictionary with two objects
        1. 'uname' - a string identifier for a user
        2. 'pw' - a string that is the password of the user
    */
    lineUpAPI.login = function (user) {
      return $http.post('/login', user);
    }

    /* DEPRECATED
      param:
      'user' - a dictionary with two objects
        1. 'uname' - a string identifier for a user
        2. 'pw' - a string that is the password of the user
    
    lineUpAPI.createUser = function (user) {
      return $http.post('/createUser', user);
    }
    */

    lineUpAPI.getUsersQueues = function () {
      return $http.post('/myQueues');
    }

    /*
      param:
      'qid' - a unique number identifier of a queue
    */
    lineUpAPI.queueStatus = function (qid) {
      return $http.get('/queueStatus/' + qid);
    }

    /*
      param:
      'qid' - a unique number identifier of a queue
    */
    lineUpAPI.postpone = function (qid) {
      return $http.post('/postpone', qid);
    }

    /*
      param:
      'data' - a dictionary with 2 fields:
        1. 'qid' - a unique number identifier of a queue
        2. 'uid' - a unique number identifier of a user
    */
		lineUpAPI.demoteSelectPerson = function (data) {
			return $http.post('/managerPostpone', data);
		}

    /*
      param:
      'qid' - a unique number identifier of a queue
    */
    lineUpAPI.leaveQueue = function (qid) {
      return $http.post('/leaveQueue', qid);
    }

    /*
      param:
      'qid' - a unique number identifier of a queue
      'user' - a dictionary with two fields
        1. 'uname' - a string identifier for a user
        2.  'optional_data' - a string of optional information
           provided by the user
    */
    lineUpAPI.enqueue = function (qid, user) {
      return $http.post('/enqueue/' + qid, user);
    }
		
		lineUpAPI.getCurrentUser = function () {
			return $http.post('/currentUser');
		}

    return lineUpAPI;
  }).

  service('lineUpUserService', function ($http) {
    var userData = { uname: "", pw: "" };

    
    this.getUser = function () {
      return userData;
    };

    /*
      param:
      'user' - a dictionary with two objects
        1. 'uname' - a string identifier for a user
        2. 'pw' - a string that is the password of the user
    */
    this.saveUser = function (user) {
      userData = user;
    };

    /*
      param:
      'user' - a dictionary with two objects
        1. 'uname' - a string identifier for a user
        2. 'pw' - a string that is the password of the user
    */
    this.login = function (user) {
      return $http.post('/login', user);
    };

    /*
      param:
      'user' - a dictionary with two objects
        1. 'uname' - a string identifier for a user
        2. 'pw' - a string that is the password of the user
    */
    this.createUser = function (user) {
      return $http.post('/createUser', user);
    }
  });