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
    let isValid = true;

    if (emailValue === ''){
        setError(email, 'Email is required');
        isValid = false;
    } 
    else if (!isValidEmail(emailValue)) {
        setError(email, 'Provide a valid email address');
        isValid = false;
    } 
    else {
        setSuccess(email);
    }

    if (usernameValue === ''){
        setError(username, 'Username is required');
        isValid = false;
    } 
    else if (usernameValue.length < 8) {
        setError(username, 'Username must be at least 8 characters.');
        isValid = false;
    } 
    else if (!hasNumber(usernameValue) || !hasChar(usernameValue)) {
        setError(username, 'Username must include characters and numbers.');
        isValid = false;
    } 
    else if (hasSpace(usernameValue)){
        setError(username, 'Username cannot include space.');
        isValid = false;
    }
    else {
        setSuccess(username);
    }

    if (firstValue === ''){
        setError(first, 'First name is required');
        isValid = false;
    } 
    else if (hasNumber(firstValue)) {
        setError(first, 'First name cannot include numbers');
        isValid = false;
    }
    else {
        setSuccess(first);
    }

    if (lastValue === ''){
        setError(last, 'Last name is required');
        isValid = false;
    } 
    else if (hasNumber(lastValue)) {
        setError(last, 'Last name cannot include numbers');
        isValid = false;
    }
    else {
        setSuccess(first);
    }

    if (passwordValue === ''){
        setError(password, 'Password is required');
        isValid = false;
    } 
    else if (passwordValue.length < 8) {
        setError(password, 'Password must be at least 8 characters.');
        isValid = false;
    } 
    else {
        setSuccess(password);
    }

    if (repassValue === ''){
        setError(repass, 'Password is required');
        isValid = false;
    } 
    else if (repassValue != passwordValue) {
        setError(repass, 'Passwords do not match.');
        isValid = false;
    } 
    else {
        setSuccess(repass);
    }
    if (isValid){
        checkEmailExists();
        checkUsernameExists();
    }
};

const checkEmailExists = () => {
    const form = document.forms['form']
    const email = form['email'].value.trim()

    axios.post('/validate-email-registration/',{
        email:email
    })
    .then ((response) => {
        if (response.data.email_exists == 'true'){
            setError(form['email'], 'Email exists. Please log in.');
        } else {
            setSuccess(form['email']);
        }
    }, (error) => {
        console.log(error);
    })
}

const checkUsernameExists = () => {
    const form = document.forms['form']
    const username = form['username'].value.trim()

    axios.post('/validate-username-registration/',{
        username:username
    })
    .then ((response) => {
        if (response.data.username_exists == 'true'){
            setError(form['username'], 'Username exists. Please log in.');
        } else {
            setSuccess(form['username']);
        }
    }, (error) => {
        console.log(error);
    })
}