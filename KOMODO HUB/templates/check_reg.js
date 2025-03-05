function checking()
    {
        var form1 = document.getElementById('form1')
        if (form1.Pass.value != form1.RePass.value)
        {
            alert("Passwords do not match")
            form1.Pass.focus();
            return false;

        }
        return true;
    }