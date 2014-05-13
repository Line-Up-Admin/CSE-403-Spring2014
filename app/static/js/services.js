'use strict';

/* Services */
angular.module('LineUpApp.services', []).
  service('lineUpAPIService', function($http) {

    var lineUpAPI = {};

    lineUpAPI.createQueue = function (queue) {
      return $http.post('/createQueue', queue);
    }

    lineUpAPI.getQueue = function (qid) {
      return $http.post('/debug/getqueuesettings', qid);
    }

    lineUpAPI.getPopularQueues = function () {
      return $http.get('/popular')
    }
    return lineUpAPI;
  });