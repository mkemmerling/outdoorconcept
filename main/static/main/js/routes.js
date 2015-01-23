(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes', ['ngRoute'])
    .config(['$routeProvider', function ($routeProvider) {
        var en, de;

        en = function (language) {
            language.setLanguage('en');
            return language;
        };
        en.$inject = ['language'];

        de = function (language) {
            language.setLanguage('de');
            return language;
        };
        de.$inject = ['language'];

        $routeProvider
            .when('/en/ropeelements', {
                templateUrl: '/en/ng/ropeelements',
                controller: 'RopeElementListController',
                resolve: {
                    language: en
                }
            })
            .when('/de/seilelemente', {
                templateUrl: '/de/ng/ropeelements',
                controller: 'RopeElementListController',
                resolve: {
                    language: de
                }
            })
            .when('/de/siebert', {
                templateUrl: '/ng/siebert',
                controller: 'SiebertFormController'
            })
            .otherwise({
                redirectTo: '/',
            });
    }]);

})(jQuery);
