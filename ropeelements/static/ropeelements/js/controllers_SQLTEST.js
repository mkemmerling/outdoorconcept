(function ($, undefined) {'use strict';

angular.module('outdoorconcept.ropeelement.controllers', [])

    .controller('RopeElementListController',
        ['$scope', '$window', 'urls', 'kinds', 'ropeelements', 'RopeElement', 'KindNEW', 'Element',
        function ($scope, $window, urls, kinds, ropeelements, RopeElement, KindNEW, Element) {
            var screen_sm = 768,
                boolean_filters, filters, current_filter;

            $scope.i18n_urls = urls.ropeelements;

            $scope.kinds = kinds;
            $scope.ropeelements = ropeelements;



            console.log('INIT RopeElementListController', ropeelements);

            ropeelements.$promise.then(function (ropeelements) {
                console.log(ropeelements);
                angular.forEach(ropeelements, function(ropeelement) {
                    KindNEW.insert(ropeelement.kind);
                    angular.forEach(ropeelement.elements, function(element) {
                        Element.insert(ropeelement.kind.id, element);
                    });
                });
            });



            $scope.difficulty_legend = {from: 1, to: 10};

            boolean_filters = ['child_friendly', 'accessible', 'canope'];
            filters = angular.copy(boolean_filters);
            filters.push('kind');

            $scope.filter = {
                kind: null,
                child_friendly: false,
                accessible: false,
                canope: false
            };
            current_filter = angular.copy($scope.filter);


            $('#imagePopUp').on('shown.bs.modal', function (event) {
                var trigger = $(event.relatedTarget),
                    row = trigger.parents('tr'),
                    thumb = trigger.children('img'),
                    modal = $(this),
                    dialog = modal.children('.modal-dialog'),
                    // Position pop up right of thumbnail ...
                    left = thumb.offset().left + thumb.outerWidth() + 5,
                    // ... and centered relative to the element row
                    row_center = row.offset().top + row.outerHeight() / 2 - $window.scrollY,
                    dialog_height, top;

                $('.modal-body img', modal).attr('src', trigger.data('image'));
                $('.modal-dialog', modal).width(trigger.data('width') + 12);

                // On desktop position pop up right of icons
                if ($window.innerWidth >= screen_sm) {
                    left += row.find('.icons').outerWidth() + 5;
                }

                // Position pop up (must be temporarly visible)
                dialog_height = dialog.outerHeight();
                top = row_center - dialog_height / 2 - 10;
                // Ensure pop up does not exceed neither viewport bottom nor top
                top += Math.min($window.innerHeight - top - dialog_height - 25, 0);
                top = Math.max(top, 0);

                dialog.css({
                    left: left + 'px',
                    top: top + 'px',
                });
            });

            function queryRopeElements() {
                var params = {};

                if ($scope.filter.kind) {
                    params.kind = $scope.filter.kind.id;
                }
                angular.forEach(boolean_filters, function (name) {
                    if ($scope.filter[name]) {
                        params[name] = 'True';
                    }
                });
                $scope.ropeelements = RopeElement.query(params);
                current_filter = angular.copy($scope.filter);
            }

            angular.forEach(filters, function (name) {
                $scope.$watch('filter.' + name, function () {
                    // Prevent query on first watch
                    if (!angular.equals($scope.filter, current_filter)) {
                        queryRopeElements();
                    }
                });
            });
        }
    ]);

})(jQuery);
