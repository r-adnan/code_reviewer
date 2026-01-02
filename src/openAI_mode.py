from openai import OpenAI

response = OpenAI.Chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that helps with Python code analysis."},
        {"role": "user", "content": "Here is the AST data: ..."}
    ]
)

print(response.choices[0].message.content)