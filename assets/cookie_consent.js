/**
 * This vanilla JS script displays cookie consent bar 
 * if not previously closed by the user.
 * After closing the bar 'cookieConsent' cookie is set to record this action.
 */

/**
 * Get the value of a cookie
 * Source: https://gist.github.com/wpsmith/6cf23551dd140fb72ae7
 * @param  {String} name  The name of the cookie
 * @return {String}       The cookie value
 */
function getCookie (name) {
  let value = `; ${document.cookie}`;
  let parts = value.split(`; ${name}=`);
	
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
}

/**
 * Sets a cookie
 * @param {String} name
 * @param {String} value
 * @param {String} path     '/' by default
 * @param {Number} maxAge   30 days by default
 */
function setCookie (name, value, path, maxAge) {
  const oneMonth = 60/*s*/ * 60/*min*/ * 24/*h*/ * 30/*day*/;

  document.cookie = `${name}=${value}; Path=${path || '/'};` +
    ' Max-Age=' + (maxAge || oneMonth) + ';' +
    ' SameSite=strict;';
}


document.addEventListener('DOMContentLoaded', function () {

  if (getCookie('cookieConsent') !== 'yes') {
    for (const selector of ['.cookie-consent', '.cookie-consent-gap']) {
      for (const elem of document.querySelectorAll(selector)) {
        elem.classList.remove('d-none');
      }
    }
  }

  for (const elem of document.querySelectorAll('.cookie-consent__close')) {
    elem.onclick = function (_event) {
      setCookie('cookieConsent', 'yes');
      for (const bar of document.querySelectorAll('.cookie-consent-gap')) {
        bar.classList.add('d-none');
      }
      for (const bar of document.querySelectorAll('.cookie-consent')) {
        bar.classList.add('fade-leave-active', 'fade-leave-to');
        window.setTimeout(() => {
          bar.classList.add('d-none');
        }, 800);
      }
    };
  }
});
