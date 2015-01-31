(function (window, undefined) {'use strict';
var cacheStatusValues = [],
    cache = window.applicationCache;

cacheStatusValues[0] = 'uncached';
cacheStatusValues[1] = 'idle';
cacheStatusValues[2] = 'checking';
cacheStatusValues[3] = 'downloading';
cacheStatusValues[4] = 'updateready';
cacheStatusValues[5] = 'obsolete';

function logEvent(e) {
    var message = 'online: ' + ((window.navigator.onLine) ? 'yes' : 'no');
    message += ', event: ' + e.type;
    message += ', status: ' + cacheStatusValues[cache.status];
    if (e.type === 'progress' && e.loaded !== undefined) {
        message += ' (' + e.loaded + ' of ' + e.total + ')';
    }
    if (e.type === 'error' && window.navigator.onLine) {
        message += ' (prolly a syntax error in manifest)';
    }
    console.log(message);
}

cache.addEventListener('cached', logEvent, false);
cache.addEventListener('checking', logEvent, false);
cache.addEventListener('downloading', logEvent, false);
cache.addEventListener('error', logEvent, false);
cache.addEventListener('noupdate', logEvent, false);
cache.addEventListener('obsolete', logEvent, false);
cache.addEventListener('progress', logEvent, false);
cache.addEventListener('updateready', logEvent, false);

})(window);
