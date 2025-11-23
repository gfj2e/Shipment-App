// Question 1: Insert shipment tuple, uses POST and calls the insert method from the backend
document.getElementById('insertQ1').addEventListener('click', function() {
    const supplierId = document.getElementById('supplierIdQ1').value;
    const partNo = document.getElementById('partNoQ1').value;
    const quantity = document.getElementById('quantityQ1').value;
    const price = document.getElementById('priceQ1').value;
    const resultDiv = document.getElementById('resultQ1');
    
    // Validate inputs
    if (!supplierId || !partNo || !quantity || !price) {
        alert('Please fill in all fields for Q1');
        return;
    }
    
    fetch('/insert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ supplierId, partNo, quantity, price }),
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `
            <h5>Operation Result:</h5>
            <span class="badge ${data.success ? 'badge-success' : 'badge-danger'}">${data.success ? 'Success' : 'Error'}</span>
            <p class="mt-2 mb-0">${data.message}</p>
        `;
        resultDiv.style.display = 'block';
    })
    .catch((error) => {
        console.error('Error:', error);
        resultDiv.innerHTML = `
            <h5>Operation Result:</h5>
            <span class="badge badge-danger">Error</span>
            <p class="mt-2 mb-0">An error occurred while communicating with the server.</p>
        `;
        resultDiv.style.display = 'block';
    });
});

// Question 2: Insert another shipment tuple, uses POST and calls the insert method from the backend
document.getElementById('insertQ2').addEventListener('click', function() {
    const supplierId = document.getElementById('supplierIdQ2').value;
    const partNo = document.getElementById('partNoQ2').value;
    const quantity = document.getElementById('quantityQ2').value;
    const price = document.getElementById('priceQ2').value;
    const resultDiv = document.getElementById('resultQ2');
    
    if (!supplierId || !partNo || !quantity || !price) {
        alert('Please fill in all fields for Q2');
        return;
    }
    
    fetch('/insert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ supplierId, partNo, quantity, price }),
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `
            <h5>Operation Result:</h5>
            <span class="badge ${data.success ? 'badge-success' : 'badge-danger'}">${data.success ? 'Success' : 'Error'}</span>
            <p class="mt-2 mb-0">${data.message}</p>
        `;
        resultDiv.style.display = 'block';
    })
    .catch((error) => {
        console.error('Error:', error);
        resultDiv.innerHTML = `
            <h5>Operation Result:</h5>
            <span class="badge badge-danger">Error</span>
            <p class="mt-2 mb-0">An error occurred while communicating with the server.</p>
        `;
        resultDiv.style.display = 'block';
    });
});

// Question 3: Increase supplier status, uses POST to raise the status of every supplier
document.getElementById('increaseStatus').addEventListener('click', function() {
    const percentage = document.getElementById('percentage').value;
    const resultDiv = document.getElementById('resultQ3');

    fetch("/raise_status", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ percentage: percentage }),
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `
            <h5>Operation Result:</h5>
            <span class="badge ${data.success ? 'badge-success' : 'badge-danger'}">${data.success ? 'Success' : 'Error'}</span>
            <p class="mt-2 mb-0">${data.message}</p>
        `;
        resultDiv.style.display = 'block';
    })
    .catch((error) => {
        console.error('Error:', error);
        resultDiv.innerHTML = `
            <h5>Operation Result:</h5>
            <span class="badge badge-danger">Error</span>
            <p class="mt-2 mb-0">An error occurred while communicating with the server.</p>
        `;
        resultDiv.style.display = 'block' ;
    });
});

// Question 4: Display all suppliers, uses GET to fetcht the data from the backend
document.getElementById('displaySuppliers').addEventListener('click', function() {
    const resultDiv = document.getElementById('resultQ4');
    
    fetch('/get_suppliers')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let tableRows = '';
                data.data.forEach(supplier => {
                    tableRows += `
                        <tr>
                            <td>${supplier.Sno}</td>
                            <td>${supplier.Sname}</td>
                            <td>${supplier.Status}</td>
                            <td>${supplier.City}</td>
                        </tr>
                    `;
                });

                resultDiv.innerHTML = `
                    <h5 class="section-title">All Suppliers</h5>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Supplier ID</th>
                                    <th>Name</th>
                                    <th>Status</th>
                                    <th>City</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${tableRows}
                            </tbody>
                        </table>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `<p class="text-danger">${data.message}</p>`;
            }
            resultDiv.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = `<p class="text-danger">An error occurred while fetching data.</p>`;
            resultDiv.style.display = 'block';
        });
});

// Question 5: Find suppliers by part, uses POST to send the user request to backend
document.getElementById('findSuppliers').addEventListener('click', function() {
    const partNo = document.getElementById('partNo').value;
    const resultDiv = document.getElementById('resultQ5');
    
    if (!partNo) {
        alert('Please enter a part number');
        return;
    }
    
    fetch('/find_suppliers_by_part', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ partNo: partNo }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let tableRows = '';
                if (data.data.length > 0) {
                    data.data.forEach(supplier => {
                        tableRows += `
                            <tr>
                                <td>${supplier.Sno}</td>
                                <td>${supplier.Sname}</td>
                                <td>${supplier.Status}</td>
                                <td>${supplier.City}</td>
                            </tr>
                        `;
                    });
                } else {
                    tableRows = '<tr><td colspan="4" class="text-center">No suppliers found for this part.</td></tr>';
                }

                resultDiv.innerHTML = `
                    <h5 class="section-title">Suppliers Who Shipped Part ${partNo}</h5>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Supplier ID</th>
                                    <th>Name</th>
                                    <th>Status</th>
                                    <th>City</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${tableRows}
                            </tbody>
                        </table>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `<p class="text-danger">${data.message}</p>`;
            }
            resultDiv.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = `<p class="text-danger">An error occurred while fetching data.</p>`;
            resultDiv.style.display = 'block';
        });
});

// Resets the database when button clicked
document.getElementById('resetDatabase').addEventListener('click', function() {
    const resultDiv = document.getElementById('reset');

    fetch('/reset_database') 
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `
            <h5>Operation Result:</h5>
            <span class="badge ${data.success ? 'badge-success' : 'badge-danger'}">${data.success ? 'Success' : 'Error'}</span>
            <p class="mt-2 mb-0">${data.message}</p>
        `;
        resultDiv.style.display = 'block' ;   
        })

        .catch((error) => {
        console.error('Error:', error);
        resultDiv.innerHTML = `
            <h5>Operation Result:</h5>
            <span class="badge badge-danger">Error</span>
            <p class="mt-2 mb-0">An error occurred while communicating with the server.</p>
        `;
        resultDiv.style.display = 'block' ;
    });
});