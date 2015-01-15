(function ($, undefined) {'use strict';

angular.module('outdoorconcept.routes',
    ['ngRoute', 'outdoorconcept.config', 'outdoorconcept.ropeelement.resources'])
    .config(['$routeProvider', 'urls', function ($routeProvider, urls) {
        var getRopeKinds, getRopeElements, ropeelement_options;

        getRopeKinds = function (Kind) {
            return Kind.query();
        };
        getRopeKinds.$inject = ['Kind'];

        getRopeElements = function (RopeElement) {
            return RopeElement.query();
        };
        getRopeElements.$inject = ['RopeElement'];

        ropeelement_options = {
            templateUrl: urls.ng.ropelement_list,
            controller: 'RopeElementListController',
            resolve: {
                kinds: getRopeKinds,
                ropeelements: getRopeElements
            }
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
