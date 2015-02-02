(function ($, undefined) {'use strict';

angular.module('outdoorconcept.siebert.controllers', [])
.controller('SiebertFormController', ['$scope', '$window', function ($scope, $window) {
    $scope.siebert = {};

    $scope.print = function () {
        var date_options = {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            },
            url = '/de/siebert/siebert.pdf',
            params;

        // TODO: Validate required fields
        // console.log('SiebertFormController', $scope.siebert);

        params = angular.copy($scope.siebert);
        if (params.flyingFox === '0') {
            delete params.flyingFox;
        }
        if (angular.isObject(params.date)) {
            params.date = params.date.toLocaleDateString('de-AT', date_options);
        } else {
            delete params.date;
        }
        params = $.param(params);
        if (params) {
            url += '?' + params;
        }

        // console.log('SiebertFormController', url);
        $window.location.href = url;
    };

}]);

})(jQuery);
