(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes', ['ngRoute'])
    .config(['$routeProvider', function ($routeProvider) {
        var en, de;

        // // We don't need to inject these values, but calling them on resolve
        // // allows us to set the language.
        // en = function (language) {
        //     language.setLanguage('en');
        //     // console.warn("ROUTE", window.localStorage);
        //     // return language;
        // };
        // en.$inject = ['language'];

        // de = function (language) {
        //     // console.warn("ROUTE", window.localStorage);
        //     language.setLanguage('de');
        //     // return language;
        // };
        // de.$inject = ['language'];

        // var TEST_en = function () {
        //     return window.localStorage.getItem('ropeelements_en');
        // };
        // var TEST_de = function () {
        //     return window.localStorage.getItem('ropeelements_de');
        // };

        $routeProvider
            .when('/en/ropeelements', {
                templateUrl: '/en/ng/ropeelements',
                controller: 'RopeElementListController',
                // resolve: {
                //     lang: en
                //     // TEST: TEST_en
                // }
            })
            .when('/de/seilelemente', {
                templateUrl: '/de/ng/ropeelements',
                controller: 'RopeElementListController',
                // resolve: {
                //     lang: de
                //     // TEST: TEST_de
                // }
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
