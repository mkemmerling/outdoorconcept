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
});

})(jQuery);
