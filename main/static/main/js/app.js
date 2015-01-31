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
    .run(['$rootScope', '$location', function ($rootScope, $location) {
        var history = [];

        $rootScope.$on('$routeChangeSuccess', function() {
            history.push($location.$$path);
        });

        $rootScope.goBack = function () {
            var previous_url = history.length > 1 ? history.splice(-2)[0] : '/';
            $location.path(previous_url);
        };
    }])
    .controller('AppController', ['$rootScope', '$window', '$timeout', function($rootScope, $window, $timeout) {
        var cacheStatusValues = [],
            cache = window.applicationCache,
            $appcache_downloaded = $('#appcacheDownloadedPopUp'),
            $appcache_updated = $('#appcacheUpdatedPopUp'),
            hide_modal;

        $rootScope.modernizr = Modernizr;

        hide_modal = function (event) {
            if(event.keyCode == 13) {
                $(this).modal('hide');
            }
        };

        cache.addEventListener('cached', function () {
            $appcache_downloaded.modal();
        }, false);

        cache.addEventListener('updateready', function () {
            $appcache_updated.modal();
        }, false);

        $appcache_downloaded.on('shown.bs.modal', function (event) {
            var dialog = $(this);
            $timeout(function () {
            //     dialog.fadeOut('slow', function () {
                    dialog.modal('hide');
                // });
            }, 5000);
        }).keypress(hide_modal);

        $appcache_updated.on('hidden.bs.modal', function () {
            $window.location.reload();
        }).keypress(hide_modal);
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
