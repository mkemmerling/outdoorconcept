(function ($, undefined) {'use strict';

angular.module('outdoorconcept.siebert.controllers', [])
.controller('SiebertFormController', ['$scope', '$window', 'language', function ($scope, $window, language) {
    $scope.siebert = {};

    $scope.numberPatternMinError = function (field) {
        return field.$error.number || field.$error.pattern || field.$error.min;
    };

    $scope.numberMinMaxError = function (field) {
        return field.$error.number || field.$error.min || field.$error.max;
    };

    // TODO:
    function siebertFormula(p, q, f, l) {
        var term1 = (q * l * l + 2 * p * l) / (8 * f),
            term2 = (q * l + p) / 2;
        return Math.sqrt(term1 * term1 + term2 * term2);
    }

    // See https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/round
    // and http://stackoverflow.com/questions/11832914/round-to-at-most-2-decimal-places-in-javascript
    function round(num) {
        return + (Math.round(num + 'e+1')  + 'e-1');
    }

    $scope.calculate = function () {

        // console.log('SiebertFormController', $scope.SiebertForm);

        var values = $scope.siebert,
            isDefined = angular.isDefined;

        if (isDefined(values.flyingFox) && isDefined(values.nrPersons)) {
            values.p = 600 - 300 * values.flyingFox + 80 * (values.nrPersons - 1);
            if ($scope.SiebertForm.$valid) {
                // console.log("CALCULATE");
                values.fz_excl = siebertFormula(values.p, values.q, values.f, values.l);
                // TODO: calculation is still bogus
                values.fz_excl = round(values.fz_excl / 100);
                values.fz_incl = round(3 * values.fz_excl);
            } else {
                values.fz_excl = values.fz_incl = null;
            }
        } else {
            values.p = values.fz_excl = values.fz_incl = null;
        }
    };

    $scope.print = function () {
        // TODO: Not working with IE
        var date_options = {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            },
            url = '/de/siebert/siebert.pdf',
            params;

        params = angular.copy($scope.siebert);
        console.log('SiebertFormController', params);
        if (params.flyingFox === '0') {
            delete params.flyingFox;
        }
        if (angular.isObject(params.date)) {
            params.date = params.date.toLocaleDateString(language.getLanguage(), date_options);
            console.log('SiebertFormController', params.date, encodeURIComponent(params.date), $.param({date: params.date}));
        } else {
            delete params.date;
        }

        params = $.param(params);
        if (params) {
            url += '?' + params;
        }

        console.log('SiebertFormController', params);
        $window.location.href = url;
    };

}]);

})(jQuery);
