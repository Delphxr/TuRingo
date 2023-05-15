// function to set a given theme/color-scheme
function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
}

function playSound(audioName, loop = false) {
    let audio = new Audio(audioName);
    audio.loop = loop
    audio.play();
    return audio;
}


function startLoading() {
    let loadingCircle = document.createElement("div")
    loadingCircle.classList.add("overlay")
    loadingCircle.innerHTML =
        '<div class="overlay__inner">' +
        '<div class="overlay__content"><span class="spinner"></span></div>' +
        '</div>';

    let circle = document.body.appendChild(loadingCircle)
    return circle;
}




function tabManager(tab) {
    const tabs = document.querySelectorAll(".tab-pane");

    tabs.forEach(tab => {
        tab.classList.remove("active");
        tab.classList.remove("show");
        
    });

    const tab3 = document.getElementById(tab);
    tab3.classList.add("active");
    tab3.classList.add("show");
}