const form = document.getElementById('user-form')

form.addEventListener('submit', async(e) => {
    e.preventDefault();
    const usernameValid = await checkUsernameExists();
    if (!usernameValid) return; // Stop if username is invalid

    form.submit();
});

const checkUsernameExists = async () => {
    const form = document.forms['user-form']
    const username = form['username'].value.trim()

    try {
        const response = await axios.post('/validate-username-registration/', { username });
        if (response.data.username_exists === 'false') {
            alert("User does not exist. Enter existing username.");
            return false;
        }
        return true;
    } catch (error) {
        console.log(error);
        return false; // Treat errors as validation failures
    }
}
