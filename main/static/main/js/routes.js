(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes', ['ngRoute'])
    .config(['$routeProvider', 'languageProvider', function ($routeProvider, languageProvider) {
        // var en, de;
        var default_url;

        // TODO: Try templateUrl function instead?
        // Or even with a :lang attribute (maybe use '/de/ng/seilelemente')
        // We don't need to inject these values, but calling them on resolve
        // allows us to set the language.
        en = function (language) {
            languageProvider.$get().setLanguage('en');
            // language.setLanguage('en');
            // console.warn("ROUTE", window.localStorage);
            // return language;
        };
        // en.$inject = ['language'];

        de = function (language) {
            languageProvider.$get().setLanguage('de');
            // console.warn("ROUTE", window.localStorage);
            // language.setLanguage('de');
            // return language;
        };
        // de.$inject = ['language'];


        // TODO:
        default_url = function () {
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
                resolve: {
                    lang: en
                }
            })
            .when('/de/seilelemente', {
                templateUrl: '/de/ng/ropeelements',
                controller: 'RopeElementListController',
                resolve: {
                    lang: de
                }
            })
            .when('/de/siebert', {
                templateUrl: '/ng/siebert',
                controller: 'SiebertFormController'
            })
            .otherwise({
                redirectTo: default_url
            });
    }]);

})(jQuery);
