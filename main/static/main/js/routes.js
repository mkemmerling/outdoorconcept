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
            .when('/de/siebert', {
                templateUrl: '/ng/siebert',
                controller: 'SiebertFormController'
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
