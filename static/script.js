function chooseFile() {
    // Create a file input dynamically
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.name = 'file';
    fileInput.id = 'file';
    fileInput.accept = '.csv';

    // Append the file input to the form
    const form = document.getElementById('sentimentForm');
    form.appendChild(fileInput);

    // Trigger the click event to open the file dialog
    fileInput.click();

    // Remove the file input after the user selects a file
    fileInput.addEventListener('change', function () {
        // Remove any existing hidden input for text
        const hiddenInput = document.getElementById('hiddenText');
        if (hiddenInput) {
            form.removeChild(hiddenInput);
        }

        // Remove the file input after the user selects a file
        form.removeChild(fileInput);
    });
}

function analyzeText() {
    // Retrieve the input text
    const text = document.getElementById('inputText').value;

    // Create a hidden input field for text
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'text';
    hiddenInput.id = 'hiddenText';
    hiddenInput.value = text;

    const form = document.getElementById('sentimentForm');
    form.appendChild(hiddenInput);

    // Fetch the sentiment analysis result
    fetch('/analyze', {
        method: 'POST',
        body: new FormData(form),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(results => {
        // Check the console for the received results
        console.log(results);

        // Update the table dynamically with the sentiment analysis results
        updateTable(results);

        // Remove the hidden input after form submission
        form.removeChild(hiddenInput);
    })
    .catch(error => {
        console.error('Error:', error);
        
        // Check if the response is JSON
        if (error.headers && error.headers.get('content-type') && error.headers.get('content-type').includes('application/json')) {
            return error.json().then(errorMessage => console.error('Server Response:', errorMessage));
        } else {
            console.error('Server Response is not JSON:', error.statusText);
        }
    });
}

// Function to update the table with sentiment analysis results
function updateTable(results) {
    const tableBody = document.querySelector('.table_body table tbody');
    
    // Clear existing table content
    tableBody.innerHTML = '';

    // Iterate through the results and append rows to the table
    results.forEach(result => {
        const row = document.createElement('tr');
        const textCell = document.createElement('td');
        const lexiconCell = document.createElement('td');

        textCell.textContent = result.text;
        lexiconCell.textContent = result.lexicon;

        row.appendChild(textCell);
        row.appendChild(lexiconCell);

        tableBody.appendChild(row);
    });
}

function clearText() {
    // Clear the input text
    document.getElementById('inputText').value = '';
}

function clearTable() {
    // Clear the table content
    const tableBody = document.querySelector('.table_body table tbody');
    tableBody.innerHTML = '';
}