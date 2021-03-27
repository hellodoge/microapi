
function copy_api_url() {
    let field = document.getElementById("api-url-field");
    field.select();
    document.execCommand('copy');
}