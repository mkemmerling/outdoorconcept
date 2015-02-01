(function ($, undefined) {'use strict';

angular.module('outdoorconcept.siebert.controllers', [])
.controller('SiebertFormController', ['$scope', '$window', function ($scope, $window) {

    $scope.pdftest = function () {
        $window.location.href = '/de/siebert/test.pdf';
    };

}]);

})(jQuery);
