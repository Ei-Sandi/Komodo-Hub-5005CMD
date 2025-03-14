const checkUserExists = () => {
    const email = document.getElementById('email')
    const emailValue = email.value.trim();
    const usernameValue = username.value.trim();

    axios.post('/validate-user-registration'),{
        email:emailValue
    } 
    .then ((response) => {
        if (response.data.email_exists == 'true'){
            setError(email, 'Email exists. Please log in.')
        } else {
            setSuccess(email);
        }
    }, (error) => {
        console.log(error);
    })
}
