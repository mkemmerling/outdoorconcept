(function ($, undefined) {'use strict';

angular.module('outdoorconcept.ropeelement.controllers', ['ngResource'])
.factory('RopeElement', ['$resource', function ($resource) {
    return $resource(
        '/:language/api/ropeelements'
    );
}])
.controller('RopeElementListController',
    ['$scope', '$window', '$timeout', 'language', function ($scope, $window, $timeout, language) {
        var lang = language.getLanguage(),
            siebert_urls = {
                'en': '/en/siebert',
                'de': '/de/siebert',
            },
            storage = $window.sessionStorage,
            kinds_by_id = {},
            elements_by_kind = {},
            boolean_filters, filters, empty_filter;

        $scope.siebert_url = siebert_urls[lang];

        $scope.i18n_urls = {
            'en': '/en/ropeelements',
            'de': '/de/seilelemente'
        };

        $scope.difficulty_legend = {from: 1, to: 10};

        $scope.kinds = [];

        $scope.ropeelements = angular.fromJson($window.localStorage.getItem('ropeelements_' + lang));

        angular.forEach($scope.ropeelements, function (kind_elements) {
            $scope.kinds.push(kind_elements.kind);
            kinds_by_id[kind_elements.kind.id] = kind_elements.kind;
            elements_by_kind[kind_elements.kind.id] = kind_elements.elements;
        });

        boolean_filters = ['child_friendly', 'accessible', 'canope'];
        filters = angular.copy(boolean_filters);
        filters.push('kind');
        filters.push('difficulty');
        empty_filter = {
            kind: null,
            difficulty: null,
            child_friendly: false,
            accessible: false,
            canope: false
        };

        function queryRopeElements() {
            var set_boolean_filters, kinds;

            set_boolean_filters = $.grep(boolean_filters, function (name) {
                return $scope.filter[name];
            });

            function filterDifficulty(element) {
                var filter = $scope.filter.difficulty,
                    i;
                if (filter === null) {
                    return true;
                } else {
                    for(i=filter.range[0]; i<=filter.range[1]; i++) {
                        if (i >= element.difficulty.from && i <= element.difficulty.to) {
                            return true;
                        }
                    }
                    return false;
                }
            }

            function filterBoolean(element) {
                return $.grep(set_boolean_filters, function (name) {
                        return element[name];
                    }).length === set_boolean_filters.length;
            }

            function getElements(kind) {
                return $.grep(elements_by_kind[kind.id], function (element) {
                    return filterDifficulty(element) && filterBoolean(element) && element;
                });
            }

            // We track kinds by their ids to ensure that the selected kind is
            // preserved on language switch. Also note that in rare cases
            // a kind might be gone after reload.
            if ($scope.filter.kind && kinds_by_id[$scope.filter.kind.id] !== undefined) {
                kinds = [kinds_by_id[$scope.filter.kind.id]];
            } else {
                kinds = $scope.kinds;
            }

            $scope.ropeelements = [];
            angular.forEach(kinds, function (kind) {
                var elements = getElements(kind);
                if (elements.length > 0) {
                    $scope.ropeelements.push({
                        kind: kind,
                        elements: elements
                    });
                }
            });
        }

        $scope.filter = angular.fromJson(storage.getItem('elementFilter'));
        if (!$scope.filter) {
            $scope.filter = empty_filter;
            storage.setItem('elementFilter', angular.toJson($scope.filter));
        }

        angular.forEach(filters, function (name) {
            $scope.$watch('filter.' + name, function () {
                // Prevent query on first watch
                if ($scope.loaded) {
                    queryRopeElements();
                    storage.setItem('elementFilter', angular.toJson($scope.filter));
                }
            });
        });

        if (!angular.equals($scope.filter, empty_filter)) {
            queryRopeElements();
        }

        // Prevent filtering and display of no results message until loaded
        $timeout(function () {
            $scope.loaded = true;
        });
    }
]);

})(jQuery);
