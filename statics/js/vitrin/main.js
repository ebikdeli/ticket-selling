// * When import a module, we should import the script with '.js' extension. JS module rules are weird!
// ! Another weird thing about js modules is that in our app we must import all the other modules we use in our current module even if we don't use every one of imported modules directly
import getCookie from '../csrftoken.js';
import { validateEmail, isNumeric } from '../functions.js';
import { sendPostData } from '../ajax.js';


const cartId = document.querySelector('.cart-id').value


// *** Convert number to a Comma separator string
export function numberWithCommas(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}


// *** Convert back a comma separator string to Number
export function parseToNumber(str) {
    return parseFloat(str.replaceAll(',', ''));
}


// *** Calculate 'total-price'
const calculateTotalPrice = () => {
    // * This function calculate total price of the order and return it. If no product found, return 'null'
    var belitOrderPrices = document.querySelectorAll('.belit-orders-price span:first-of-type');
    var totalPrice = document.querySelector('#total-price');
    var price = 0;
    if (belitOrderPrices == undefined) {
        return null
    }
    Array.from(belitOrderPrices).forEach(belitOrderPrice => {
        price += parseToNumber(belitOrderPrice.innerHTML);
    })
    totalPrice.innerHTML = numberWithCommas(price);
    return price;
}
calculateTotalPrice()



// *** Calculate 'total-quantity'
const calculateTotalQuantity = () => {
    // * This function calculate total quantity of the order and return it
    const headerBelitQuantity = document.querySelector('.header-cart-quantity');
    var orderFillInputs = document.querySelectorAll('.order-fill-input')
    var totalquantity = document.querySelector('#total-belit');
    var quantity = 0;
    Array.from(orderFillInputs).forEach(orderFillInput => {
        quantity += Number(orderFillInput.value)
    })
    totalquantity.innerHTML = quantity;
    headerBelitQuantity.innerHTML = quantity;
    return quantity;
}
calculateTotalQuantity()



function checkHasOrder() {
    // * If no order registered, show empty order message to user
    let orderEmpty = document.querySelector('.order-empty');
    let orderFill = document.querySelector('.order-fill');
    if (calculateTotalQuantity() == 0 && calculateTotalPrice() == 0) {
        orderEmpty.classList.remove('d-none');
        orderFill.classList.add('d-none')
    }
    else {
        orderEmpty.classList.add('d-none');
        orderFill.classList.remove('d-none')
    }
}
checkHasOrder();



// *!*! SHOW EVERY PRICE AS COMMA SEPARATED VALUE
// ? For prize-money
Array.from(document.querySelectorAll('.prize_money-number')).forEach(elem => {
    elem.innerHTML = numberWithCommas(elem.innerHTML);
})
// ? For belit-price
Array.from(document.querySelectorAll('.belit-price')).forEach(elem => {
    elem.innerHTML = numberWithCommas(elem.innerHTML);
})
// ? For belit-order-price
Array.from(document.querySelectorAll('.belit-orders-price')).forEach(elem => {
    elem.innerHTML = numberWithCommas(elem.innerHTML);
})
// ? For total-price
document.querySelector('#total-price').innerHTML = numberWithCommas(document.querySelector('#total-price').innerHTML);



// * Disable every card that is not active
Array.from(document.querySelectorAll('.card-disabled')).forEach(belitCardButton => {
    belitCardButton.querySelector('.belit-card-add-cart-button').disabled = true;
    belitCardButton.querySelector('.belit-card-add-cart-button').innerHTML = 'تمام شد';
})



// *****************************************************************************


// *** Show ticket-card pop up button if user click on the ticket body 'except for click on the 'add-to-cart' button
// *** OR ***
// *** Buy ticket with 'buy ticket button'

