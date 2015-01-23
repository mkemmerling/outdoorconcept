(function ($, Modernizr, undefined) {'use strict';

angular.module('outdoorconcept.base', [])
   .config(['$interpolateProvider', function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }])
    .config(['$locationProvider', function ($locationProvider) {
        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });
    }])
    .config(['$httpProvider', function ($httpProvider) {
        // Ensure Django's request.is_ajax() method returns True
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        // See e.g. http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])
    .factory('language', ['$window', function ($window) {
        if ($window.localStorage.getItem('language') === null) {
            $window.localStorage.setItem('language', ($window.navigator.language === 'de') ? 'de' : 'en');
        }
        return {
            getLanguage: function () {
                return $window.localStorage.getItem('language');
            },
            setLanguage: function (language) {
                $window.localStorage.setItem('language', language);
            }
        };
    }])
    .controller('AppController', ['$scope', 'language', function($scope, language) {
        $scope.modernizr = Modernizr;
    }]);

angular.module('outdoorconcept.app', [
    'ngSanitize',
    'outdoorconcept.base',
    'outdoorconcept.directives',
    'outdoorconcept.routes',
    'outdoorconcept.ropeelement.directives',
    'outdoorconcept.ropeelement.controllers',
    'outdoorconcept.siebert.controllers'
]);

})(jQuery, Modernizr);
