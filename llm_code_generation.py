from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from markdownify import markdownify as md

# Load once at module level for efficiency
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)
model.eval()
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def generate_solution_with_deepseek(question_data: dict) -> str:
    """
    Generate solution code for a LeetCode question using DeepSeek‑Coder.
    Args:
      question_data: {'content_html': HTML prompt, 'code': code template}
    Returns:
      Full code with filled solution.
    """
    prompt_text = md(question_data.get("content_html", ""))
    template = question_data.get("code", "")

    prompt = (
        "You are a code generation engine.\n\n"
        "Given the following LeetCode problem, generate only the Python solution code that completes the class definition.\n"
        "Do not add any explanations, comments, imports, print statements, or test cases.\n"
        "Your output must start with 'class Solution:' and include only valid Python code to solve the problem.\n\n"
        f"{prompt_text}\n\n"
        "Here is the function template:\n"
        f"{template}"
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    print('before generationg....')
    outputs = model.generate(
        **inputs,
        max_new_tokens=1280,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
    )
    print('after generation')
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Return the part including template and generated content
    return decoded.split(template, 1)[-1]

if __name__ == "__main__":
    sample = {
        "content_html": "<p>Given an array of integers <code>nums</code> and integer <code>target</code>, return indices of the two numbers that add to target.</p>",
        "code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        "
    }
    solution_body = generate_solution_with_deepseek(sample)
    print("### Generated body:\n", solution_body)