const RunSentimentAnalysis = () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const output = document.getElementById("system_response");
    const xhttp = new XMLHttpRequest();
    output.textContent = "Analyzing...";
    xhttp.onreadystatechange = function () {
        if (this.readyState !== 4) return;
        if (this.status === 200 || this.status === 400) {
            output.textContent = this.responseText;
        } else {
            output.textContent = "Analysis unavailable. Please try again later.";
        }
    };
    xhttp.open("GET", "/emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
};
