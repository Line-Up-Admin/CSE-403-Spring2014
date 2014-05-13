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

    lineUpAPI.getPopularQueues = function () {
      return $http.get('/popular');
    }

    lineUpAPI.joinQueue = function () {
      return $http.post('/joinQueue');
    }

    return lineUpAPI;
  });