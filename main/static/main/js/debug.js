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
    var online, status, type, message;
    online = (navigator.onLine) ? 'yes' : 'no';
    status = cacheStatusValues[cache.status];
    type = e.type;
    message = 'online: ' + online;
    message += ', event: ' + type;
    message += ', status: ' + status;
    if (type == 'error' && navigator.onLine) {
        message += ' (prolly a syntax error in manifest)';
        alert(e);
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

// window.applicationCache.addEventListener(
//     'updateready',
//     function(){
//         window.applicationCache.swapCache();
//         console.log('swap cache has been called');
//     },
//     false
// );

// setInterval(function(){
//     cache.update();
// }, 10000);

})(window);
