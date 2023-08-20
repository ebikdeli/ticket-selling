import { validate_phone_number, validateEmail, isNumeric } from '../functions.js';
import {sendPostData} from '../ajax.js';



const cartId = document.querySelector('.cart-id').value


// *** Convert number to a Comma separator string
export function numberWithCommas(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

// *** Convert back a comma separator string to Number
export function parseToNumber(str) {
    return parseFloat(str.replaceAll(',', ''));
}



// *** Redirect with buttons to 'orders' and 'cart' url
document.querySelector('#my-orders').addEventListener('click', e => {
    // Must get changed for backend purpose
    let orderUrl = `${location.protocol}//${location.host}/order.html`;
    // To support page load on github
    if(location.pathname.includes('front-ticket-selling')){
        orderUrl = `${location.protocol}//${location.host}/front-ticket-selling/order.html`;
    }
    window.open(orderUrl);
})
document.querySelector('#my-cart').addEventListener('click', e => {
    // Must get changed for backend purpose
    let cartUrl = `${location.protocol}//${location.host}/cart.html`;
    // To support page load on github
    if(location.pathname.includes('front-ticket-selling')){
        cartUrl = `${location.protocol}//${location.host}/front-ticket-selling/cart.html`;
    }
    window.open(cartUrl);
})



// ! Error box elements
const errorBox = document.querySelector('#error-box-wrapper');
const errorMsg = document.querySelector('.message');




// *********** Change content using icons *****************
// If the icon clicked on is not active, deactive the currently active icon and hide its content div and in the end active clicked icon and show its content div
// let editProfileIcon = document.querySelector('.person');
let editProfileBox = document.querySelector('.profile-change-box');
// let changePasswordIcon = document.querySelector('.key');
let changePasswordBox = document.querySelector('.password-change-box');
const icons = document.querySelectorAll('.icons > i');
Array.from(icons).forEach(icon => {
    icon.addEventListener('click', e => {
        let currentActiveIcon = document.querySelector('.icons .active');
        if(!e.target.classList.contains('active')){
            // If error box is shown, hide them
            errorBox.classList.add('d-none');
            errorMsg.innerHTML = '';
            // Deactive current active icon and hide its contents
            currentActiveIcon.classList.remove('active');
            if (currentActiveIcon.classList.contains('person')){
                editProfileBox.classList.add('d-none');
            }
            else if(currentActiveIcon.classList.contains('key')){
                changePasswordBox.classList.add('d-none');
            }
            // Active clicked icon and show its content
            e.target.classList.add('active');
            if (e.target.classList.contains('person')){
                editProfileBox.classList.remove('d-none');
            }
            else if(e.target.classList.contains('key')){
                changePasswordBox.classList.remove('d-none');
            }
        }
    })
})




// *** FORMS IN THE PAGE ***
const editProfileForm = document.querySelector('#profile-edit-form');
const changePasswordForm = document.querySelector('#password-change-form');



// **************** Profile edit form (Only send request if there is a change in the form data)
let editProfileFormSubmitBtn = document.querySelector('#profile-edit-button');
// ? ProfileForm initial data
let firstNameElem = document.querySelector('input[name="first-name"]');
let lastNameElem = document.querySelector('input[name="last-name"]');
let emailElem = document.querySelector('input[name="email"]');
let phoneElem = document.querySelector('input[name="phone"]');
let addressElem = document.querySelector('textarea[name="address"]');

let initialFirstName = firstNameElem.value;
let initialLastName = lastNameElem.value;
let initialEmail = emailElem.value;
let initialPhone = phoneElem.value;
let initialAddress = addressElem.value;
let editFormInitials = [initialFirstName, initialLastName, initialEmail, initialPhone, initialAddress]

// * enable/disable submit button only if any input in the form has changed
editProfileForm.addEventListener('keyup', e=>{
    // Based number of changed input tags, we can know if any form field changed from it initial value to enable or disable submit button
    let inputsChanged = editProfileForm.querySelectorAll('.form-control').length;
    Array.from(editProfileForm.querySelectorAll('.form-control')).forEach(inputElem => {
        // If submit button is already disabled look if it must be enabled
        if(editProfileFormSubmitBtn.disabled){
            if(!editFormInitials.includes(inputElem.value)){
                editProfileFormSubmitBtn.disabled = false;
            }
        }
        // If submit button is already enabled look if it must be disabled PART(1)
        if(!editProfileFormSubmitBtn.disabled){
            if(editFormInitials.includes(inputElem.value)){
                inputsChanged -= 1;
            }
        }
    })
    // If submit button is already enabled look if it must be disabled PART(2)
    if(!inputsChanged){
        editProfileFormSubmitBtn.disabled = true;
    }
})

// * validate and submit edit profile form
editProfileForm.addEventListener('submit', e =>{
    e.preventDefault();
    errorBox.classList.add('d-none');
    errorMsg.innerHTML = '';
    // edit profile form validation
    let firstName = firstNameElem.value;
    firstNameElem.style.borderColor = '#dee2e6';
    let LastName = lastNameElem.value;
    lastNameElem.style.borderColor = '#dee2e6';
    let Email = emailElem.value;
    emailElem.style.borderColor = '#dee2e6';
    let Phone = phoneElem.value;
    phoneElem.style.borderColor = '#dee2e6';
    let Address = addressElem.value;
    addressElem.style.borderColor = '#dee2e6';
    let errors = 0;
    // Only change profile
    if(!editProfileFormSubmitBtn.disabled){
        if(firstName.length == 0){
            errorBox.classList.remove('d-none');
            errorMsg.innerHTML += '<span>فیلد نام نمی تواند خالی باشد</span>'
            firstNameElem.style.borderColor = 'red';
            errors += 1;
        }
        if(LastName.length == 0){
            errorBox.classList.remove('d-none');
            errorMsg.innerHTML += '<span>فیلد نام خانوادگی نمی تواند خالی باشد</span>'
            lastNameElem.style.borderColor = 'red';
            errors += 1;
        }
        if(Email.length == 0){
            errorBox.classList.remove('d-none');
            errorMsg.innerHTML += '<span>ایمیل خود را وارد کنید</span>'
            emailElem.style.borderColor = 'red';
            errors += 1;
        }
        else if(Email.length > 0 && !validateEmail(Email)){
            errorBox.classList.remove('d-none');
            errorMsg.innerHTML += '<span>ایمیل خود را به درستی وارد کنید</span>'
            emailElem.style.borderColor = 'red';
            errors += 1;
        }
        if(Phone.length == 0){
            errorBox.classList.remove('d-none');
            errorMsg.innerHTML += '<span>شماره تماس خود را وارد کنید</span>'
            phoneElem.style.borderColor = 'red';
            errors += 1;
        }
        else if(Phone.length > 0 && !validate_phone_number(Phone)){
            errorBox.classList.remove('d-none');
            errorMsg.innerHTML += '<span>شماره تماس خود را به درستی وارد کنید</span>'
            phoneElem.style.borderColor = 'red';
            errors += 1;
        }
        if(Address.length == 0){
            errorBox.classList.remove('d-none');
            errorMsg.innerHTML += '<span>آدرس خود را وارد کنید</span>'
            addressElem.style.borderColor = 'red';
            errors += 1;
        }
        // If no error in validation, proceeds to send ajax request to server
        if(errors == 0){
            let url = `${location.protocol}//${location.host}/login/edit-profile`;
            let data = {'first-name': firstName, 'last-name': LastName, 'email': Email,
                        'phone': Phone, 'address': Address, 'cart-id': cartId}
            sendPostData(url, data)
            .then(data => {
                // console.log(data);
                if(data['status'] != 'ok'){
                  // errorMsgElem.innerHTML = data['msg'];
                  Swal.fire({
                    icon: 'error',
                    title: 'خطا در تغییر مشخصات',
                    text: data['msg'],
                  })
                }
                else{
                  // disable submit button and set form initials as the updated profile data
                    editFormInitials = [firstName, LastName, Email, Phone, Address]
                    editProfileFormSubmitBtn.disabled = true;
                }
            })
            .catch(error => {
                // console.log(error);
                Swal.fire({
                  icon: 'error',
                  title: 'خطا در تغییر مشخصات',
                  text: error,
                })
            })
        }
    }
})




// ****************** Password change form (Only send request if there is a change in the form data)
// ? PasswordChangeForm initial data
let currentPasswordElem = document.querySelector('input[name="password"]');
let newPasswordElem = document.querySelector('input[name="password-new"]');
let confirmNewPasswordElem = document.querySelector('input[name="password-confirm"]');

// * Toggle passwords visible/invisible 
const passwords = document.querySelectorAll(".password");
Array.from(passwords).forEach(passwordDiv => {
    passwordDiv.addEventListener('click', e => {
        if (e.target.closest('.togglePassword')){
            let passwordToggler = passwordDiv.querySelector('.togglePassword');
            let passwordInput = passwordDiv.querySelector('input');
            // toggle the type attribute
            const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
            passwordInput.setAttribute("type", type);
            // toggle the icon
            passwordToggler.classList.toggle("bi-eye");
        }
    })
})

// * Validate and submit password change form
changePasswordForm.addEventListener('submit', e =>{
    e.preventDefault();
    errorBox.classList.add('d-none');
    errorMsg.innerHTML = '';
    let currentPassword = currentPasswordElem.value;
    currentPasswordElem.style.borderColor = '#dee2e6';
    let newPassword = newPasswordElem.value;
    newPasswordElem.style.borderColor = '#dee2e6';
    let confirmNewPassword = confirmNewPasswordElem.value;
    confirmNewPasswordElem.style.borderColor = '#dee2e6';
    let errors = 0;
    // Validate data
    if(currentPassword.length == 0){
        errorBox.classList.remove('d-none');
        errorMsg.innerHTML += '<span>رمز عبور خود را وارد کنید</span>'
        currentPasswordElem.style.borderColor = 'red';
        errors += 1;
    }
    if(newPassword.length == 0){
        errorBox.classList.remove('d-none');
        errorMsg.innerHTML += '<span>رمز عبور جدید را وارد کنید</span>'
        newPasswordElem.style.borderColor = 'red';
        errors += 1;
    }
    else if(newPassword.length > 0 && newPassword.length < 6){
        errorBox.classList.remove('d-none');
        errorMsg.innerHTML += '<span>رمز عبور باید بیشتر از 6 کاراکتر باشد</span>'
        newPasswordElem.style.borderColor = 'red';
        errors += 1;
    }
    else if(newPassword.length > 20){
        errorBox.classList.remove('d-none');
        errorMsg.innerHTML += '<span>رمز عبور باید کمتر از 20 کاراکتر باشد</span>'
        newPasswordElem.style.borderColor = 'red';
        errors += 1;
    }
    if(confirmNewPassword.length == 0){
        errorBox.classList.remove('d-none');
        errorMsg.innerHTML += '<span>تکرار رمز عبور را وارد کنید</span>'
        confirmNewPasswordElem.style.borderColor = 'red';
        errors += 1;
    }
    if(confirmNewPassword.length > 0 && confirmNewPassword !== newPassword){
        errorBox.classList.remove('d-none');
        errorMsg.innerHTML += '<span>تکرار رمز عبور اشتباه است</span>'
        confirmNewPasswordElem.style.borderColor = 'red';
        errors += 1;
    }
    // If no error in validation, proceeds to send ajax request to server
    if(errors == 0){
        let url = `${location.protocol}//${location.host}/login/password-change`;
        let data = {'password': currentPassword, 'password-new': newPassword, 'cart-id': cartId}
        sendPostData(url, data)
        .then(data => {
            // console.log(data);
            if(data['status'] != 'ok'){
              Swal.fire({
                icon: 'error',
                title: 'خطا در تغییر رمز عبور',
                text: data['msg'],
              })
            }
            else{
                Swal.fire({
                    icon: 'success',
                    title: 'رمز عبور',
                    text: data['msg'],
                })
                currentPasswordElem.value = ''
                newPasswordElem.value = ''
                confirmNewPasswordElem.value = ''
            }
        })
        .catch(error => {
            // console.log(error);
            Swal.fire({
              icon: 'error',
              title: 'خطا در تغییر رمز عبور',
              text: error,
            })
        })
    }
})