const belitCards = document.querySelectorAll('.belit-card');
Array.from(belitCards).forEach(belitCard => {
    belitCard.addEventListener('click', e => {
        e.preventDefault();
        // *** Show belit-card popup for each ticket user click on
        if (e.target.closest('.belit-card-top')) {
            // ! Must wait just a little to not interrupted with "removeBelitPopUp" function and show belit popup without closing it immediatly! 
            window.setTimeout(() => {
                // console.log('Display popup!');
                // ! GET NEED DATA FROM THE BELIT-CARD JUST CLICKED ON
                let src = belitCard.querySelector('img').src;
                let name = belitCard.querySelector('.belit-name').innerHTML;
                let rewardValue = belitCard.querySelector('.prize_money-number').innerHTML;
                // let rewardQuantity = belitCard.querySelector('.belit-reward-quantity').innerHTML;
                // let systemNumber = belitCard.getAttribute('system-ticket-number');
                // let gameNumber = belitCard.getAttribute('game-ticket-number');
                let belitUnitPrice = belitCard.querySelector('.belit-price-number').innerHTML;
                let belitContent = belitCard.querySelector('.ticket-content').innerHTML;
                let belitDate = belitCard.querySelector('.ticket-date').innerHTML;
                // <div class="belit-card-popup-template">
                const newPopUpText = `<div class="belit-card-popup">
            <i class="bi bi-x-lg belit-card-popup-close-button"></i>
            <p class="belit-card-popup-name">مشخصات محصول</p>
            <img src="${src}" class="mx-auto" alt="${name}">
            <div class="belit-card-popup-anounce">
                <h3>اعلام قرعه کشی</h3>
                
                <p>
                <span>جایزه:</span>
                <span class="me-1" style="font-weight: 600;">${name}</span>
                </p>
                <p>
                <span>مبلغ جایزه:</span>
                <span class="mx-1" style="color: #f27a1a; font-weight: 600; letter-spacing: 1px;">${rewardValue}</span>
                <span>تومان</span>
                </p>
                <p>
                <span>قیمت بلیط:</span>
                <span class="mx-1" style="color: #f27a1a; font-weight: 600; letter-spacing: 1px;">${belitUnitPrice}</span>
                <span>تومان</span>
                </p>
                <p>
                <span>زمان قرعه کشی</span>
                <span class="me-1" style="font-weight: 600;">${belitDate}</span>
                </p>
                <p>
                <span>توضیحات:</span>
                <span class="me-1">${belitContent}</span>
                </p>
            </div>
            </div>`;
        // </div>
        const newPopUpElem = document.createElement('div');
        // popUpElem.classList.add('belit-card-popup-template');
        newPopUpElem.classList.add('belit-card-popup-template');
        newPopUpElem.innerHTML = newPopUpText;
        const parent = document.querySelector('.bc-popup');
        parent.appendChild(newPopUpElem);
        }, 10)
    }

        // *** Add ticket to the cart
        if (e.target.classList.contains('belit-card-add-cart-button')) {
            let belit_id = e.target.getAttribute('data-belit-id');
            let belit_quantity = '1';
            // Send data to server
            // // let url = `${location.protocol}://${location.hostname}/cart/add-ticket-cart`;
            let url = `${location.protocol}//${location.host}/cart/add-ticket-cart`;
            let errormsg = 'ارتباط با سرور برقرار نشد';
            let data = {'cart-id': cartId, 'ticket-id': belit_id, 'quantity': belit_quantity}
            // ! Important: To not let user wait for server data, we always assume ajax request is successful so user can continue their experience. But if any happend, server send the error message with a little delay!
            sendPostData(url, data, errormsg)
            .then(data => {
                // console.log(data);
                if(data['status'] != 'ok'){
                    Swal.fire({
                        icon: 'error',
                        title: 'مشکلی پیش آمده',
                        text: data['msg'],
                        confirmButtonText: 'بله'
                    })
                }
            })
            .catch(err => {
                // console.log(err);
                Swal.fire({
                    icon: 'error',
                    title: 'خطا',
                    text: err,
                    confirmButtonText: 'بله'
                })
            })
            // ! Add current belit to the orders. First check if 'order-fill' has 'd-none' class
            const orderEmpty = document.querySelector('.order-empty');
            const orderFill = document.querySelector('.order-fill');
            const belitOrdersBox = document.querySelector('.belit-orders-box');
            if (orderFill.classList.contains('d-none')) {
                orderEmpty.classList.remove('d-none');
                orderFill.classList.add('d-none');
            }
            const belitName = belitCard.querySelector('.belit-name').innerHTML;
            const belitPrice = belitCard.querySelector('.belit-price > span').innerHTML;
            const newOrderElement = document.createElement('div');
            ['belit-orders', 'd-flex', 'justify-content-center', 'align-items-center'].forEach((cl => {
                newOrderElement.classList.add(cl)
            }))
            const newOrderText = `<p class="belit-orders-name">${belitName}</p>
            <p class="belit-orders-price">
            <span>${belitPrice}</span>&nbsp;<span style="font-size: 12px;">تومان</span>
            </p>
            <div class="d-flex justify-content-center align-items-center">
            <button class="order-fill-button belit-card-dec order-fill-button-dec btn"><i class="fas fa-minus order-fill-button-dec"></i></button>
            <input type="number" data-belit-id="${belit_id}" data-ticketsold-id="" value="1" min="1" max="150" maxlength="3" class="order-fill-input belit-quantity-input">
            <button class="order-fill-button belit-card-inc order-fill-button-inc btn"><i class="fas fa-plus order-fill-button-inc"></i></button>
            </div>`
            newOrderElement.innerHTML = newOrderText;
            belitOrdersBox.appendChild(newOrderElement);
            calculateTotalPrice();
            calculateTotalQuantity();
            checkHasOrder()
            e.target.style.animation = 'fade-out ease-in-out .2s';
            setTimeout(() => { e.target.classList.add('d-none') }, 200)
            var belitIncDec = e.target.nextElementSibling;
            setTimeout(() => belitIncDec.classList.remove('d-none'), 200)
            // To be able repeat this process smooth, we need to remove animation from current style
            setTimeout(() => {
                e.target.style.animation = null
            }, 50)
        }
    })
})



