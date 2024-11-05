/*check to see if service worker is supported on the browser. The main purpose of this code is to enable offline capabilities and 
enhance performance for the web application by utilizing a service worker, allowing for features like caching and background sync. 
*/
if('serviceWorker' in navigator) { //if service worker is supported on browser
    navigator.serviceWorker.register('/sw.js')
    .then((reg) => console.log('service worker registered', reg)) //succesful
    .catch((err) => console.log('service worker not registered', err)); //catch errors

}