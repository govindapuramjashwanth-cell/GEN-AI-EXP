import unittest
from llm_client import LLMClient

class FakeProvider:
    model = "test-model"
    def generate(self, prompt):
        return {"response": "AI stands for Artificial Intelligence.", "input_tokens": 2, "output_tokens": 5}

class FakeLogger:
    def __init__(self):
        self.records = []
    def log_call(self, data):
        self.records.append(data)

class TestLLMClient(unittest.TestCase):
    def test_generate_and_log(self):
        logger = FakeLogger()
        client = LLMClient(FakeProvider(), logger)
        answer = client.generate("Explain AI")
        self.assertEqual(answer, "AI stands for Artificial Intelligence.")
        self.assertEqual(len(logger.records), 1)
        self.assertEqual(logger.records[0]["status"], "success")
        self.assertEqual(logger.records[0]["total_tokens"], 7)

if __name__ == "__main__":
    unittest.main()
