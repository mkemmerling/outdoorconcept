(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes', ['ngRoute', 'outdoorconcept.config'])
    .config(['$routeProvider', 'urls', function ($routeProvider, urls) {
        var ropeelement_options, ropeelement_offline_options;

        $routeProvider
            .when(urls.en.ropeelements, {
                templateUrl: urls.en.ng.ropelement_list,
                controller: 'RopeElementListController'
            })
            .when(urls.de.ropeelements, {
                templateUrl: urls.de.ng.ropelement_list,
                controller: 'RopeElementListController'
            })
            .when(urls.siebert, {
                templateUrl: urls.de.ng.siebert_form,
                controller: 'SiebertFormController'
            })
            .otherwise({
                redirectTo: urls.root,
            });
    }]);

})(jQuery);
