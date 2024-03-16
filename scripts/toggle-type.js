function showArticles(articleTypeToShow) {
    console.log("showArticles called", articleTypeToShow);

    // Show only the articles of the type that was clicked
    var articles = document.querySelectorAll(".item-card");
    for (var i = 0; i < articles.length; i++) {
        if (articles[i].classList.contains(articleTypeToShow)) {
            // Add show class, remove hide class
            articles[i].classList.add("show");
            articles[i].classList.remove("hide");
        } else {
            // Add hide class, remove show class
            articles[i].classList.add("hide");
            articles[i].classList.remove("show");
        }
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
