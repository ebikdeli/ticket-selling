import {validateEmail} from '../functions.js';
import { sendPostData } from '../ajax.js';
import getCookie from '../csrftoken.js';


let cartId = document.querySelector('.cart-id').value;


// * Toggle password visible/invisible (LOGIN and SIGNUP FORM)
const togglePasswords = document.querySelectorAll(".togglePassword");
Array.from(togglePasswords).forEach(togglepassword => {
    togglepassword.addEventListener("click", function () {
        // toggle the type attribute
        const passwordInput = this.previousElementSibling;
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        // const type = loginPassword.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);
        // toggle the icon
        this.classList.toggle("bi-eye");
    });
})



// * Toggle between login button and signup button
const loginButton = document.querySelector('#login-button');
const loginSection = document.querySelector('#login-section');
const signupButton = document.querySelector('#signup-button');
const signUpSection = document.querySelector('#signup-section');

// If login-button is disable, enable it by click on it then hide the signup form and show signin form
loginButton.addEventListener('click', e=>{
    if(!loginButton.classList.contains('active')){
        signupButton.classList.toggle('active');
        loginButton.classList.toggle('active');
        // Hide signup form and show signin form
        signUpSection.classList.add('d-none');
        loginSection.classList.remove('d-none');
    }
})
// If signup-button is disable, enable it by click on it then hide the signin form and show signup form
signupButton.addEventListener('click', e=>{
    if(!signupButton.classList.contains('active')){
        loginButton.classList.remove('active');
        signupButton.classList.add('active');
        // Hide Signin form and show signup form
        loginSection.classList.add('d-none');
        signUpSection.classList.remove('d-none');
    }
})



// * Gender button selection in SignUp Form
const maleButton = document.querySelector('.male');
const femaleButton = document.querySelector('.female');

// If not male button active, activate male button and deactive female button (if activated before)
maleButton.addEventListener('click', e => {
    if(!maleButton.classList.contains('active')){
        // If female button active, 
        if(femaleButton.classList.contains('active')){
            femaleButton.classList.remove('active');
            femaleButton.classList.remove('q-secondary');
            femaleButton.classList.add('q-gray');
        }
        femaleButton.classList.add('border-right-none');
        maleButton.classList.add('active');
        maleButton.classList.add('q-secondary')
        maleButton.classList.remove('border-left-none');
        maleButton.classList.remove('q-gray');
        document.querySelector('input[name="gender"]').value = 'M'
    }
})
// If not female button active, activate female button and deactive male button (if activated before)
femaleButton.addEventListener('click', e => {
    if(!femaleButton.classList.contains('active')){
        if(maleButton.classList.contains('active')){
            maleButton.classList.remove('active');
            maleButton.classList.remove('q-secondary');
            maleButton.classList.add('q-gray');
        }
        maleButton.classList.add('border-left-none');
        femaleButton.classList.add('active');
        femaleButton.classList.add('q-secondary');
        femaleButton.classList.remove('border-right-none');
        femaleButton.classList.remove('q-gray');
        document.querySelector('input[name="gender"]').value = 'F'
    }
})



// *** Validate Login form
const validateLoginForm = (email=new String, password=new String) => {
    let errorBox = document.querySelector('#error-box-wrapper');
    let erroMsg = document.querySelector('.message');
    errorBox.classList.add('d-none');
    erroMsg.innerHTML = '';
    let errors = 0;
    // Process form data
    if(email.length == 0){
        errorBox.classList.remove('d-none');
        erroMsg.innerHTML = 'ایمیل خود را وارد کنید';
        errors += 1;
        return false;
    }
    else if(email.length > 0 && (!validateEmail(email))){
        errorBox.classList.remove('d-none');
        erroMsg.innerHTML = 'ایمیل خود را به درستی وارد کنید';
        errors += 1;
        return false;
    }
    else if(password.length == 0){
        errorBox.classList.remove('d-none');
        erroMsg.innerHTML = 'رمز عبور خود را وارد کنید';
        errors += 1;
        return false;
    }
    // If there is no error in validation, return true
        return true;
}



// *** Validate SignUp form
const validateSignupForm = (email=new String, password=new String) => {
    let errorBox = document.querySelector('#error-box-wrapper');
    let erroMsg = document.querySelector('.message');
    errorBox.classList.add('d-none');
    erroMsg.innerHTML = '';
    let errors = 0;
    // Process form data
    if(email.length == 0){
        errorBox.classList.remove('d-none');
        erroMsg.innerHTML = 'ایمیل خود را وارد کنید';
        errors += 1;
        return false;
    }
    else if(email.length > 0 && (!validateEmail(email))){
        errorBox.classList.remove('d-none');
        erroMsg.innerHTML = 'ایمیل خود را به درستی وارد کنید';
        errors += 1;
        return false;
    }
    else if(password.length == 0){
        errorBox.classList.remove('d-none');
        erroMsg.innerHTML = 'رمز عبور خود را وارد کنید';
        errors += 1;
        return false;
    }
    else if(password.length < 6){
        errorBox.classList.remove('d-none');
        erroMsg.innerHTML = 'رمز عبور کمتر از 6 کاراکتر است';
        errors += 1;
        return false;
    }
    else if(password.length > 20){
        errorBox.classList.remove('d-none');
        erroMsg.innerHTML = 'رمز عبور بیش از 20 کاراکتر است';
        errors += 1;
        return false;
    }
    // If there is no error in validation, return true
        return true;
}



// *** Send AJAX request to Login user
const loginForm = document.querySelector('#login-form');
loginForm.addEventListener('submit', function(e){
    e.preventDefault();
    let email = this.querySelector('#login-username').value;
    let password = this.querySelector('#login-password').value;
    if (validateLoginForm(email, password)) {
        let url = `${location.protocol}//${location.host}/login/login/`;
        let data = {'username': email, 'password': password, 'cart-id': cartId}
        sendPostData(url, data)
        .then(data => {
            if(data['status'] != 'ok'){
                Swal.fire({
                    icon: 'error',
                    title: 'خطا در ورود',
                    text: data['msg'],
                })
            }
            else{
                location.replace(`${location.protocol}//${location.host}`);
            }
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'خطا در ورود',
                text: error,
            })
        })
    }
})



// *** Send AJAX request to Signup user
const signUpForm = document.querySelector('#signup-form');
signUpForm.addEventListener('submit', function(e){
    e.preventDefault();
    let email = this.querySelector('#signup-username').value;
    let password = this.querySelector('#signup-password').value;
    if (validateSignupForm(email, password)) {
        let url = `${location.protocol}//${location.host}/login/signup/`;
        let gender = document.querySelector('input[name="gender"]').value;
        if (gender.length == 0){
            gender = null;
        }
        let allowMarketing = document.querySelector('#marketing-verify-checkbox').checked;
        let allowPersonalData = document.querySelector('#personal-verify-checkbox').checked;
        let data = {'username': email, 'password': password, 'cart-id': cartId, 'gender': gender, 'marketing': allowMarketing, 'personal': allowPersonalData}
        sendPostData(url, data)
        .then(data => {
            if(data['status'] != 'ok'){
                Swal.fire({
                    icon: 'error',
                    title: 'خطا در ثبت نام',
                    text: data['msg'],
                })
            }
            else{
                location.replace(`${location.protocol}//${location.host}`);
            }
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'خطا در ورود',
                text: error,
            })
        })
    }
})