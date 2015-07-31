(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes', ['ngRoute'])
    .config(['$routeProvider', 'languageProvider', function ($routeProvider, languageProvider) {
        var language = languageProvider.$get();

        $routeProvider
            .when('/en/ropeelements', {
                templateUrl: function () {
                    language.setLanguage('en');
                    return '/en/ng/ropeelements';
                },
                controller: 'RopeElementListController'
            })
            .when('/de/seilelemente', {
                templateUrl: function () {
                    language.setLanguage('de');
                    return '/de/ng/ropeelements';
                },
                controller: 'RopeElementListController'
            })
            .when('/en/siebert', {
                templateUrl: function () {
                    language.setLanguage('en');
                    return '/en/ng/siebert';
                },
                controller: 'SiebertFormController'
            })
            .when('/de/siebert', {
                templateUrl: function () {
                    language.setLanguage('de');
                    return '/de/ng/siebert';
                },
                controller: 'SiebertFormController'
            })
            .when('/:lang/offline', {
                templateUrl: function (params) {
                    language.setLanguage(params.lang);
                    return '/' + params.lang + '/ng/offline';
                }
            })
            .otherwise({
                redirectTo: function () {
                    if (language.getLanguage() === 'de') {
                        return '/de/seilelemente';
                    } else {
                        return '/en/ropeelements';
                    }
                }
            });
    }]);

})(jQuery);
