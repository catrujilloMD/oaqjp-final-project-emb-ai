# Final project
## Purpose
Educational emotion-analysis demo using fictional clinic feedback.
It is not a diagnostic tool and does not establish a person's actual emotional state.

## Run locally
```powershell
py -m pip install Flask requests
py server.py
```
Open http://127.0.0.1:5000.

## Verified tests
```powershell
py -m unittest test_server -v
```
All 3 tests passed using simulated Watson responses:
- Valid text returns HTTP 200 and formatted scores.
- Missing, empty, or whitespace-only input returns HTTP 400 without calling Watson.
- A simulated rejection by Watson returns HTTP 400.

The browser also displayed the invalid-input message correctly.

## Client-request example
```powershell
curl.exe -i "http://127.0.0.1:5000/emotionDetector?textToAnalyze="
```
Verified result: HTTP 400 BAD REQUEST.
Response: Invalid text! Please try again!

## Synthetic healthcare example and limitation
Input: "The clinic staff were kind and helpful. I am happy with the service."

The local live request timed out while connecting to Watson after 30 seconds.
The application returned HTTP 500 and displayed "Analysis unavailable."
No emotion result was obtained for this example.

Next improvement: handle connection failures explicitly and return HTTP 503.