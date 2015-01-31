(function ($, undefined) {'use strict';

angular.module('outdoorconcept.ropeelement.directives', [])
.directive('difficultyPlot', function () {

    var PLOT_WIDTH = 60,
        PLOT_HEIGHT = 34,
        BAR_H_OFFSET = 4,
        bar_width = PLOT_WIDTH / 10,
        bar_height_factor = (PLOT_HEIGHT - BAR_H_OFFSET) / 10;

    function drawBar(context, nr, rgb) {
        var x = (nr - 1) * bar_width,
            h = BAR_H_OFFSET + nr * bar_height_factor,
            y = PLOT_HEIGHT - h,
            color = rgb.join(', ');

        context.fillStyle = 'rgba('+ color + ', .4)';
        context.fillRect (x, y, 1, h);
        context.fillStyle = 'rgba('+ color + ', .7)';
        context.fillRect (x + 1, y, bar_width - 2, h);
        context.fillStyle = 'rgb('+ color + ')';
        context.fillRect (x + bar_width - 1, y, 1, h);
    }

    function drawPlot(element, from, to) {
        var context = element.getContext('2d'),
            color_map = {
                0: [224, 224, 224],
                1: [0, 208, 0],
                2: [0, 192, 64],
                3: [0, 192, 128],
                4: [0, 128, 224],
                5: [0, 80, 224],
                6: [0, 0, 224],
                7: [240, 0, 188],
                8: [240, 0, 82],
                9: [240, 0, 0],
                10: [32, 32, 32]
            }, i;

        for (i = 1; i <=10; i++) {
            drawBar(context, i, color_map[(i >= from && i <= to) ? i : 0]);
        }
    }

    return {
        require: 'ngModel',

        link: function (scope, $element, attrs) {
            var difficulty = scope.$eval(attrs.ngModel),
                from = difficulty.from,
                to = difficulty.to;

            if (from) {
                drawPlot($element[0], from, (to) ? to : from);
            }
        }
    };
})
.directive('imagePopup', ['$window', function ($window) {
    return {
        link: function (scope, $element, attrs) {
            var screen_sm = 768;

            // $element.on('shown.bs.modal', function (event) {
            //     var trigger = $(event.relatedTarget),
            //         row = trigger.parents('tr'),
            //         thumb = trigger.children('img'),
            //         modal = $(this),
            //         dialog = modal.children('.modal-dialog'),
            //         // Position pop up right of thumbnail ...
            //         left = thumb.offset().left + thumb.outerWidth() + 5,
            //         // ... and centered relative to the element row
            //         row_center = row.offset().top + row.outerHeight() / 2 - $window.scrollY,
            //         dialog_height, top;

            //     $('.modal-body img', modal).attr('src', trigger.data('image'));
            //     $('.modal-dialog', modal).width(trigger.data('width') + 12);

            //     // On desktop position pop up right of icons
            //     if ($window.innerWidth >= screen_sm) {
            //         left += row.find('.icons').outerWidth() + 5;
            //     }

            //     // Position pop up (must be temporarly visible)
            //     dialog_height = dialog.outerHeight();
            //     top = row_center - dialog_height / 2 - 10;
            //     // Ensure pop up does not exceed neither viewport bottom nor top
            //     top += Math.min($window.innerHeight - top - dialog_height - 25, 0);
            //     top = Math.max(top, 0);

            //     dialog.css({
            //         left: left + 'px',
            //         top: top + 'px',
            //     });
            // });


            $element.on('show.bs.modal', function (event) {
                var trigger = $(event.relatedTarget),
                    $row = trigger.parents('tr'),
                    $thumb = trigger.children('img'),
                    $modal = $(this),
                    $dialog = $modal.children('.modal-dialog'),
                    // Position pop up right of thumbnail ...
                    left = $thumb.offset().left + $thumb.outerWidth() + 5,
                    // ... and centered relative to the element row
                    row_center = $row.offset().top + $row.outerHeight() / 2 - $window.scrollY,
                    dialog_height, top;

                console.warn("$row.offset()", $row.offset());
                console.warn("$row.outerHeight()", $row.outerHeight());
                console.warn("$window.scrollY", $window.scrollY);
                console.warn("row_center", row_center);

                $('.modal-body img', $modal).attr('src', trigger.data('image'));
                $dialog.width(trigger.data('width') + 12);

                // On desktop position pop up right of icons
                if ($window.innerWidth >= screen_sm) {
                    left += $row.find('.icons').outerWidth() + 5;
                }

                // Position pop up (must be temporarly visible)
                $element.show();
                console.warn("$dialog.outerHeight()", $dialog.outerHeight());
                dialog_height = $dialog.outerHeight();
                // $element.hide();

                top = row_center - dialog_height / 2 - 10;
                // Ensure pop up does not exceed neither viewport bottom nor top
                top += Math.min($window.innerHeight - top - dialog_height - 25, 0);
                top = Math.max(top, 0);

                $dialog.css({
                    left: left + 'px',
                    top: top + 'px',
                });
            });



        }
    };
}]);

})(jQuery);