// ??????????????????????????????? INCREASE QUANTITY FUNCTIONS ???????????????

// *** 'Increase' ticket quantity with 'inc button' in Belit Card section
const IncBelitCard = (buttonElem) => {
    let inputElem = buttonElem.previousElementSibling;
    let belitQuantity = Number(inputElem.value)
    let belitId = inputElem.getAttribute('data-belit-id');
    let belit = buttonElem.parentElement.parentElement.parentElement;
    let belitPrice = parseToNumber(belit.querySelector('.belit-price span:first-of-type').innerHTML);
    // console.log(inputElem, belitQuantity, belitId, belit, belitPrice);
    // No we can process further things on the data
    if (belitQuantity == 150) {
        console.log('Belit quantity exceeded from 150 unit');
        return null;
    }
    // Make ajax call to increase ticket by one
    let url = `${location.protocol}//${location.host}/cart/change-ticket-cart`;
    let errormsg = 'ارتباط با سرور برقرار نشد';
    let data = {'cart-id': cartId, 'ticket-id': belitId, 'quantity': belitQuantity+1}
    // ! Important: To not let user wait for server data, we always assume ajax request is successful so user can continue their experience. But if any happend, server send the error message with a little delay!
    sendPostData(url, data, errormsg)
    .then(data => {
        // console.log(data);
        if(data['status'] != 'ok'){
            Swal.fire({
                icon: 'error',
                title: 'مشکلی پیش آمده',
                text: data['msg'],
                confirmButtonText: 'بله'
            })
        }
    })
    .catch(err => {
        // console.log(err);
        Swal.fire({
            icon: 'error',
            title: 'خطا',
            text: err,
            confirmButtonText: 'بله'
        })
    })

    // After successfully increased belit quantity, update the front with 'belit-input' and 'orderfill'
    let belitOrders = document.querySelectorAll('.belit-orders');
    Array.from(belitOrders).forEach(belitOrder => {
        // console.log(belitOrder.querySelector('.belit-quantity-input').getAttribute('data-belit-id'), belitId);
        if (belitOrder.querySelector('.belit-quantity-input').getAttribute('data-belit-id') == belitId) {
            inputElem.value = String(belitQuantity + 1);
            belitOrder.querySelector('.belit-quantity-input').value = String(belitQuantity + 1);
            belitOrder.querySelector('.belit-orders-price span:first-of-type').innerHTML = numberWithCommas(belitPrice * (belitQuantity + 1));
            calculateTotalQuantity();
            calculateTotalPrice();
        }
    })
}
// CALL THE 'IncBelitCard' or 'DecBelitCard' or 'ChangeBelitCardQuantity' functions
let belitIncDecs = document.querySelectorAll('.belit-card-add-cart-inc-dec');
Array.from(belitIncDecs).forEach(belitIncDec => {
    // increase or decrease belit quantity using buttons
    belitIncDec.addEventListener('click', e => {
        // 
        // "Increase" belit quantity
        if (e.target.classList.contains('belit-card-inc-button')) {
            // console.log("SUCCESS");
            IncBelitCard(belitIncDec.querySelector('.belit-card-inc'))
        }
        // "Decrease" belit quantity
        else if (e.target.classList.contains('belit-card-dec-button')) {
            DecBelitCard(belitIncDec.querySelector('.belit-card-dec'));
        }
    })
    // change belit quantity directly using 'input'
    belitIncDec.querySelector('.belit-quantity-input').addEventListener('keyup', e => {
        ChangeBelitCardQuantity(belitIncDec.querySelector('.belit-quantity-input'));
    })
})



