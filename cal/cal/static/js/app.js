/*jslint devel: true, browser: true, jquery: true */
/*global d3, moment */

var analyticsApp = window.angular.module('analyticsApp', ['analyticsApp.services', 'nvd3', 'ui.calendar']);

analyticsApp.controller('LoggedInCtrl', function LoggedInController($scope, $window) {
  $scope.init = function() {
    angular.element(document).ready(function () {
        $window.location.href = '/v1/sync?sync_all=true';
    });
  };
});
