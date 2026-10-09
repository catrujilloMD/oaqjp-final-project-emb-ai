"""Offline route tests: Watson is replaced with controlled responses."""
import unittest
from unittest.mock import patch
from server import app


class TestEmotionRoutes(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("server.emotion_detector")
    def test_valid_text(self, detector):
        detector.return_value = {
            "anger": 0.01, "disgust": 0.02, "fear": 0.03,
            "joy": 0.9, "sadness": 0.04, "dominant_emotion": "joy"
        }
        response = self.client.get(
            "/emotionDetector",
            query_string={"textToAnalyze": "The clinic staff were kind & helpful."}
        )
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("The dominant emotion is joy.", body)
        self.assertIn("'joy': 0.9", body)
        detector.assert_called_once_with("The clinic staff were kind & helpful.")

    @patch("server.emotion_detector")
    def test_blank_input_rejected_before_service_call(self, detector):
        detector.return_value = {"dominant_emotion": None}
        for query in ({}, {"textToAnalyze": ""}, {"textToAnalyze": "   "}):
            with self.subTest(query=query):
                response = self.client.get("/emotionDetector", query_string=query)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.get_data(as_text=True),
                                 "Invalid text! Please try again!")
        detector.assert_not_called()

    @patch("server.emotion_detector")
    def test_service_rejects_text(self, detector):
        detector.return_value = {"dominant_emotion": None}
        response = self.client.get(
            "/emotionDetector", query_string={"textToAnalyze": "example"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid text!", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