// *** 'Increase' ticket quantity with 'belit-card-inc button' in Order section
const IncOrderBelit = (buttonElem) => {
    let inputElem = buttonElem.previousElementSibling;
    let belitQuantity = Number(inputElem.value)
    let belitId = inputElem.getAttribute('data-belit-id');
    let belit = buttonElem.parentElement.parentElement;
    let belitPriceElem = belit.querySelector('.belit-orders-price span:first-of-type');
    let belitUnitPrice = parseToNumber(belitPriceElem.innerHTML) / belitQuantity;
    // console.log(inputElem, belitQuantity, belitId, belit, belitUnitPrice);
    // No we can process further things on the data
    if (belitQuantity == 150) {
        console.log('Belit quantity exceeded from 150 unit');
        return null;
    }
    // Make ajax call to increase ticket by one
    // // let url = `${location.protocol}://${location.hostname}/cart/change-ticket-cart`;
    let url = `${location.protocol}//${location.host}/cart/change-ticket-cart`;
    let errormsg = 'ارتباط با سرور برقرار نشد';
    let data = {'cart-id': cartId, 'ticket-id': belitId, 'quantity': belitQuantity+1}
    // ! Important: To not let user wait for server data, we always assume ajax request is successful so user can continue their experience. But if any happend, server send the error message with a little delay!
    sendPostData(url, data, errormsg)
    .then(data => {
        // console.log(data);
        if(data['status'] != 'ok'){
            Swal.fire({
                icon: 'error',
                title: 'مشکلی پیش آمده',
                text: data['msg'],
                confirmButtonText: 'بله'
            })
        }
    })
    .catch(err => {
        // console.log(err);
        Swal.fire({
            icon: 'error',
            title: 'خطا',
            text: err,
            confirmButtonText: 'بله'
        })
    })

    // After successfully increased belit quantity, update the front with 'belit-input' and 'orderfill'
    let belitCards = document.querySelectorAll('.belit-card');
    Array.from(belitCards).forEach(belitCard => {
        // console.log(belitCard.querySelector('.belit-quantity-input').getAttribute('data-belit-id'), belitId);
        if (belitCard.querySelector('.belit-quantity-input').getAttribute('data-belit-id') == belitId) {
            inputElem.value = String(belitQuantity + 1);
            belitPriceElem.innerHTML = numberWithCommas(belitUnitPrice * (belitQuantity + 1));
            belitCard.querySelector('.belit-quantity-input').value = String(belitQuantity + 1);
            calculateTotalQuantity();
            calculateTotalPrice();
        }
    })
}
// CALL THE 'IncOrderBelit' or 'DecOrderBelit' function
let belitOrderBox = document.querySelector('.belit-orders-box');
belitOrderBox.addEventListener('click', e => {
    // Call 'IncOrderBelit' to increase belit quantity
    if (e.target.classList.contains('order-fill-button-inc')) {
        if (e.target.tagName == 'BUTTON') {
            var incButt = e.target
        }
        else if (e.target.tagName == 'I') {
            var incButt = e.target.parentElement
        }
        IncOrderBelit(incButt)
    }
    // call 'DecOrderBelit' to decrease belit quantity
    else if (e.target.classList.contains('order-fill-button-dec')) {
        if (e.target.tagName == 'BUTTON') {
            var incButt = e.target
        }
        else if (e.target.tagName == 'I') {
            var incButt = e.target.parentElement
        }
        DecOrderBelit(incButt);
    }
})
// Call the 'ChangeOrderBelitQuantity' to change ticket quantity from OrderBelit input directly
belitOrderBox.addEventListener('keyup', e => {
    if (e.target.tagName == 'INPUT') {
        ChangeOrderBelitQuantity(e.target);
    }
})




// ??????????????????????????????? DECREASE QUANTITY FUNCTIONS ???????????????

