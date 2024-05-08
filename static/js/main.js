window.onscroll = function showHeader() {
    let header = document.querySelector('.header');

    if (window.pageYOffset > 200) {
        header.classList.add('header__fixed');
    } else {
        header.classList.remove('header__fixed');

    }
}
// function copyTextToClipboard() {
//     var text = "Ваш текст для копирования"; // Замените эту строку на текст, который вы хотите скопировать

//     var dummy = document.createElement("textarea");
//     document.body.appendChild(dummy);
//     dummy.value = text;
//     dummy.select();
//     document.execCommand("copy");
//     document.body.removeChild(dummy);

//     // alert("Текст скопирован в буфер обмена: " + text);
// }