function momoPay(total) {
    var totals = total;
    console.log("momo");
    fetch('/api/momo-pay', {
        method: "POST",
        body: JSON.stringify({
            "total": totals
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        if (data.payUrl) {
            window.location.href = data.payUrl;
        } else {
            console.error('payUrl not found in response');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function zaloPay(total) {
    var totals = total;
    console.log("zalopay");
    fetch('/api/momo-pay', {
        method: "POST",
        body: JSON.stringify({
            "total": totals
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        if (data.payUrl) {
            window.location.href = data.payUrl;
        } else {
            console.error('payUrl not found in response');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
    function submitFormAndPay(total) {
//    const paymethod = document.getElmentByName('payMethod');
    const form = document.getElementById('passengerForm');
    console.log(total)
    const formData = new FormData(form);
    const payMethod = formData.get('payMethod');
    const passengersQuantity = formData.get('passengers_quantity');

    const passengersData = [];
    for (let i = 0; i < passengersQuantity; i++) {
        const passenger = {
            name: formData.get(`name_${i}`),
            phoneNumber: formData.get(`phoneNumber_${i}`),
            address: formData.get(`address_${i}`),
            cccd: formData.get(`cccd_${i}`),
            email: formData.get(`email_${i}`)
        };
        passengersData.push(passenger);
    }

    localStorage.setItem('passengersData', JSON.stringify(passengersData));
    localStorage.setItem('selectedSeats', formData.get('selected_seats'));
    console.log(payMethod.value)
    if (payMethod == "MOMO" ){
        momoPay(total);
    } else {
        zaloPay(total);
    }

}