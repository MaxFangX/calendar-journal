/*jslint devel: true, browser: true, jquery: true */
/*global getCookie */

var analyticsApp = window.angular.module('analyticsApp.services', []);

analyticsApp.factory('CalendarFilterService', ['$rootScope', function CalendarFilterService($rootScope) {
  var filterData =  {
    start: undefined, // ISO String
    end: undefined, // ISO String
    timeRange: undefined,
    type: undefined,
  };

  return {
    getFilter: function() {
      return filterData;
    },
    setFilter: function(start, end, type) {
      filterData.start = start;
      filterData.end = end;
      filterData.type = type;
      filterData.timeRange = filterData.start.toISOString() + " " + filterData.end.toISOString();
      $rootScope.$broadcast('calendarFilter:updated');
    }
  };
}]);

analyticsApp.service("TagService", ['$http', '$q', function($http, $q) {

  var _this = this;

  this.tags = {};

  this.getTags = function(timeRange, start, end) {

    if (!timeRange) {
      throw "timeRange must always be supplied";
    }

    if (start || end) {
      // If the start and end time match the given timeRange
      if (timeRange !== start.toISOString() + " " + end.toISOString()) {
        throw "timeRange doesn't match given start and end times";
      }
    }

    // Attempt to return cached tags
    if (_this.tags[timeRange]) {
      return $q.when(_this.tags[timeRange]);
    }

    // Request the tags and return a promise
    return $http({
      method: 'GET',
      url: '/v1/tags.json',
      cache: true,
      params: {
        start: (start)? start.toISOString() : null,
        end: (end)? end.toISOString() : null,
      }
    }).then(function successCallback(response) {
      _this.tags[timeRange] = [];
      for (var i = 0; i < response.data.results.length; i++) {
        var tag = response.data.results[i];
        _this.tags[timeRange].push({
          id: tag.id,
          label: tag.label,
          keywords: tag.keywords,
          hours: tag.hours
        });
      }
      return _this.tags[timeRange];
    }, function errorCallback(response) {
      /* jshint unused:vars */
      console.log("Failed to get tags");
    });
  };

  this.createTag = function(label, keywords) {
    return $http({
      method: 'POST',
      url: '/v1/tags.json',
      data: $.param({
        label: label,
        keywords: keywords,
        csrfmiddlewaretoken: getCookie('csrftoken')
      }),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  };

  this.editTag = function(tagId, newLabel, newKeywords) {
    return $http({
      method: 'POST',
      url: '/v1/tags/' + tagId,
      data: $.param({
        label: newLabel,
        keywords: newKeywords,
        csrfmiddlewaretoken: getCookie('csrftoken'),
        _method: 'PATCH'
      }),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(function successCallback(response) {
      return response.data;
    }, function errorCallback() {
      console.log("Failed to edit tag with id " + tagId);
      return null;
    });
  };

  this.deleteTag = function(tagId) {
    return $http({
      method: 'POST',
      url: '/v1/tags/' + tagId,
      data: $.param({
        csrfmiddlewaretoken: getCookie('csrftoken'),
        _method: 'DELETE'
      }),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  };

}]);

analyticsApp.service('CategoryService', ['$http', '$q', function($http, $q) {

  var _this = this;

  this.categories = {};

  this.getCategories = function(timeRange, start, end) {
    if (!timeRange) {
      throw "timeRange must always be supplied";
    }

    if (start || end) {
      // If the start and end time match the given timeRange
      if (timeRange !== start.toISOString() + " " + end.toISOString()) {
        throw "timeRange doesn't match given start and end times";
      }
    }

    // Attempt to return cached categories
    if (_this.categories[timeRange]) {
      return $q.when(_this.categories[timeRange]);
    }

    // Request the categories and return a promise
    return $http({
      method: 'GET',
      url: '/v1/colorcategories.json',
      cache: true,
      params: {
        start: (start)? start.toISOString() : null,
        end: (end)? end.toISOString() : null,
      }
    }).then(function successCallback(response) {
      _this.categories[timeRange] = [];
      for (var i = 0; i < response.data.results.length; i++) {
        var category = response.data.results[i];
        _this.categories[timeRange].push({
          id: category.id,
          label: category.label,
          hours: category.hours,
          include: true,
          color: category.category_color,
        });
      }
      return _this.categories[timeRange];
    }, function errorCallback(response) {
      /* jshint unused:vars */
      console.log("Failed to get categories");
    });
  };

  this.editCategory = function(categoryId, newLabel) {
    return $http({
      method: 'POST',
      url: '/v1/colorcategories/' + categoryId,
      data: $.param({
        label: newLabel,
        csrfmiddlewaretoken: getCookie('csrftoken'),
        _method: 'PATCH'
      }),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(function successCallback(response) {
      return response.data;
    }, function errorCallback() {
      console.log("Failed to edit category with id " + categoryId);
      return null;
    });
  };

  this.deleteCategory = function(categoryId) {
    return $http({
      method: 'POST',
      url: '/v1/colorcategories/' + categoryId,
      data: $.param({
        csrfmiddlewaretoken: getCookie('csrftoken'),
        _method: 'DELETE'
      }),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  };

}]);

analyticsApp.service('QueryService', function() {
  this.populateData = function(data, type) {
    var ctrlDetails = [];
    var maxYValue = 0;
    var events = [];
    for (var i = 0; i < data.length; i++) {
      var event = data[i];
      var date = new Date(event[0]);
      var hours = event[1];
      if (hours > maxYValue) {
        maxYValue = hours;
      }
      events.push({
        x: date,
        y: hours
      });
    }
    ctrlDetails = [{
      values: events,
      key: type + ' Graph',
      color: '#003057',
      strokeWidth: 2,
    }];
    return [ctrlDetails, maxYValue];
  };
});
