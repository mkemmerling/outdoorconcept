(function (undefined) {'use strict';

angular.module('outdoorconcept.ropeelement.db', [])
.constant('DB_CONFIG', {
    name: 'ropeelements',
    version: '1.0',
    displayName: 'Rope Elements',
    maxSize: -1,
    tables: [
        {
            name: 'kinds',
            columns: [
                {name: 'id', type: 'integer primary key'},
                {name: 'title', type: 'text'}
            ]
        },
        {
            name: 'elements',
            columns: [
                {name: 'id', type: 'integer primary key'},
                {name: 'kind_id', type: 'integer'},
                {name: 'title', type: 'text'},
                {name: 'description', type: 'text'},
                {name: 'direction', type: 'text'},
                {name: 'direction_title', type: 'text'},
                {name: 'accessible', type: 'text'}
            ]
        }
    ]
})
.factory('db', function($q, DB_CONFIG) {
    var self = this;
    self.database = null;

    console.log('window.indexedDB', window.indexedDB);

    self.init = function() {
        self.database = window.openDatabase(DB_CONFIG.name, DB_CONFIG.version, DB_CONFIG.displayName, DB_CONFIG.maxSize);

        angular.forEach(DB_CONFIG.tables, function(table) {
            var columns = [],
                query;

            angular.forEach(table.columns, function(column) {
                columns.push(column.name + ' ' + column.type);
            });

            query = 'CREATE TABLE IF NOT EXISTS ' + table.name + ' (' + columns.join(', ') + ')';
            self.query(query);
            console.log('Table ' + table.name + ' initialized');
        });
    };

    self.query = function(query, params) {
        params = typeof params !== 'undefined' ? params : [];
        var deferred = $q.defer();

        self.database.transaction(function(transaction) {
            transaction.executeSql(query, params, function(transaction, result) {
                deferred.resolve(result);
            }, function(transaction, error) {
                deferred.reject(error);
            });
        });

        return deferred.promise;
    };

    return self;
})
.run(function(db) {
    db.init();
});

})();
