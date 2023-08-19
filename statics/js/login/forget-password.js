// ! In current module we imported 'csrftoken.js' and 'functions.js' even so we have not used them! If we don't that, the browser can't find the modules we have not used!!! 
import getCookie from '../csrftoken.js';
import { validateEmail } from '../functions.js';
import { sendPostData } from '../ajax.js';



// *** Validate forgetPasswordForm
const forgetPasswordForm = document.getElementById('fp-c');
forgetPasswordForm.addEventListener('submit', e => {
    e.preventDefault();
    let passwordElem = document.getElementById('password');
    let confirmPasswordElem = document.getElementById('password-confirm');
    let errors = 0;

    if(passwordElem.value.length == 0){
        Swal.fire({
            icon: 'error',
            title: 'خطا در رمز عبور',
            text: 'رمز عبور را وارد کنید',
        })
        errors += 1;
    }
    else if(passwordElem.value.length < 6){
        Swal.fire({
            icon: 'error',
            title: 'خطا در رمز عبور',
            text: 'رمز عبور باید بیش از 6 کاراکتر باشد',
        })
        errors += 1;
    }
    else if(passwordElem.value.length > 20){
        Swal.fire({
            icon: 'error',
            title: 'خطا در رمز عبور',
            text: 'رمز عبور باید کمتر از 20 کاراکتر باشد',
        })
        errors += 1;
    }
    else if(confirmPasswordElem.value.length == 0){
        Swal.fire({
            icon: 'error',
            title: 'خطا در رمز عبور',
            text: 'تکرار رمز عبور را وارد کنید',
        })
        errors += 1;
    }
    else if (passwordElem.value != confirmPasswordElem.value){
        Swal.fire({
            icon: 'error',
            title: 'خطا در رمز عبور',
            text: 'تکرار رمز عبور با مرز عبور یکسان نیست',
        })
        errors += 1;
    }
    // We dont use ajax to send data to server. form.submit in enough
    if(errors === 0){
        forgetPasswordForm.submit();
    }
})