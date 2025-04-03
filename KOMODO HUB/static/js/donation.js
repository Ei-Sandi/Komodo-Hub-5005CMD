document.getElementById('donation-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting

    // Gather form data
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const phoneNumber = document.getElementById('phone-number').value;
    const cardNumber = document.getElementById('card-number').value;
    const cvv = document.getElementById('cvv').value;
    const expirationDate = document.getElementById('expiration-date').value;
    const billingAddress = document.getElementById('billing-address').value;
    const email = document.getElementById('email').value;
    const recurring = document.querySelector('input[name="recurring"]:checked').value;

    // Check if all fields are filled
    if (!firstName || !lastName || !phoneNumber || !cardNumber || !cvv || !expirationDate || !billingAddress || !email) {
        alert('Please fill in all required fields.');
        return;
    }

    // Submit the donation (for now, just log the data)
    console.log({
        firstName,
        lastName,
        phoneNumber,
        cardNumber,
        cvv,
        expirationDate,
        billingAddress,
        email,
        recurring
    });

    alert('Thank you for your donation!');
});
