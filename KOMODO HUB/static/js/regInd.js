const form = document.getElementById('form')
const email = document.getElementById('email')
const first = document.getElementById('first')
const last = document.getElementById('last')
const username = document.getElementById('username')
const password = document.getElementById('Pass')
const repass = document.getElementById('RePass')

form.addEventListener('submit', e => {
    e.preventDefault();
    validateInputs();
});

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success');
}
const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
}
const isValidEmail = email => {
    const re = /^[^@]+@[^@]+\.[^@]+$/;
    return re.test(String(email).toLowerCase());
}
const hasNumber = str => {
    const hasNumber = /\d/.test(str);
    return hasNumber;
}
const hasChar = str => {
    const hasChar = /[a-zA-Z]/.test(str);
    return hasChar;
}
const hasSpace = str => {
    return str.includes(' ');
}
const validateInputs = () => {
    const emailValue = email.value.trim();
    const usernameValue = username.value.trim();
    const firstValue = first.value.trim();
    const lastValue = last.value.trim();
    const passwordValue = password.value.trim();
    const repassValue = repass.value.trim();

    if (emailValue === ''){
        setError(email, 'Email is required');
    } else if (!isValidEmail(emailValue)) {
        setError(email, 'Provide a valid email address');
    } else {
        setSuccess(email);
    }

    if (usernameValue === ''){
        setError(username, 'Username is required');
    } else if (usernameValue.length < 8) {
        setError(username, 'Username must be at least 8 characters.');
    } 
    else if (!hasNumber(usernameValue) || !hasChar(usernameValue)) {
        setError(username, 'Username must include characters and numbers.');
    } else if (hasSpace(usernameValue)){
        setError(username, 'Username cannot include space.');
    }
    else {
        setSuccess(username);
    }

    if (firstValue === ''){
        setError(first, 'First name is required');
    } else if (hasNumber(firstValue)) {
        setError(first, 'First name cannot include numbers');
    }
    else {
        setSuccess(first);
    }

    if (lastValue === ''){
        setError(last, 'Last name is required');
    } else if (hasNumber(lastValue)) {
        setError(last, 'Last name cannot include numbers');
    }else {
        setSuccess(first);
    }

    if (passwordValue === ''){
        setError(password, 'Password is required');
    } else if (passwordValue.length < 8) {
        setError(password, 'Password must be at least 8 characters.');
    } else {
        setSuccess(password);
    }

    if (repassValue === ''){
        setError(repass, 'Password is required');
    } else if (repassValue != passwordValue) {
        setError(repass, 'Passwords do not match.');
    } else {
        setSuccess(repass);
    }
};