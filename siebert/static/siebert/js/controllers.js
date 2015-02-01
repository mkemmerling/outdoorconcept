(function ($, undefined) {'use strict';

angular.module('outdoorconcept.siebert.controllers', [])
.controller('SiebertFormController', ['$scope', '$window', function ($scope, $window) {

    $scope.print = function () {
        // TODO: Validate required fields
        $window.location.href = '/de/siebert/siebert.pdf';
    };

}]);

})(jQuery);
