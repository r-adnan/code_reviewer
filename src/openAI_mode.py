from openai import OpenAI

class openAI_module():

    def __init__(self, ast_data)
    self.ast_data = ast_data

    def analyze_code_with_openai(self):
        response = OpenAI.Chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps with Python code analysis."},
                {"role": "user", "content": "Here is the AST data: ..."}
            ]
        )

print(response.choices[0].message.content)