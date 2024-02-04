function openFile() {
    document.getElementById('fileInput').click();
}

function submitForm() {
    var fileInput = document.getElementById('fileInput');
    var textInput = document.getElementById('inputText').value;

    if (fileInput.files.length > 0) {
        handleFile();  // Call the handleFile function for CSV file analysis
    } else if (textInput.trim() !== '') {
        // Analyze sentiment for text input
        var tableBody = document.getElementById('tableBody');
        var newRow = tableBody.insertRow();
        var messageCell = newRow.insertCell(0);
        var sentimentCell = newRow.insertCell(1);

        // Display the input text in the table
        messageCell.innerHTML = textInput;

        // Analyze sentiment for text input
        analyzeTextSentiment(textInput, sentimentCell);
    } else {
        alert('Please enter text or choose a CSV file before analyzing.');
    }
}

    // Modify the handleFile function to dynamically analyze based on "message" column
    function handleFile() {
        var fileInput = document.getElementById('fileInput');
        var selectedFile = fileInput.files[0];
    
        // Check if a file is selected
        if (selectedFile) {
            // Check if the selected file is a CSV file
            if (selectedFile.name.toLowerCase().endsWith('.csv')) {
                var reader = new FileReader();
    
                reader.onload = function (e) {
                    var csvContent = e.target.result;
                    var rows = csvContent.split('\n');
                    var tableBody = document.getElementById('tableBody');
    
                    // Clear existing table content
                    tableBody.innerHTML = '';
    
                    // Find the index of the "message" column dynamically
                    var headerRow = rows[0].split(',');
                    var messageIndex = headerRow.findIndex(column => column.toLowerCase().trim() === 'message');
    
                    for (var i = 1; i < rows.length; i++) {
                        var cells = rows[i].split(',');
    
                        if (cells.length > messageIndex) {
                            var newRow = tableBody.insertRow();
                            var messageCell = newRow.insertCell(0);
                            var sentimentCell = newRow.insertCell(1);
    
                            var messageText = cells[messageIndex].trim();
                            messageCell.innerHTML = messageText;
    
                            // Analyze sentiment for each message
                            analyzeTextSentiment(messageText, sentimentCell);
                        }
                    }
    
                    alert('CSV file uploaded and analyze successfully');
                };
    
                reader.readAsText(selectedFile);
            } else {
                // Show an error alert for invalid file format
                alert('Invalid file format. Please select a CSV file.');
                // Reset the file input
                fileInput.value = '';
            }
        } else {
            // The user canceled file selection
            console.log('File selection canceled.');
        }
    }
    
    // Modify the analyzeTextSentiment function to handle both CSV and text inputs
    function analyzeTextSentiment(text, sentimentCell) {
        // Assuming your Flask server is running on http://127.0.0.1:5000
        fetch('http://127.0.0.1:5000/api/sentiment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'text': text }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('API Response:', data);  // Add this line for debugging
            sentimentCell.innerHTML = data.sentiment;
        })
        .catch(error => console.error('Error:', error));
    }
    

function clearText() {
    document.getElementById('inputText').value = '';
}

 function clearTable() {
    // Clear the name displayed on the button
    var button = document.getElementById('fileButton');
    button.innerText = 'Choose File';

    // Reset the file input
    var fileInput = document.getElementById('fileInput');
    fileInput.value = '';

    // Clear the table content
    var tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';
}