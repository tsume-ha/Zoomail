var menuCheckbox = document.getElementById('nav-toggle');
menuCheckbox.addEventListener('change', function () {
    if (menuCheckbox.checked) {
        // add ?login=true to the URL
        var currentUrl = window.location.href;
        var urlSearchParams = new URLSearchParams(window.location.search);
        urlSearchParams.set('login', 'true');
        var newUrl = currentUrl.split('?')[0] + '?' + urlSearchParams.toString();
        history.pushState(null, null, newUrl);
    } else {
        // remove ?login=true from the URL
        var currentUrl = window.location.href;
        var urlSearchParams = new URLSearchParams(window.location.search);
        urlSearchParams.delete('login');
        var newUrl = currentUrl.split('?')[0] + '?' + urlSearchParams.toString();
        history.pushState(null, null, newUrl);
    }
});