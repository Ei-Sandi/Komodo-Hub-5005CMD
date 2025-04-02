const form = document.getElementById('orgForm')
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nameValid = await checkOrgNameExists();
    console.log(nameValid);

    if (nameValid){
        form.submit();
    }
});

const checkOrgNameExists = async () => {
    const form = document.forms['orgForm']
    const orgname = form['orgName'].value.trim()
    
    try {
        const response = await axios.post('/validate-orgname-registration/',{orgname:orgname});
        if (response.data.orgname_exists == 'true'){
            alert("Organisation name already taken. Please choose a different one.");
            return false;
        } else {
            console.log('here1')
            return true;
        }
    } catch (error){
        console.log(error);
        return false;
    }
}