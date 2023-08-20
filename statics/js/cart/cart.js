// Base cart template and script:
// https://codepen.io/justinklemm/pen/kyMjjv
// ??? To not make users wait for server response, we always assume changes in the cart were successful. So we change in front before server respond with the result
import {addOne, minuseOne} from '../functions.js';
import {sendPostData} from '../ajax.js';


// *** Convert number to a Comma separator string
function numberWithCommas(x) {
  return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}


// *** Convert back a comma separator string to Number
function parseToNumber(str) {
  return parseFloat(str.replaceAll(',', ''));
}


// *** Change all price to thousand separator text
Array.from(document.querySelectorAll('.price-value')).forEach(elem => {
  elem.innerHTML = numberWithCommas(elem.innerHTML);
})


const calculateTotalPrice = () => {
  // * This function calculate total price of the order and return it. If no product found, return 'null'
  var totalPriceUnits = document.querySelectorAll('.total-price-unit');
  var totalPrice = document.querySelector('#total-price');
  var price = 0;
  if (totalPriceUnits == undefined){
      return null
  }
  Array.from(totalPriceUnits).forEach(totalPriceUnit => {
      price += parseToNumber(totalPriceUnit.innerHTML);
  })
  totalPrice.innerHTML = numberWithCommas(price);
  return price;
}
calculateTotalPrice()



// *** Calculate 'total-quantity'
const headerCartQuantity = document.querySelector('.header-cart-quantity');
const calculateTotalQuantity = () => {
  // * This function calculate total quantity of the order and return it
  var cartQuantityNumbers = document.querySelectorAll('.cart-quantity-number')
  var totalquantity = document.querySelector('#total-quantity');
  var quantity = 0;
  Array.from(cartQuantityNumbers).forEach(cartQuantityNumber => {
      quantity += Number(cartQuantityNumber.value)
  })
  totalquantity.innerHTML = quantity;
  headerCartQuantity.innerHTML = quantity;
  return quantity;
}
calculateTotalQuantity()


const ticketUnits = document.querySelectorAll('.ticket-unit')
const errorMsgElem = document.querySelector('.error-msg');

// *** Cart funtionalities

Array.from(ticketUnits).forEach(ticketUnit =>{
  ticketUnit.addEventListener('click', e => {
    const inputQuantityElem = ticketUnit.querySelector('.cart-quantity-number');
    errorMsgElem.innerHTML = '';
    // ? Increase item by one
    if(e.target.closest('.cart-quantity-inc')){
      let ticketId = inputQuantityElem.getAttribute('data-ticket-id');
      let cartId = document.querySelector('input[name="cart-id"]').value;
      let quantity = Number(inputQuantityElem.value);
      // Only change increase quantity if quantity is less than 150
      if(quantity < 150){
        let url = `${location.protocol}//${location.host}/cart/change-ticket-cart`;
        let data = {'quantity': quantity+1, 'ticket-id': ticketId,'cart-id': cartId}
        increaseOne(url, data, inputQuantityElem);
        inputQuantityElem.value = quantity + 1;
        ticketUnit.querySelector('.total-price-unit').innerHTML = numberWithCommas(
          parseToNumber(ticketUnit.querySelector('.price-unit').innerHTML) * (quantity + 1)
        )
        calculateTotalPrice();
        calculateTotalQuantity()
      }
    }
    // ? Decrease item by one
    if(e.target.closest('.cart-quantity-dec')){
      let data = {};
      let url = '';
      let ticketId = inputQuantityElem.getAttribute('data-ticket-id');
      let cartId = document.querySelector('input[name="cart-id"]').value;
      let quantity = Number(inputQuantityElem.value);
      if(quantity == 1){
        url = `${location.protocol}//${location.host}/cart/delete-ticket-cart`;
        data = {'ticket-id': ticketId, 'cart-id': cartId}
        // removeTicket(url, data, ticketUnit);
        // ! simulate successful ticket removal from cart
        ticketUnit.remove();
        calculateTotalPrice();
        calculateTotalQuantity();
        // Check if cart is empty show empty cart
        if(Number(document.querySelector('#total-quantity').innerHTML) == 0){
          document.querySelector('.cart-fill').classList.add('d-none');
          document.querySelector('.empty-cart').classList.remove('d-none');
        }
      }
      else if(quantity > 1){
        url = `${location.protocol}//${location.host}/cart/change-ticket-cart`;
        data = {'quantity': quantity-1, 'ticket-id': ticketId,'cart-id': cartId}
        DecreaseOne(url, data, inputQuantityElem);
        inputQuantityElem.value = quantity - 1;
        ticketUnit.querySelector('.total-price-unit').innerHTML = numberWithCommas(
          parseToNumber(ticketUnit.querySelector('.price-unit').innerHTML) * (quantity - 1)
        )
        calculateTotalPrice();
        calculateTotalQuantity()
      }
    }
    // ? Remove item from cart by click on the trash bin
    if(e.target.closest('.cart-remove')){
      let ticketId = inputQuantityElem.getAttribute('data-ticket-id');
      let cartId = document.querySelector('input[name="cart-id"]').value;
      let url = `${location.protocol}//${location.host}/cart/delete-ticket-cart`;
      let data = {'ticket-id': ticketId, 'cart-id': cartId}
      removeTicket(url, data);
      ticketUnit.remove();
      calculateTotalPrice();
      calculateTotalQuantity();
      // Check if cart is empty show empty cart
      if(Number(document.querySelector('#total-quantity').innerHTML) == 0){
        document.querySelector('.cart-fill').classList.add('d-none');
        document.querySelector('.empty-cart').classList.remove('d-none');
      }
    }
  })
})



const increaseOne = (url, data, inputElem) => {
  sendPostData(url, data)
  .then(data => {
    // console.log(data);
    if(data['status'] != 'ok'){
      // errorMsgElem.innerHTML = data['msg'];
      Swal.fire({
        icon: 'error',
        title: 'خطا در سبد خرید',
        text: data['msg'],
      })
    }
    else{
      // inputElem.value = data['quantity'] + 1;
    }
  })
  .catch(error => {
    // console.log(error);
    Swal.fire({
      icon: 'error',
      title: 'خطا در سبد خرید',
      text: error,
    })
    // errorMsgElem.innerHTML = error
  })
}

const DecreaseOne = (url, data, inputElem) => {
  sendPostData(url, data)
  .then(data => {
    console.log(data);
    if(data['status'] != 'ok'){
      // errorMsgElem.innerHTML = data['msg'];
      Swal.fire({
        icon: 'error',
        title: 'خطا در سبد خرید',
        text: data['msg'],
      })
    }
    else{
      // inputElem.value = data['quantity'] - 1;
    }
  })
  .catch(error => {
    // console.log(error);
    // errorMsgElem.innerHTML = error;
    Swal.fire({
      icon: 'error',
      title: 'خطا در سبد خرید',
      text: error,
    })
  })
}

const removeTicket = (url, data, ticketElem) => {
  sendPostData(url, data)
  .then(data => {
    // console.log(data);
    if(data['status'] != 'ok'){
      // errorMsgElem.innerHTML = data['msg'];
      Swal.fire({
        icon: 'error',
        title: 'خطا در سبد خرید',
        text: data['msg'],
      })
    }
    else{
      // ticketElem.remove();
    }
  })
  .catch(error => {
    // console.log(error);
    // errorMsgElem.innerHTML = error;
    Swal.fire({
      icon: 'error',
      title: 'خطا در سبد خرید',
      text: error,
    })
  })
}