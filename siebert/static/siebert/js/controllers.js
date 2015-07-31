(function ($, undefined) {'use strict';

angular.module('outdoorconcept.siebert.controllers', [])
.controller('SiebertFormController',
    ['$scope', '$window', 'language', function ($scope, $window, language) {
        var lang = language.getLanguage(),
            ropeelements_urls = {
                'en': '/en/ropeelements',
                'de': '/de/seilelemente',
            };

        $scope.ropeelements_url = ropeelements_urls[lang];

        $scope.i18n_urls = {
            'en': '/en/siebert',
            'de': '/de/siebert'
        };

        if (!$scope.modernizr.inputtypes.date) {
            $.datepicker.setDefaults($.datepicker.regional[lang]);
            $scope.datePickerOptions = {
                changeYear: true,
                changeMonth: true,
                yearRange: 'c-2:c+2'
            };
        }

        $scope.printDisabled = true;

        $scope.siebert = {};

        function siebertFormula(p, q, f, l) {
            var q1 = q / 1000,
                factor = 1 / 101.97,
                term1 = (q1 * l * l + 2 * p * l) * (factor / (8 * f)),
                term2 = (q1 * l + p) * factor / 2;
            return Math.sqrt(term1 * term1 + term2 * term2);
        }

        // See https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/round
        // and http://stackoverflow.com/questions/11832914/round-to-at-most-2-decimal-places-in-javascript
        function round(num, decimals) {
            decimals = decimals || 1;
            return + (Math.round(num + 'e+' + decimals)  + 'e-' + decimals);
        }

        $scope.calculate = function () {
            var values = $scope.siebert,
                isDefined = angular.isDefined;

            if (isDefined(values.flyingFox) && isDefined(values.nrPersons)) {
                values.p = (values.nrPersons === 0) ? 0 : 600 - 300 * values.flyingFox + 80 * (values.nrPersons - 1);
                if ($scope.SiebertForm.$valid) {
                    values.fz_excl = siebertFormula(values.p, values.q, values.f, values.l);
                    values.fz_incl = round(3 * values.fz_excl);
                    values.fz_excl = round(values.fz_excl);
                } else {
                    values.fz_excl = values.fz_incl = undefined;
                }
            } else {
                values.p = values.fz_excl = values.fz_incl = undefined;
            }
            $scope.printDisabled = !isFinite($scope.siebert.fz_excl);
        };

        $scope.print = function () {
            var date_options = {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                },
                url = '/' + lang + '/siebert/siebert.pdf',
                params = angular.copy($scope.siebert),
                date_param;

            if (params.flyingFox === '0') {
                delete params.flyingFox;
            }

            // Working around strange IE behaviour adding (encoded) quotes when URL encoding date string.
            date_param = (angular.isObject(params.date)) ?
                $.param({date: params.date.toLocaleDateString(language.getLanguage(), date_options)}).replace(/%E2%80%8E/g, '') :
                null;
            delete params.date;

            // Cause of required fields (non date) params are always guaranteed to be present.
            params = $.param(params);
            if (date_param) {
                params += '&' + date_param;
            }

            $window.location.href = ($window.navigator.onLine) ? (url + '?' + params) : $window.location.href;
        };

    }
]);

})(jQuery);
