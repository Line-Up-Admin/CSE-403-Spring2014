'use strict';

/* Services */
angular.module('LineUpApp.services', []).
  service('lineUpAPIService', function($http) {

    var lineUpAPI = {};

    lineUpAPI.createQueue = function (queue) {
      return $http.post('/createQueue', queue);
    }

    lineUpAPI.getQueueSettings = function (qid) {
      return $http.post('/getQueueSettings', qid);
    }

		lineUpAPI.getDetailedQueueInfo = function (qid) {
			return $http.post('/employeeView/' + qid);
		}
		
    lineUpAPI.getPopularQueues = function () {
      return $http.get('/popular');
    }

    lineUpAPI.joinQueue = function (data) {
      console.log(data);
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

    return lineUpAPI;
  });