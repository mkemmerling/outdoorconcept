(function ($, undefined) {'use strict';

angular.module('outdoorconcept.directives', ['outdoorconcept.base'])
.directive('switchLanguage', ['$location', 'language', function ($location, language) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var select = element.find("select[name='language']"),
                urls = angular.fromJson(attrs.switchLanguage);

            select.change(function () {
                var lang = select.val();
                language.setLanguage(lang);
                $location.path(urls[lang]);
                scope.$apply();
            });
        }
    };
}])
.directive('movable', ['$document', function ($document) {
    return {
        restrict: 'A',
        scope: { handleSelector: '@dragHandle' },
        link: function (scope, element) {
            var handle, startX, startY;

            handle = (scope.handleSelector) ? element.find(scope.handleSelector) : element;

            element.css('position', 'relative');
            handle.css('cursor', 'move');

            handle.on('mousedown', function (event) {
                var left = parseInt(element.css('left'), 10),
                    top = parseInt(element.css('top'), 10);

                // Prevent default dragging of selected content
                event.preventDefault();

                if (isNaN(left)) {
                    left = element.position().left;
                }
                startX = left - event.pageX;

                if (isNaN(top)) {
                    top = element.position().top;
                }
                startY = top - event.pageY;

                $document.on('mousemove', mousemove);
                $document.on('mouseup', mouseup);
            });

            function mousemove(event) {
                var x = startX + event.pageX,
                    y = startY + event.pageY;

                element.css({
                    top: y + 'px',
                    left: x + 'px'
                });
            }

            function mouseup() {
                $document.off('mousemove', mousemove);
                $document.off('mouseup', mouseup);
            }
        }
    };
}])
.directive('numberMaxLength', function() {
    return {
        require: 'ngModel',
        restrict: 'A',
        link: function (scope, element, attrs, ngModelController) {
            var maxlength = Number(attrs.numberMaxLength);

            function userInput(number) {
                var string_value = String(number);

                if (string_value.length > maxlength) {
                    string_value = string_value.slice(0, maxlength);
                    number = Number(string_value);
                    ngModelController.$setViewValue(string_value);
                    ngModelController.$render();
                }
                return number;
            }
            ngModelController.$parsers.push(userInput);
        }
    };
})
// .config(function() {
//     $.datepicker.setDefaults({
//         minDate: new Date(1900, 0, 1),
//         maxDate: new Date(2200, 0, 1)
//     });
// })
.directive('datePicker', ['$timeout', function ($timeout) {
    return {
        require: 'ngModel',
        link: function (scope, element, attrs, ngModelController) {
            var current_date,
                // The (localized) display format of the date, set on 'setUpDatePicker'.
                date_format = '';

            // Note: Use '$.datepicker.formatDate' and $.datepicker.parseDate'
            // utility functions to convert date strings to and from Date object
            // to avoid timezone problems.

            /* Parse ISO formatted date string into date object */
            function parseISODate(date) {
                if (angular.isDefined(date) && date !== null) {
                    try {
                        date = $.datepicker.parseDate($.datepicker.ISO_8601, date);
                    } catch (error) {
                        throw new Error(
                            "ng-Model value '" + angular.toJson(date) + "' for '" +
                            attrs.name + "' is not an ISO-formatted date."
                        );
                    }
                }
                return date;
            }

            /* Throw error if date lower than min date or greater than max date. */
            // function verifyMinMaxDate(date) {
            //     var inst, minDate, maxDate;
            //     if (date) {
            //         inst = $.datepicker._getInst(element[0]);
            //         minDate = $.datepicker._getMinMaxDate(inst, "min");
            //         if (minDate && date < minDate) {
            //             throw new Error('Year too small');
            //         }
            //         maxDate = $.datepicker._getMinMaxDate(inst, "max");
            //         if (maxDate && date > maxDate) {
            //             throw new Error('Year too large');
            //         }
            //     }
            // }

            /* Set date on model and date picker.
             *
             * Passed 'date' is supposed to be Date object.
             *
             * Set date on the datepicker since it might not have been entered
             * in the format specified by 'date_format'.
             */
            function setDate(date) {
                element.datepicker('setDate', $.datepicker.formatDate(date_format, date));
                ngModelController.$setViewValue($.datepicker.formatDate($.datepicker.ISO_8601, date) || null);
                current_date = date;
            }

            /* Verify and update date
             *
             * If verification fails, date is reset to the current date.
             */
            function updateModel() {
                scope.$apply(function () {
                    var date = element.datepicker('getDate'),
                        input_date;
                    try {
                        input_date = $.datepicker.parseDate(date_format, element.val());
                        // verifyMinMaxDate(input_date);
                        setDate(date);
                    } catch (error) {
                        setDate(current_date);
                    }
                });
            }

            // /* Update date on select of month and/or year */
            function onChangeMonthYear(userHandler) {
                return function (year, month, inst) {
                    if (current_date) {
                        // Invoke 'setDate' within the $apply block; the 1 millisecond
                        // delay is required by the karma test.
                        $timeout(function () {
                            setDate(new Date(year, month - 1, inst.selectedDay));
                        }, 1, true);
                    }
                    if (userHandler) {
                        // Caller has specified their own onChangeMonthYear handler
                        // so call this as well.
                        return userHandler(year, month, inst);
                    }
                 };
            }

            function setUpDatePicker() {
                var options = scope.$eval(attrs.datePicker) || {};
                // Bind to the date picker event triggered on select to a new month and/or year
                options.onChangeMonthYear = onChangeMonthYear(options.onChangeMonthYear);
                // Bind to element's change event to update model when date is selected
                // by the date picker or entered directly in the input box.
                element.bind('change', updateModel);
                // Remove any previous date picker, to ensure any config changes are picked up
                element.datepicker('destroy');
                // Create the new datepicker widget
                element.datepicker(options);
                date_format = element.datepicker('option', 'dateFormat');
                // Render will update the date picker with the date
                ngModelController.$render();
            }

            // Set current date from model
            current_date = parseISODate(scope.$eval(attrs.ngModel));

            ngModelController.$formatters.push(function (datestring) {
                return parseISODate(datestring);
            });

            ngModelController.$render = function () {
                var value = ngModelController.$viewValue;
                value = (!value) ? null : new Date(value);
                element.datepicker('setDate', $.datepicker.formatDate(date_format, value));
            };

            // Watch for changes to the directive options
            scope.$watch(attrs.datePicker, setUpDatePicker, true);

            // Calendar button click handler
            element.parent('.input-group').find('.ui-datepicker-trigger').click(function () {
                element.datepicker(($.datepicker._datepickerShowing) ? 'hide' : 'show');
            });
        }
    };
}]);

})(jQuery);
