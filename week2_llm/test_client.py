import unittest

from llm_client import LLMClient


class FakeProvider:
    def generate(self, prompt):
        return "AI stands for Artificial Intelligence."


class TestLLMClient(unittest.TestCase):
    def test_generate(self):
        client = LLMClient(FakeProvider())
        result = client.generate("Explain AI")
        self.assertEqual(
            result,
            "AI stands for Artificial Intelligence.",
        )


if __name__ == "__main__":
    unittest.main()
