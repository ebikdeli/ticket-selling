// *** Change all price to thousand separator text
function numberWithCommas(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}
Array.from(document.querySelectorAll('.price-value')).forEach(elem => {
    elem.innerHTML = numberWithCommas(elem.innerHTML);
})