// Toggle the dropdown content when the dropdown is clicked
// Close the dropdown if the user clicks outside of it or on the dropdown button

function openDropdown() {
    var dd = this.getElementsByClassName("dropdown-content")[0];
    if (dd.classList.contains("show")) {
        dd.classList.remove("show");
        dd.classList.add("hide");
    } else {
        dd.classList.remove("hide");
        dd.classList.add("show");
    }
}

function addDropdownEventListeners() {
    let dropdowns = document.getElementsByClassName("dropdown");
    for (let i = 0; i < dropdowns.length; i++) {
        dropdowns[i].addEventListener("click", openDropdown);
    }
}

document.addEventListener("DOMContentLoaded", addDropdownEventListeners);

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
