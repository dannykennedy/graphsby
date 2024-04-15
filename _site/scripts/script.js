// .navbar-item.dropdown {
//     position: relative;
// }

// .dropdown-content {
//     display: none;
//     position: absolute;
//     background-color: #f9f9f9;
//     min-width: 160px;
//     box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
//     z-index: 1;
// }

{
    /* <div id="navbar-links">
<!-- Dropdown for 'topics' -->
<div class="navbar-item dropdown">
    <span>Topics</span>
    <div class="dropdown-content">
        <a href="../bcpov6darticles/articles">Articles</a>
        <a href="../bcpov6dinterviews/interviews">Interviews</a>
        <a href="../bcpov6dpoetry/poetry">Poetry</a>
        <a href="../bcpov6dreviews/reviews">Reviews</a>
        <a href="../bcpov6dvisualarts/visual-arts">Visual Arts</a>
    </div>
</div>
<div>
    ... */
}

// Toggle the dropdown content when the dropdown is clicked
// Close the dropdown if the user clicks outside of it or on the dropdown button

function openDropdown() {
    let dropdowns = document.getElementsByClassName("dropdown");
    for (let i = 0; i < dropdowns.length; i++) {
        dropdowns[i].addEventListener("click", function () {
            var dd = this.getElementsByClassName("dropdown-content")[0];
            if (dd.classList.contains("show")) {
                dd.classList.remove("show");
                dd.classList.add("hide");
            } else {
                dd.classList.remove("hide");
                dd.classList.add("show");
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", openDropdown);

window.addEventListener("click", function (event) {
    var clickedInsideDropdown =
        event.target.classList.contains("dropdown") ||
        event.target.classList.contains("dropdown-content") ||
        event.target.classList.contains("dropdown-header");

    if (!clickedInsideDropdown) {
        let dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            if (dropdowns[i].classList.contains("show")) {
                dropdowns[i].classList.remove("show");
                dropdowns[i].classList.add("hide");
            }
        }
    }
});
