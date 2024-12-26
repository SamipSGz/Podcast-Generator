document.getElementById('audioForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const sourceFileUrl = document.getElementById('sourceFileUrl').value;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = "Generating audio, please wait...";

    try {
        const response = await fetch('http://127.0.0.1:8000/generate_audio/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ source_file_url: sourceFileUrl }),
        });

        const data = await response.json();

        if (response.ok) {
            resultDiv.innerHTML = `
                <p>Audio generated successfully!</p>
                <audio controls>
                    <source src="${data.audio_url}" type="audio/wav">
                    Your browser does not support the audio element.
                </audio>
                <a href="http://127.0.0.1:8000/download_audio/?audio_url=${encodeURIComponent(data.audio_url)}" download>
                    <button>Download Audio</button>
                </a>
            `;
        } else {
            resultDiv.innerHTML = `<p>Error: ${data.detail}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});
