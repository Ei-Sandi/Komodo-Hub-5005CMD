const form = document.getElementById('login-form')

form.addEventListener('submit', async(e) => {
    e.preventDefault();
    const usernameValid = await checkUsernameExists();
    if (!usernameValid) return; // Stop if username is invalid

    const passwordValid = await checkPassword();
    if (!passwordValid) return; // Stop if password is incorrect

    form.submit();
});

const checkUsernameExists = async () => {
    const form = document.forms['login-form']
    const username = form['username'].value.trim()

    try {
        const response = await axios.post('/validate-username-registration/', { username });
        if (response.data.username_exists === 'false') {
            alert("Invalid Username. Please register first.");
            return false;
        }
        return true;
    } catch (error) {
        console.log(error);
        return false; // Treat errors as validation failures
    }
}

const checkPassword = async () => {
    const form = document.forms['login-form']
    const username = form['username'].value.trim()
    const password = form['password'].value.trim()
    
    try {
        const response = await axios.post('/check-password/', { username, password });
        if (response.data.password_match === 'false') {
            alert("Invalid Password.");
            return false;
        }
        return true;
    } catch (error) {
        console.log(error);
        return false;
    }
}
