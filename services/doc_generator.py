from typing import List, Tuple
import requests

class DocGenerator:
    def __init__(self, llm_provider_url: str, llm_model: str, api_key: str):
        self.llm_provider_url = llm_provider_url
        self.llm_model = llm_model
        self.api_key = api_key

    def generate_summary_and_diagram(self, code_chunks: List[Tuple[str, str]], additional_instruction: str) -> str:
        prompt = self.build_prompt(code_chunks, additional_instruction)
        response_text = self.query_model(prompt)
        return response_text

    def build_prompt(self, code_chunks: List[Tuple[str, str]], additional_prompt) -> str:
        combined_code = "\n\n".join(f"# File: {path}\n{content}" for path, content in code_chunks)
        prompt = (
            "You are a skilled software documentation writer and systems analyst.\n\n"
            "You are given a set of source code files. Each file starts with a header: `# File: <filename>`.\n\n"
            "Your task is to generate comprehensive documentation that includes the following:\n"
            "## Architecture Overview\n"
            "- Describe the service purpose and core responsibilities.\n"
            "- Describe key components, modules, and how they interact.\n"
            "- Summarize inputs and outputs.\n\n"
            "## Flow Diagram\n"
            "- Create a Mermaid diagram (in code block) to visualize the high-level flow of logic or operations.\n"
            "- Use `graph TD` or `graph LR` to show processes and transitions.\n\n"
            "## Detailed Process Explanation\n"
            "- Describe the main processes step by step.\n"
            "- For each process, explain what it does, the decisions or conditions involved, and the purpose from a business logic perspective.\n"
            "- Avoid explaining every line of code.\n"
            "- Use clear, structured formatting: headings, bullet points, and Markdown.\n\n"
            f"{additional_prompt.upper()}\n\n"
            "The reader may be semi-technical (e.g., QA, PM, junior developer), so use clear and accessible language.\n\n"
            "Here is the code:\n"
            f"{combined_code}\n\n"
        )
        return prompt

    def query_model(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": self.llm_model,
            "messages": [
                {"role": "system", "content": "You are a skilled software documentation writer and systems analyst."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            self.llm_provider_url,
            json=body,
            headers=headers,
            timeout=120
        )

        if response.status_code != 200:
            print(response.text)
            raise Exception("server error")

        result = response.json()
        return result["choices"][0]["message"]["content"]
