function onSubmit() {
    // Prevent the default form submission behavior

    var amount = document.forms["myForm"]["amount"];
    var transactionDate = document.forms["myForm"]["transactiondate"];
    var transactionTime = document.forms["myForm"]["transactiontime"];
    var category = document.forms["myForm"]["category"];
    var currentDate = new Date();
    var dataValidated = true;

    // Validate form fields
    if (amount.value === '' || transactionDate.value === '' || transactionTime.value === '' || category.value === '') {
        alert("Please fill all the required data!");
        dataValidated = false;
    }

    if (isNaN(amount.value)) {
        alert("Please enter a valid amount!");
        dataValidated = false;
    }

    var inputDate = new Date(transactionDate.value + 'T' + transactionTime.value);
    if (inputDate > currentDate) {
        alert("Please Enter A Valid Date!");
        dataValidated = false;
    }

    if (dataValidated) {
        // Collect user input data from form
        var form = document.getElementById("myForm");
        var formData = {};

        // Loop through each form element
        for (var i = 0; i < form.elements.length; i++) {
            var element = form.elements[i];
            // Check if the element is an input field with a name
            if (element.tagName === 'INPUT' || element.tagName === 'SELECT') {
                formData[element.name] = element.value;
            }
        }
        console.log(formData);

        // Send a POST request to the server (Flask) for prediction
        fetch("/hello", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("This Transaction is " + data.prediction);
            }
        })
        .catch(error => console.error("Error:", error));
    }
}