// ** 'Decrease' ticket quantity with 'dec button' in Belit Card section
const DecBelitCard = (buttonElem) => {
    let inputElem = buttonElem.nextElementSibling;
    let belitQuantity = Number(inputElem.value)
    let belitId = inputElem.getAttribute('data-belit-id');
    let belit = buttonElem.parentElement.parentElement.parentElement;
    let belitPrice = parseToNumber(belit.querySelector('.belit-price span:first-of-type').innerHTML);
    // console.log(inputElem, belitQuantity, belitId, belit, belitPrice);
    // No we can process further things on the data
    // Make ajax call to decrease ticket by one. If quantity == 1, call 'delete-ticket-cart' in ajax call
    let url = '';
    let errormsg = 'ارتباط با سرور برقرار نشد';
    let data = {};
    if(belitQuantity-1 > 0){
        url = `${location.protocol}//${location.host}/cart/change-ticket-cart`;
        data = {'cart-id': cartId, 'ticket-id': belitId, 'quantity': belitQuantity-1}
    }
    else{
        url = `${location.protocol}//${location.host}/cart/delete-ticket-cart`;
        data = {'cart-id': cartId, 'ticket-id': belitId}
    }
    // ! Important: To not let user wait for server data, we always assume ajax request is successful so user can continue their experience. But if any happend, server send the error message with a little delay!
            sendPostData(url, data, errormsg)
            .then(data => {
                // console.log(data);
                if(data['status'] != 'ok'){
                    Swal.fire({
                        icon: 'error',
                        title: 'مشکلی پیش آمده',
                        text: data['msg'],
                        confirmButtonText: 'بله'
                    })
                }
            })
            .catch(err => {
                // console.log(err);
                Swal.fire({
                    icon: 'error',
                    title: 'خطا',
                    text: err,
                    confirmButtonText: 'بله'
                })
            })

    // After successfully decrease-delete belit quantity, update the front with 'belit-input' and 'orderfill'
    let belitOrders = document.querySelectorAll('.belit-orders');
    Array.from(belitOrders).forEach(belitOrder => {
        // console.log(belitOrder.querySelector('.belit-quantity-input').getAttribute('data-belit-id'), belitId);
        if (belitOrder.querySelector('.belit-quantity-input').getAttribute('data-belit-id') == belitId) {
            // If new quantity is zero, delete the belit from the Order, and bring back 'buy-button' in Belit-Card section
            if (belitQuantity - 1 > 0) {
                inputElem.value = String(belitQuantity - 1);
                belitOrder.querySelector('.belit-quantity-input').value = String(belitQuantity - 1);
                belitOrder.querySelector('.belit-orders-price span:first-of-type').innerHTML = numberWithCommas(belitPrice * (belitQuantity - 1));
            }
            else {
                let belitInputIncDec = buttonElem.parentElement;
                belitInputIncDec.animation = 'fade-out ease-in-out .2s';
                belitOrder.remove();
                setTimeout(() => { belitInputIncDec.classList.add('d-none') }, 200)
                var belitAddButton = belitInputIncDec.previousElementSibling;
                setTimeout(() => belitAddButton.classList.remove('d-none'), 200)
                // To be able repeat this process smooth, we need to remove animation from current style
                setTimeout(() => {
                    belitInputIncDec.style.animation = null
                }, 50)
                // belit.querySelector('.belit-card-add-cart-button').classList.remove()
            }
            calculateTotalQuantity();
            calculateTotalPrice();
            checkHasOrder();
        }
    })
}


// *** 'Decrease' ticket quantity with 'belit-card-dec button' in Order section
const DecOrderBelit = (buttonElem) => {
    let inputElem = buttonElem.nextElementSibling;
    let belitQuantity = Number(inputElem.value)
    let belitId = inputElem.getAttribute('data-belit-id');
    let belitOrder = buttonElem.parentElement.parentElement;
    let belitPriceElem = belitOrder.querySelector('.belit-orders-price span:first-of-type');
    let belitUnitPrice = parseToNumber(belitPriceElem.innerHTML) / belitQuantity;
    // No we can process further things on the data
    if (belitQuantity == 150) {
        console.log('Belit quantity exceeded from 150 unit');
        return null;
    }
    // Make ajax call to decrease ticket by one. If quantity == 1, call 'delete-ticket-cart' in ajax call
    let url = '';
    let errormsg = 'ارتباط با سرور برقرار نشد';
    let data = {};
    if(belitQuantity-1 > 0){
        url = `${location.protocol}//${location.host}/cart/change-ticket-cart`;
        data = {'cart-id': cartId, 'ticket-id': belitId, 'quantity': belitQuantity-1}
    }
    else{
        url = `${location.protocol}//${location.host}/cart/delete-ticket-cart`;
        data = {'cart-id': cartId, 'ticket-id': belitId}
    }
    // ! Important: To not let user wait for server data, we always assume ajax request is successful so user can continue their experience. But if any happend, server send the error message with a little delay!
    sendPostData(url, data, errormsg)
    .then(data => {
        // console.log(data);
        if(data['status'] != 'ok'){
            Swal.fire({
                icon: 'error',
                title: 'مشکلی پیش آمده',
                text: data['msg'],
                confirmButtonText: 'بله'
            })
        }
    })
    .catch(err => {
        // console.log(err);
        Swal.fire({
            icon: 'error',
            title: 'خطا',
            text: err,
            confirmButtonText: 'بله'
        })
    })

    // After successfully decrease-delete belit quantity, update the front with 'belit-input' and 'orderfill'
    let belitCards = document.querySelectorAll('.belit-card');
    Array.from(belitCards).forEach(belitCard => {
        if (belitCard.querySelector('.belit-quantity-input').getAttribute('data-belit-id') == belitId) {
            // If new quantity is zero, delete the belit from the Order, and bring back 'buy-button' in Belit-Card section
            if (belitQuantity - 1 > 0) {
                // Change values for Order section
                inputElem.value = String(belitQuantity - 1);
                belitPriceElem.innerHTML = numberWithCommas(belitUnitPrice * (belitQuantity - 1));
                belitCard.querySelector('.belit-quantity-input').value = belitQuantity - 1;
            }
            else {
                let belitCardIncDec = belitCard.querySelector('.belit-card-add-cart-inc-dec');
                belitCardIncDec.animation = 'fade-out ease-in-out .2s';
                belitOrder.remove();
                setTimeout(() => { belitCardIncDec.classList.add('d-none') }, 200)
                var belitAddButton = belitCardIncDec.previousElementSibling;
                setTimeout(() => belitAddButton.classList.remove('d-none'), 200)
                // To be able repeat this process smooth, we need to remove animation from current style
                setTimeout(() => {
                    belitCardIncDec.style.animation = null
                }, 50)
            }
            calculateTotalQuantity();
            calculateTotalPrice();
            checkHasOrder();
        }
    })
}




