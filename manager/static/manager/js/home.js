
function copyUrlToClipboard(relative) {
    let field = document.createElement('textarea');
    field.value = document.location.host + relative;
    document.body.appendChild(field);
    field.select();
    document.execCommand('copy');
    document.body.removeChild(field);
}

function displayCopyUrlButtons() {
    let buttons = document.getElementsByClassName("copy-url-button");
    for (let i = 0; i < buttons.length; i++) {
        buttons.item(i).style.display = "block";
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
   displayCopyUrlButtons();
});