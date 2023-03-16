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