// ******************************* Change belit quantity using input field directly **********

// *** Change ticket quantity using 'Belit Card input'
const ChangeBelitCardQuantity = (inputElem) => {
    const belitId = inputElem.getAttribute('data-belit-id');
    let newQuantity = Number(inputElem.value);
    const belitCardElem = inputElem.parentElement.parentElement.parentElement;
    const belitUnitPrice = parseToNumber(belitCardElem.querySelector('.belit-price span:first-of-type').innerHTML);
    if (newQuantity > 150) {
        // console.log('quantity cannot be greater than 150');
        newQuantity = 150;
    }
    // Now we can process further things on the data
    // Make ajax call to change ticket quantity. If newQuantity == 0, call 'delete-ticket-cart' in ajax call
    let url = '';
    let errormsg = 'ارتباط با سرور برقرار نشد';
    let data = {};
    if(newQuantity > 0){
        url = `${location.protocol}//${location.host}/cart/change-ticket-cart`;
        data = {'cart-id': cartId, 'ticket-id': belitId, 'quantity': newQuantity}
    }
    else{
        url = `${location.protocol}//${location.host}/cart/delete-ticket-cart`;
        data = {'cart-id': cartId, 'ticket-id': belitId}
    }
    // ! Important: To not let user wait for server data, we always assume ajax request is successful so user can continue their experience. But if any happend, server send the error message with a little delay!
    sendPostData(url, data, errormsg)
    .then(data => {
        // console.log(data);
        if(data['status'] != 'ok'){
            Swal.fire({
                icon: 'error',
                title: 'مشکلی پیش آمده',
                text: data['msg'],
                confirmButtonText: 'بله'
            })
        }
    })
    .catch(err => {
        // console.log(err);
        Swal.fire({
            icon: 'error',
            title: 'خطا',
            text: err,
            confirmButtonText: 'بله'
        })
    })

    // Update OrderBelit with new data
    let belitOrderBox = document.querySelector('.belit-orders-box');
    Array.from(belitOrderBox.children).forEach(belitOrder => {
        if (belitOrder.querySelector('.order-fill-input').getAttribute('data-belit-id') == belitId) {
            if (newQuantity > 0) {
                inputElem.value = newQuantity;
                belitOrder.querySelector('.order-fill-input').value = newQuantity;
                belitOrder.querySelector('.belit-orders-price span:first-of-type').innerHTML = numberWithCommas(belitUnitPrice * newQuantity)
            }
            else {
                inputElem.value = 1;
                let belitCardIncDec = belitCardElem.querySelector('.belit-card-add-cart-inc-dec');
                belitCardIncDec.animation = 'fade-out ease-in-out .2s';
                belitOrder.remove();
                setTimeout(() => { belitCardIncDec.classList.add('d-none') }, 200)
                var belitAddButton = belitCardIncDec.previousElementSibling;
                setTimeout(() => belitAddButton.classList.remove('d-none'), 200)
                // To be able repeat this process smooth, we need to remove animation from current style
                setTimeout(() => {
                    belitCardIncDec.style.animation = null
                }, 50)
            }
        }
    })
    calculateTotalQuantity();
    calculateTotalPrice();
    checkHasOrder();
}


