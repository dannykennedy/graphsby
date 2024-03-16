function showArticles(articleTypeToShow) {
    console.log("showArticles called", articleTypeToShow);

    // Show only the articles of the type that was clicked
    var articles = document.querySelectorAll(".item-card");

    // Reorder the articles to show the selected type first
    var newArticles = [];
    for (var i = 0; i < articles.length; i++) {
        if (articles[i].classList.contains(articleTypeToShow)) {
            // Add show class, remove hide class
            articles[i].classList.add("show");
            articles[i].classList.remove("hide");
            newArticles.push(articles[i]);
        }
    }
    for (var i = 0; i < articles.length; i++) {
        if (!articles[i].classList.contains(articleTypeToShow)) {
            // Add hide class, remove show class
            articles[i].classList.add("hide");
            articles[i].classList.remove("show");
            newArticles.push(articles[i]);
        }
    }

    // Remove all articles from the grid
    var grid = document.querySelector(".main-grid");
    while (grid.firstChild) {
        grid.removeChild(grid.firstChild);
    }

    // Add the new articles to the grid
    for (var i = 0; i < newArticles.length; i++) {
        grid.appendChild(newArticles[i]);
    }

    // Set button to selected
    var buttons = document.querySelectorAll(".type-toggle-pill");
    for (var i = 0; i < buttons.length; i++) {
        // If button classlist includes articleTypeToShow, add the active class
        if (buttons[i].classList.contains(articleTypeToShow)) {
            buttons[i].classList.add("active");
        } else {
            buttons[i].classList.remove("active");
        }
    }

    // // Initialize MiniMasonry
    var mainMasonry = new MiniMasonry({
        container: ".main-grid",
        minify: false,
        basewidth: 350,
        gutterX: 20,
        gutterY: 20,
    });

    mainMasonry.layout();

    // // Layout the articles
    // masonry.layout();

    // // Remove MiniMasonry
    // masonry.destroy();
}
