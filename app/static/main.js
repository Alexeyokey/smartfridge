document.addEventListener("DOMContentLoaded", function () {
    let currentPage = parseInt(new URLSearchParams(window.location.search).get("page")) || 1;

    document.getElementById("prevPage").addEventListener("click", function () {
        if (currentPage > 1) {
            changePage(currentPage - 1);
        }
    });

    document.getElementById("nextPage").addEventListener("click", function () {
        changePage(currentPage + 1);
    });

    function changePage(page) {
        const url = new URL(window.location.href);
        url.searchParams.set("page", page);
        window.location.href = url.toString();
    }
});