// *** Change ticket quantity using 'Order Belit input'
const ChangeOrderBelitQuantity = (inputElem) => {
    const belitId = inputElem.getAttribute('data-belit-id');
    let newQuantity = Number(inputElem.value);
    let belitOrder = inputElem.parentElement.parentElement;
    // const belitUnitPrice = parseToNumber(belitCardElem.querySelector('.belit-price span:first-of-type').innerHTML);
    if (newQuantity > 150) {
        // console.log('quantity cannot be greater than 150');
        newQuantity = 150;
    }
    // Now we can process further things on the data
    // Make ajax call to change ticket quantity. If newQuantity == 0, call 'delete-ticket-cart' in ajax call
    let url = '';
    let errormsg = 'ارتباط با سرور برقرار نشد';
    let data = {};
    if(newQuantity > 0){
        url = `${location.protocol}//${location.host}/cart/change-ticket-cart`;
        data = {'cart-id': cartId, 'ticket-id': belitId, 'quantity': newQuantity}
    }
    else{
        url = `${location.protocol}//${location.host}/cart/delete-ticket-cart`;
        data = {'cart-id': cartId, 'ticket-id': belitId}
    }
    // ! Important: To not let user wait for server data, we always assume ajax request is successful so user can continue their experience. But if any happend, server send the error message with a little delay!
    sendPostData(url, data, errormsg)
    .then(data => {
        // console.log(data);
        if(data['status'] != 'ok'){
            Swal.fire({
                icon: 'error',
                title: 'مشکلی پیش آمده',
                text: data['msg'],
                confirmButtonText: 'بله'
            })
        }
    })
    .catch(err => {
        // console.log(err);
        Swal.fire({
            icon: 'error',
            title: 'خطا',
            text: err,
            confirmButtonText: 'بله'
        })
    })
    
    // After successfully change belit quantity, update the front with 'belit-input' and 'orderfill'
    let belitCards = document.querySelectorAll('.belit-card');
    Array.from(belitCards).forEach(belitCard => {
        if (belitCard.querySelector('.belit-quantity-input').getAttribute('data-belit-id') == belitId) {
            // If new quantity is zero, delete the belit from the Order, and bring back 'buy-button' in Belit-Card section
            if (newQuantity > 0) {
                // Change values for Order section and BelitCard
                inputElem.value = newQuantity;
                let belitUnitPrice = parseToNumber(belitCard.querySelector('.belit-price span:first-of-type').innerHTML)
                belitOrder.querySelector('.belit-orders-price span:first-of-type').innerHTML = numberWithCommas(belitUnitPrice * newQuantity);
                belitCard.querySelector('.belit-quantity-input').value = newQuantity;
            }
            else {
                let belitCardIncDec = belitCard.querySelector('.belit-card-add-cart-inc-dec');
                belitCardIncDec.animation = 'fade-out ease-in-out .2s';
                belitOrder.remove();
                setTimeout(() => { belitCardIncDec.classList.add('d-none') }, 200)
                var belitAddButton = belitCardIncDec.previousElementSibling;
                setTimeout(() => belitAddButton.classList.remove('d-none'), 200)
                // To be able repeat this process smooth, we need to remove animation from current style
                setTimeout(() => {
                    belitCardIncDec.style.animation = null
                }, 50)
            }
            calculateTotalQuantity();
            calculateTotalPrice();
            checkHasOrder();
        }
    })
}



// *** Belit Order Button click redirection (INSTEAD OF DISABLED POP UP SECTION)
const belitOrderButton = document.querySelector('.belit-order-payment-button');
belitOrderButton.addEventListener('click', e=>{
    let orderUrl = `${location.protocol}//${location.host}/order.html`;
    if(location.pathname.includes('front-ticket-selling')){
        orderUrl = `${location.protocol}//${location.host}/front-ticket-selling/order.html`;
    }
    window.open(orderUrl);
})



// *** Authentication Pop up interaction (TEMPORARY DISABLED)
// const belitOrderButton = document.querySelector('.belit-order-payment-button');
// const popupSection = document.querySelector('.popup-section');
// const closeButton = document.querySelector('.close');
// // Show popup when click on order button
// belitOrderButton.addEventListener('click', e => {
//     setTimeout(() => {
//         popupSection.classList.toggle('d-none');
//     }, 160)
// })
// // Close popup when click on 'close' button
// closeButton.addEventListener('click', e => {
//     popupSection.classList.add('d-none');
// })
// // Close popup when click on 'Escape' key on the keyboard
// document.addEventListener('keyup', e => {
//     if (e.key == 'Escape' && !popupSection.classList.contains('d-none')) {
//         popupSection.classList.add('d-none');
//     }
// })
// // Close popup when click outside the popup cadre
// document.addEventListener("click", (e) => {
//     // Check if the filter list parent element exist
//     const isClosest = e.target.closest('#popup-cadre');
//     // If `isClosest` equals falsy & popup has the class `show`
//     // then hide the popup
//     if (!isClosest && (!popupSection.classList.contains("d-none"))) {
//         popupSection.classList.add("d-none");
//     }
// });




