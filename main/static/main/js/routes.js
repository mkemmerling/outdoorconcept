(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes', ['ngRoute', 'outdoorconcept.config'])
    .config(['$routeProvider', 'urls', function ($routeProvider, urls) {
        var ropeelement_options, ropeelement_offline_options;

        ropeelement_options = {
            templateUrl: urls.ng.ropelement_list,
            controller: 'RopeElementListController'
        };
        ropeelement_offline_options = {
            templateUrl: urls.ng.ropelement_list,
            controller: 'RopeElementOfflineListController'
        };

        $routeProvider
            .when(urls.ropeelements.en.index, ropeelement_options)
            .when(urls.ropeelements.en.offline, ropeelement_offline_options)
            .when(urls.ropeelements.de.index, ropeelement_options)
            .when(urls.ropeelements.de.offline, ropeelement_offline_options)
            .when(urls.siebert, {
                templateUrl: urls.ng.siebert_form,
                controller: 'SiebertFormController'
            })
            .otherwise({
                redirectTo: urls.root,
            });
    }]);

})(jQuery);
