(function ($, undefined) {'use strict';

angular.module('outdoorconcept.ropeelement.controllers', ['ngResource'])
.factory('RopeElement', ['$resource', 'urls', function ($resource, urls) {
    return $resource(
        urls.api.ropeelement
    );
}])
.controller('RopeElementListController',
    ['$scope', '$window', 'urls', 'RopeElement',
    function ($scope, $window, urls, RopeElement) {
        var boolean_filters, filters, current_filter;

        $scope.i18n_urls = {
            'en': urls.ropeelements.en.index,
            'de': urls.ropeelements.de.index
        };

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

        $scope.kinds = [];

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
                // Populate kinds on load
                if (!$scope.loaded) {
                    angular.forEach(result, function (elements) {
                        $scope.kinds.push(elements.kind);
                    });
                }
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
    ['$scope', '$window', 'urls', 'RopeElement',
    function ($scope, $window, urls, RopeElement) {
        var db, boolean_filters, filters, current_filter;

        $scope.i18n_urls = {
            'en': urls.ropeelements.en.offline,
            'de': urls.ropeelements.de.offline
        };

        $scope.difficulty_legend = {from: 1, to: 10};

        // TODO: test for indexeddb, polyfill?

        // (Re-)create database
        Dexie.getDatabaseNames(function (databases) {
            if (databases.indexOf('outdoorconcept') > -1) {
                new Dexie('outdoorconcept').delete();
            }
            db = new Dexie('outdoorconcept');
            db.version(1).stores({
                elements: 'id, kind'
            });
            db.open();
        });

        $scope.kinds = [];

        RopeElement.query().$promise.then(function (result) {
            $scope.ropeelements = result;
            // Prevent display of no results message on first load
            $scope.loaded = true;

            // Set kinds and populate database with elements
            db.transaction('rw', db.elements, function () {
                var position = 0;

                db.elements.clear();

                angular.forEach(result, function (kind_elements) {
                    var kind_title = kind_elements.kind.title;

                    $scope.kinds.push(kind_elements.kind);

                    angular.forEach(kind_elements.elements, function (element) {
                        db.elements.add({
                            id: 'element/' + position,
                            kind: kind_title,
                            position: position,
                            title: element.title,
                            description: element.description,
                            image: element.image,
                            image_width: element.image_width,
                            thumbnail: element.thumbnail,
                            direction: element.direction,
                            direction_title: element.direction_title,
                            difficulty: element.difficulty,
                            child_friendly: element.child_friendly ? 1 : 0,
                            accessible: element.accessible ? 1 : 0,
                            canope: element.canope ? 1 : 0,
                            ssb: element.ssb
                        });
                        position++;
                    });
                });
            }).catch(function(err) {
                console.error("Error on populating elements table", err.stack || err);
            });
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
            db.transaction('r', db.elements, function () {
                var query = db.elements.where('kind');

                if ($scope.filter.kind) {
                    query = query.equals($scope.filter.kind.title);
                } else {
                    query = query.above('');
                }

                angular.forEach(boolean_filters, function (name) {
                    if ($scope.filter[name]) {
                        query = query.and(function(element) {
                            return element[name];
                        });
                    }
                });

                query.sortBy('position').then(function (result) {
                    var current_kind = null,
                        elements = [];

                    function addElements(kind, elements) {
                        if (elements.length > 0) {
                            $scope.ropeelements.push({
                                kind: {title: kind},
                                elements: elements
                            });
                        }
                    }

                    $scope.ropeelements = [];

                    angular.forEach(result, function(element) {
                        if (element.kind !== current_kind) {
                            addElements(current_kind, elements);
                            elements = [];
                        }
                        current_kind = element.kind;
                        elements.push(element);
                    });

                    addElements(current_kind, elements);
                    $scope.$apply();
                    current_filter = angular.copy($scope.filter);
                });

            }).catch(function(err) {
                console.error("Error on querying elements", err.stack || err);
            });
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
