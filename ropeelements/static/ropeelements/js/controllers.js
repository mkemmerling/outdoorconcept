(function ($, undefined) {'use strict';

angular.module('outdoorconcept.ropeelement.controllers', [])
.controller('RopeElementListController',
    ['$scope', '$window', 'urls', 'Kind', 'RopeElement',
    function ($scope, $window, urls, Kind, RopeElement) {
        var boolean_filters, filters, current_filter;

        $scope.i18n_urls = {
            'en': urls.ropeelements.en.index,
            'de': urls.ropeelements.de.index
        };

        $scope.kinds = Kind.query();

        $scope.difficulty_legend = {from: 1, to: 10};

        boolean_filters = ['child_friendly', 'accessible', 'canope'];
        filters = angular.copy(boolean_filters);
        filters.push('kind');

        $scope.filter = {
            kind: null,
            child_friendly: false,
            accessible: false,
            canope: false
        };
        current_filter = angular.copy($scope.filter);

        function queryRopeElements() {
            var params = {};

            if ($scope.filter.kind) {
                params.kind = $scope.filter.kind.id;
            }
            angular.forEach(boolean_filters, function (name) {
                if ($scope.filter[name]) {
                    params[name] = 'True';
                }
            });
            RopeElement.query(params).$promise.then(function (result) {
                $scope.ropeelements = result;
                // Prevent display of no results message on first load
                $scope.loaded = true;
            });
            current_filter = angular.copy($scope.filter);
        }

        angular.forEach(filters, function (name) {
            $scope.$watch('filter.' + name, function () {
                // Prevent query on first watch
                if (!angular.equals($scope.filter, current_filter)) {
                    queryRopeElements();
                }
            });
        });

        queryRopeElements();
    }
])
.controller('RopeElementOfflineListController',
    ['$scope', '$window', 'urls', 'Kind', 'RopeElement',
    function ($scope, $window, urls, Kind, RopeElement) {
        var boolean_filters, filters, current_filter;

        $scope.i18n_urls = {
            'en': urls.ropeelements.en.offline,
            'de': urls.ropeelements.de.offline
        };

        $scope.kinds = Kind.query();

        $scope.difficulty_legend = {from: 1, to: 10};

        boolean_filters = ['child_friendly', 'accessible', 'canope'];
        filters = angular.copy(boolean_filters);
        filters.push('kind');

        $scope.filter = {
            kind: null,
            child_friendly: false,
            accessible: false,
            canope: false
        };
        current_filter = angular.copy($scope.filter);

        function queryRopeElements() {
            var params = {};

            if ($scope.filter.kind) {
                params.kind = $scope.filter.kind.id;
            }
            angular.forEach(boolean_filters, function (name) {
                if ($scope.filter[name]) {
                    params[name] = 'True';
                }
            });
            RopeElement.query(params).$promise.then(function (result) {
                $scope.ropeelements = result;
                // Prevent display of no results message on first load
                $scope.loaded = true;
            });
            current_filter = angular.copy($scope.filter);
        }

        angular.forEach(filters, function (name) {
            $scope.$watch('filter.' + name, function () {
                // Prevent query on first watch
                if (!angular.equals($scope.filter, current_filter)) {
                    queryRopeElements();
                }
            });
        });

        queryRopeElements();
    }
]);

})(jQuery);
