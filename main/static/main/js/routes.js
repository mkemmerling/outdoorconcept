(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes', ['ngRoute'])
    .config(['$routeProvider', 'languageProvider', function ($routeProvider, languageProvider) {
        // var en, de;
        var default_url;

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

        default_url = function (a, b, c) {
            // console.warn("default_url", a, b, c, window);
            // console.warn("default_url", languageProvider, languageProvider.$get().getLanguage());
            // return '/de/seilelemente';
            var lang = languageProvider.$get().getLanguage();
            console.log("default_url", lang);
            if (lang === 'de') {
                return '/de/seilelemente';
            } else {
                return '/en/ropeelements';
            }
        };


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
                // redirectTo: '/de/seilelemente'
                redirectTo: default_url
            });
    }]);

})(jQuery);
