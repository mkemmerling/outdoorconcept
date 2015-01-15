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
    }])
    .factory('KindNEW', ['db', function (db) {
        var self = this;

        self.insert = function(data) {
            var params = [
                    data.id,
                    data.title
                ];
            db.query('INSERT INTO kinds VALUES(?, ?)', params);
        };

        // return DB.query('SELECT * FROM documents')
        // .then(function(result){
        //     return DB.fetchAll(result);
        // });

        return self;
    }])
    .factory('Element', ['db', function (db) {
        var self = this;

        self.insert = function(kind_id, data) {
            var params = [
                    data.id,
                    kind_id,
                    data.title,
                    data.description,
                    data.direction,
                    data.direction_title
                ];
            db.query('INSERT INTO elements VALUES(?, ?, ?, ?, ?, ?)', params);
        };

        return self;
    }]);

})();
