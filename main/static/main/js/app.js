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
        var storage = $window.localStorage;

        if (storage.getItem('language') === null) {
            storage.setItem('language', ($window.navigator.language === 'de') ? 'de' : 'en');
        }
        return {
            getLanguage: function () {
                return storage.getItem('language');
            },
            setLanguage: function (language) {
                storage.setItem('language', language);
            }
        };
    }])
    .controller('AppController', ['$scope', '$window', '$route', 'language', function($scope, $window, $route, language) {
        $scope.modernizr = Modernizr;

        var cacheStatusValues = [],
            cache = window.applicationCache;

        cacheStatusValues[0] = 'uncached';
        cacheStatusValues[1] = 'idle';
        cacheStatusValues[2] = 'checking';
        cacheStatusValues[3] = 'downloading';
        cacheStatusValues[4] = 'updateready';
        cacheStatusValues[5] = 'obsolete';

        $scope.debug_msg = "–––";

        cache.addEventListener('noupdate', function () {
            console.warn("No manifest update");
            $scope.debug_msg = "No manifest update";
            $scope.$apply();
        }, false);

        cache.addEventListener('downloading', function () {
            console.warn("Downloading manifest");
            $scope.debug_msg = "Downloading manifest";
            $scope.$apply();
        }, false);

        cache.addEventListener('cached', function () {
            console.warn("manifest cached");
            $scope.debug_msg = "manifest cached";
            $scope.$apply();
        }, false);

        cache.addEventListener('updateready', function () {
            console.warn("manifest redownloaded");
            $scope.debug_msg = "manifest redownloaded";
            $window.applicationCache.swapCache();

            $window.localStorage.removeItem('ropeelements_en');
            $window.localStorage.removeItem('ropeelements_de');

            $route.reload();
        }, false);

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
