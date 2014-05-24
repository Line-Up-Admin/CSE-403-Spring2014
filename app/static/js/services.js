'use strict';

/* Services */
angular.module('LineUpApp.services', []).
  service('lineUpAPIService', function($http) {

    var lineUpAPI = {};

    lineUpAPI.createQueue = function (queue) {
      return $http.post('/createQueue', queue);
    }

		lineUpAPI.editQueue = function (queue) {
			return $http.post('/editQueue', queue);
		}

    lineUpAPI.getQueueSettings = function (qid) {
      return $http.post('/getQueueSettings', qid);
    }

    lineUpAPI.modifyQueue = function (queueSettings) {
      return $http.post('/modifyQueue', queueSettings);
    }

		lineUpAPI.getDetailedQueueInfo = function (qid) {
			return $http.post('/managerView/' + qid);
		}

		lineUpAPI.dequeueFirstPerson = function (qid) {
			return $http.post('/dequeue/' + qid);
		}
		
		lineUpAPI.dequeueSelectPerson = function (data) {
			return $http.post('/remove/' + data);
		}

    lineUpAPI.getPopularQueues = function () {
      return $http.get('/popular');
    }

    lineUpAPI.search = function (query) {
      console.log(query);
      return $http.post('/search', query);
    }

		lineUpAPI.setActive = function (data) {
			return $http.post('/setActive', data);
		}

    lineUpAPI.joinQueue = function (data) {
      return $http.post('/join', data);
    }

    lineUpAPI.login = function (user) {
      return $http.post('/login', user);
    }

    lineUpAPI.createUser = function (user) {
      return $http.post('/createUser', user);
    }

    lineUpAPI.getUsersQueues = function () {
      return $http.post('/myQueues');
    }

    lineUpAPI.queueStatus = function (qid) {
      return $http.get('/queueStatus/' + qid);
    }

    lineUpAPI.postpone = function (qid) {
      return $http.post('/postpone', qid);
    }

    return lineUpAPI;
  }).

  service('lineUpUserService', function ($http) {
    var userData = { uname: "", pw: "" };

    this.getUser = function () {
      return userData;
    };

    this.saveUser = function (user) {
      userData = user;
    };

    this.login = function (user) {
      console.log(user);
      return $http.post('/login', user);
    };

    this.createUser = function (user) {
      console.log(user);
      return $http.post('/createUser', user);
    }
  });