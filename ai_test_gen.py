from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
print("THE API KEY IS:", os.getenv("OPENAI_API_KEY"))
client = OpenAI()

def generate_tests(code):
    prompt = f"""
    You are an AI that generates unit tests.
    Given the following code:
    {code}

    Generate:
    - Unit tests
    - Edge cases
    - Invalid input tests
    Output only Python code.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    with open("data/code_example.py", "r") as f:
        code = f.read()
    print(generate_tests(code))
