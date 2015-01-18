(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes', ['ngRoute', 'outdoorconcept.config'])
    .config(['$routeProvider', 'urls', function ($routeProvider, urls) {
        var getRopeKinds, getRopeElements, ropeelement_options;

        ropeelement_options = {
            templateUrl: urls.ng.ropelement_list,
            controller: 'RopeElementListController'
        };

        $routeProvider
            .when(urls.ropeelements.en, ropeelement_options)
            .when(urls.ropeelements.de, ropeelement_options)
            .when(urls.siebert, {
                templateUrl: urls.ng.siebert_form,
                controller: 'SiebertFormController'
            })
            .otherwise({
                redirectTo: urls.root,
            });
    }]);

})(jQuery);
