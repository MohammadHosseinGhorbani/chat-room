const html = document.getElementsByTagName("html")[0];
html.setAttribute("data-bs-theme", sessionStorage.getItem("theme") ?? "dark");
function changeColorMode() {
            if (html.getAttribute("data-bs-theme") === "light") {
                html.setAttribute("data-bs-theme", "dark");
                sessionStorage.setItem("theme", "dark");
            }
            else {
                html.setAttribute("data-bs-theme", "light");
                sessionStorage.setItem("theme", "light");
            }
}