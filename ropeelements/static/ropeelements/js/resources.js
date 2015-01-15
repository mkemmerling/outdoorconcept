(function (undefined) {'use strict';

angular.module('outdoorconcept.ropeelement.resources', ['ngResource', 'outdoorconcept.config'])
    .factory('Kind', ['$resource', 'urls', function ($resource, urls) {
        return $resource(
            urls.api.kind
        );
    }])
    .factory('RopeElement', ['$resource', 'urls', function ($resource, urls) {
        return $resource(
            urls.api.ropeelement
        );
    }]);

})();
