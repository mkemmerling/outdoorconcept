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
        var storage = $window.sessionStorage;

        function setLanguage(language) {
            try {
                storage.setItem('language', language);
            } catch (e) {
                // Safari sets storage quota to 0 when private surfing is activated,
                // i.e. 'getItem' works, but getItem' fails.
                $('#content').hide();
                $('#storageDisabledAlert').show();
                return;
            }
        }

        if (storage.getItem('language') === null) {
            setLanguage(($window.navigator.language === 'de') ? 'de' : 'en');
        }
        return {
            getLanguage: function () {
                return storage.getItem('language');
            },
            setLanguage: setLanguage
        };
    }])
    .controller('AppController', ['$scope', '$window', function($scope, $window) {
        var cacheStatusValues = [],
            cache = window.applicationCache,
            $updated_popup = $('#appcacheUpdatedPopUp');

        $scope.modernizr = Modernizr;

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
            console.warn("manifest redownloaded RELOAD ROUTE");
            $scope.debug_msg = "manifest redownloaded";
            $('#appcacheUpdatedPopUp').modal();
        }, false);

        $updated_popup.on('hidden.bs.modal', function () {
            $window.location.reload();
        }).keypress(function(e) {
            if(e.keyCode == 13) {
                $updated_popup.modal('hide');
            }
        });

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
