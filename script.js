window.onbeforeunload = function () {
    window.scrollTo(0, 0);
  }


// Check if the page is being reloaded
if (performance.navigation.type === 1) {
    // Redirect to index.html
    window.location.href = '/index.html';
}