// *** Identity Form validation and ajax send (TEMPORARY DISABLED)
// const identityForm = document.querySelector('form[name="identity-check-form"]');
// identityForm.addEventListener('submit', function (e) {
//     e.preventDefault();
//     // Get form field data with default border color
//     let firstNameElem = document.querySelector('input[name="first-name"]');
//     firstNameElem.parentElement.style.borderColor = '#e6e6e6';
//     let surNameElem = document.querySelector('input[name="last-name"]');
//     surNameElem.parentElement.style.borderColor = '#e6e6e6';
//     let birthDateElem = document.querySelector('input[name="birth-date"]');
//     birthDateElem.parentElement.parentElement.style.borderColor = '#e6e6e6';
//     let identifierElem = document.querySelector('input[name="identifier"]');
//     identifierElem.parentElement.style.borderColor = '#e6e6e6';
//     let agreeElem = document.querySelector('input[name="agree"]');
//     agreeElem.style.borderColor = '#999999';
//     if (agreeElem.checked) {
//         agreeElem.style.borderColor = '#f27a1a';
//     }
//     // Error box
//     let errorBox = document.querySelector('#error-box-wrapper');
//     let erroMsg = document.querySelector('.message');
//     errorBox.classList.add('d-none');
//     erroMsg.innerHTML = '';
//     let errors = 0;
//     // Process form data
//     if (firstNameElem.value.length == 0) {
//         firstNameElem.parentElement.style.borderColor = '#d21313';
//         errorBox.classList.remove('d-none');
//         erroMsg.innerHTML = 'نام کوچک خود را وارد کنید';
//         errors += 1;
//         return false;
//     }
//     else if (surNameElem.value.length == 0) {
//         surNameElem.parentElement.style.borderColor = '#d21313';
//         errorBox.classList.remove('d-none');
//         erroMsg.innerHTML = 'نام خانوادگی خود را وارد';
//         errors += 1;
//         return false;
//     }
//     else if (birthDateElem.value.length == 0) {
//         birthDateElem.parentElement.parentElement.style.borderColor = '#d21313';
//         errorBox.classList.remove('d-none');
//         erroMsg.innerHTML = 'تاریخ تولد خود را وارد کنید';
//         errors += 1;
//         return false;
//     }
//     else if (identifierElem.value.length == 0) {
//         identifierElem.parentElement.style.borderColor = '#d21313';
//         errorBox.classList.remove('d-none');
//         erroMsg.innerHTML = 'شماره ملی خود را وارد کنید';
//         errors += 1;
//         return false;
//     }
//     else if (identifierElem.value.length !== 10 || (identifierElem.value.length === 10 && !isNumeric(identifierElem.value))) {
//         identifierElem.parentElement.style.borderColor = '#d21313';
//         errorBox.classList.remove('d-none');
//         erroMsg.innerHTML = 'شماره ملی خود را به درستی وارد کنید';
//         errors += 1;
//         return false;
//     }
//     else if (!agreeElem.checked) {
//         agreeElem.style.borderColor = '#d21313';
//         errorBox.classList.remove('d-none');
//         erroMsg.innerHTML = 'با قوانین موافقت نکرده اید';
//         errors += 1;
//         return false;
//     }
//     // If no error proceed to send data in AJAX request
//     if (errors == 0) {
//         // let url = `${location.protocol}://${location.hostname}/login/...`;
//         let url = `${location.protocol}/login/...`;
//         let data = {
//             'first-name': firstNameElem.value,
//             'last-name': surNameElem.value,
//             'birth-date': birthDateElem.value,
//             'identifier': identifierElem.value
//         }
//         // sendPostData(url, data)
//         // .then(data => {
//         //     console.log(data);
//         // })
//         // .catch(error => {
//         //     console.log(error);
//         // })
//         console.log(url);
//         console.log(data);
//     }
// })




// *********** Close BelitCardPopUp ************

function removeBelitPopUp(){
    // If popup is displayed try to close it by click on close button or click on outside of popup box
    document.addEventListener('click', e => {
        // console.log('removeBelitPopUp');
        const belitPopUp = document.querySelector('.belit-card-popup-template');
        if (belitPopUp != null) {
            // Close by close button
            if (e.target.closest('.belit-card-popup-close-button')) {
                belitPopUp.remove();
            }
            // Close by clicking outside the Popup box
            if (!e.target.closest('.belit-card-popup')) {
                belitPopUp.remove();
            }
        }
    })
    // If popup is displayed try to close it by press 'escape' key
    document.addEventListener('keyup', e => {
        const belitPopUp = document.querySelector('.belit-card-popup-template');
        if (belitPopUp != null && e.key == 'Escape') {
            belitPopUp.remove();
        }
    })
}
removeBelitPopUp();