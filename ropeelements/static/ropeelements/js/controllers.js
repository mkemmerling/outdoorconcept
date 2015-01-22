(function ($, undefined) {'use strict';

angular.module('outdoorconcept.ropeelement.controllers', ['ngResource'])
.factory('RopeElement', ['$resource', 'urls', function ($resource, urls) {
    return $resource(
        urls.api.ropeelement
    );
}])
.controller('RopeElementListController',
    ['$scope', '$location', '$window', 'urls', 'RopeElement',
    function ($scope, $location, $window, urls, RopeElement) {
        var boolean_filters, filters, current_filter;

        $scope.i18n_urls = {
            'en': urls.en.ropeelements,
            'de': urls.de.ropeelements
        };

        $scope.difficulty_legend = {from: 1, to: 10};

        $scope.kinds = [];

        var elements_by_kind = {};

        // TODO: If offline get from local storage to allow for reload
        RopeElement.query().$promise.then(function (result) {
            $scope.ropeelements = result;
            angular.forEach(result, function (kind_elements) {
                $scope.kinds.push(kind_elements.kind);
                elements_by_kind[kind_elements.kind.title] = kind_elements.elements;
            });
            // Prevent display of no results message on first load
            $scope.loaded = true;
        });

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
            var set_boolean_filters, kinds;

            set_boolean_filters = $.grep(boolean_filters, function (name) {
                return $scope.filter[name];
            });

            function getElements(kind) {
                return $.grep(elements_by_kind[kind], function (element) {
                    return ($.grep(set_boolean_filters, function (name) {
                        return element[name];
                    }).length === set_boolean_filters.length) && element;
                });
            }

            kinds = ($scope.filter.kind) ? [$scope.filter.kind] : $scope.kinds;
            $scope.ropeelements = [];
            angular.forEach(kinds, function (kind) {
                var elements = getElements(kind.title);
                if (elements.length > 0) {
                    $scope.ropeelements.push({
                        kind: kind,
                        elements: elements
                    });
                }
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
    }
]);

})(jQuery);
