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

		lineUpAPI.dequeueFirstPerson = function (qid, uid) {
			return $http.post('/dequeue/' + qid, uid);
		}

		lineUpAPI.dequeueSelectPerson = function (data) {
			return $http.post('/remove', data);
		}

    lineUpAPI.getPopularQueues = function () {
      return $http.get('/popular');
    }

    lineUpAPI.search = function (query) {
      return $http.post('/search', query);
    }

		lineUpAPI.setActive = function (qid, data) {
			return $http.post('/setActive/' + qid, data);
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

		lineUpAPI.demoteSelectPerson = function (data) {
			return $http.post('/managerPostpone', data);
		}

    lineUpAPI.leaveQueue = function (qid) {
      return $http.post('/leaveQueue', qid);
    }

    lineUpAPI.enqueue = function (qid, user) {
      return $http.post('/enqueue/' + qid, user);
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
      return $http.post('/login', user);
    };

    this.createUser = function (user) {
      return $http.post('/createUser', user);
    }
  });