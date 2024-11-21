
function toggleSidebar() {
    const openIcon = document.querySelector("#open-sidebar");
    const closeIcon = document.querySelector("#close-sidebar");
    const sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("collapsed");
    if (sidebar.classList.contains("collapsed")) {
        openIcon.classList.remove("hidden");
        closeIcon.classList.add("hidden");
    } else {
        openIcon.classList.add("hidden");
        closeIcon.classList.remove("hidden");
    }
}