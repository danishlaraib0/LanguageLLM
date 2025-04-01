import requests
import re
import json

class AIGuardrail:
    def __init__(self, model="phi4", api_url="http://localhost:11434/api/generate"):
        self.model = model
        self.api_url = api_url

    def _generate_prompt(self, user_input):
        """
        Creates the prompt for the API request.
        """
        prompt = f"Your are an ai guardrail. Your task is to check whether your given query is safe or not from an ethical perspective. Give output in json with key 'label' (SAFE and UNSAFE) and 'reason' (4-5 words only). Query is: {user_input}"
        return prompt

    def _send_request(self, prompt):
        """
        Sends the API request and returns the response.
        """
        response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()

    def _extract_json_from_response(self, response):
        """
        Extracts the JSON data from the response using regex.
        """
        json_pattern = r'```json\n(\{.*\})\n```'
        match = re.search(json_pattern, response.get('response', ''), re.DOTALL)

        if match:
            json_str = match.group(1)
            try:
                json_data = json.loads(json_str)
                return json_data
            except json.JSONDecodeError:
                return None
        return None

    def guardrails(self, user_input):
        """
        Main method to perform the guardrail check on user input.
        Returns the parsed JSON with 'label' and 'reason' or None if the response is invalid.
        """
        prompt = self._generate_prompt(user_input)
        response = self._send_request(prompt)
        return self._extract_json_from_response(response)

    def extract_label(self, label_dict):
        """
        Extracts the 'label' field from the JSON response.
        """
        return label_dict.get('label', None)

    def extract_reason(self, reason_dict):
        """
        Extracts the 'reason' field from the JSON response.
        """
        return reason_dict.get('reason', None)


# Example usage
# if __name__ == "__main__":
#     guardrail = AIGuardrail()
#     user_input = "fuck you"
#     result = guardrail.guardrails(user_input)
#     if result:
#         label = guardrail.extract_label(result)
#         reason = guardrail.extract_reason(result)
#         print(f"Label: {label}, Reason: {reason}")
#     else:
#         print("Invalid response from AI guardrail.")
