window.onload = function () {
        if (performance.navigation.type === 1) {
            location.reload();
        }
    };
console.log("Page loaded and refreshed on navigation");