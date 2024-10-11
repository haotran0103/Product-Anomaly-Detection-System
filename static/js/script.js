async function predictSingle() {
    const fileInput = document.getElementById('singleFileInput');
    const resultDiv = document.getElementById('singleResult');

    if (fileInput.files.length === 0) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://localhost:8000/predict/', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (response.ok) {
            displaySingleResult(data.overlay_image);
            resultDiv.insertAdjacentHTML('afterbegin', `<p>Anomaly Detected: ${data.anomaly_detected}</p>`);
        } else {
            resultDiv.innerHTML = `<p>Error: ${data.detail}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}

async function predictMultiple() {
    const fileInput = document.getElementById('multipleFilesInput');
    const resultDiv = document.getElementById('multipleResults');

    if (fileInput.files.length === 0) {
        alert('Please select one or more image files.');
        return;
    }

    const formData = new FormData();
    for (const file of fileInput.files) {
        formData.append('files', file);
    }

    try {
        const response = await fetch('http://localhost:8000/predict_multiple/', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (response.ok) {
            // Tạo mảng các overlay_image từ kết quả trả về
            const overlayImages = data.map(result => result.overlay_image);
            displayMultipleResults(overlayImages);
            resultDiv.insertAdjacentHTML('afterbegin', data.map(result => `
                <div>
                    <p>Filename: ${result.filename}</p>
                    <p>Anomaly Detected: ${result.anomaly_detected}</p>
                </div>
            `).join(''));
        } else {
            resultDiv.innerHTML = `<p>Error: ${data.detail}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}

function displaySingleResult(imageData) {
    const resultDiv = document.getElementById('singleResult');
    resultDiv.className = 'image-container single'; 
    resultDiv.innerHTML = `<img src="data:image/jpeg;base64,${imageData}" alt="Single Prediction">`;
}

function displayMultipleResults(images) {
    const resultDiv = document.getElementById('multipleResults');
    resultDiv.className = 'image-container multiple'; 
    resultDiv.innerHTML = images.map(imageData => 
        `<img src="data:image/jpeg;base64,${imageData}" alt="Multiple Prediction">`
    ).join('');
}
