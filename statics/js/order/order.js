export function numberWithCommas(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}


// *** Convert total-price to thousan-separator value

let totalPriceElem = document.querySelector('#total-price');
totalPriceElem.innerHTML = numberWithCommas(totalPriceElem.innerHTML);


// *** 
document.querySelector('.header-cart-quantity').innerHTML = document.querySelector('#total-quantity').innerHTML;