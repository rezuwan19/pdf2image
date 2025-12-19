function searchDashboard() {
    let input = document.getElementById("searchBox").value.toLowerCase();
    let items = document.getElementsByClassName("search-item");

    for (let i = 0; i < items.length; i++) {
        let text = items[i].innerText.toLowerCase();
        items[i].style.display = text.includes(input) ? "" : "none";
    }
}
