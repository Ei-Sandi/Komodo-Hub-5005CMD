const form = document.getElementById('login-form')

form.addEventListener('submit', async(e) => {
    e.preventDefault();
    const usernameValid = await checkUsernameExists();
    const passwordValid = await checkPassword();

    if (!(usernameValid && passwordValid)) {
        form.submit();
    }
});

const checkUsernameExists = async () => {
    const form = document.forms['login-form']
    const username = form['username'].value.trim()

    axios.post('/validate-username-registration/',{
        username:username
    })
    .then ((response) => {
        if (response.data.username_exists == 'false'){
            alert ("Invalid Username. Please register first.")
            return false;
        } else {
            return true;
        }
    }, (error) => {
        console.log(error);
    })
}

const checkPassword = async () => {
    const form = document.forms['login-form']
    const username = form['username'].value.trim()
    const password = form['password'].value.trim()
    
    axios.post('/check-password/',{
        username:username,
        password:password
    })
    .then ((response) => {
        if (response.data.password_match == 'false'){
            alert ("Invalid Password.")
            return false;
        } else {
            return true;
        }
    }, (error) => {
        console.log(error);
    })
}
