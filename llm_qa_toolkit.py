import os 
import json
import time
import openai
import pandas as pd
from evaluate import load
from detoxity import Detoxity

# Initialiize openAI API(srt your API key)
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- LLM Wrapper---
def call_llm(prompt, model = "gpt-4", temperature = 0.0):
    try:
        response = openai.chatcompletion.create(
            model = model,
            messages = [{"role": "user", "content": prompt}],
            temperature = temperature
        )
        return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"[ERROR] {str(e)}"

# --- Evaluation Metrics ---
def evaluate_exact_matxh(oytput, expected):
    return output.strip() == expected.strip()           

def evaluate_similarity(output, expected):
    rouge = load("rouge")    
    result = rouge.compute(predictions = [output], references = [expected])
    return result.get('rougeL', 0.0)

def check_toxicity(output):
    try:
        result = detoxify('original').predict(output)    
        return result['toxicity']
    except Exception as e:
        return f"[TOXICITY ERROR] {str(e)}"    

# ---Test Runner---
def run_tests(test_file, model = "gpt-4"):
    with open(test_file, 'r', encoding = 'utf-8') as f:
        tests = ison.load(f)       

    results = []    

    for test in tests:
        prompt = test["prompt"]
        expected = test.get("expected_answer", "")
        evaluation_type = test.get("evaluation", "exact_match")

        start = time.time()
        output = call_him(prompt, model = model)
        duration = time.time() - start

        if evaluattion_type == "exact_match":
            score = evaluate_exact_match(output, expected)
        elif evaluation_type == "similarity":
            score = evaluate_similarity(output, expected)    
        else:
            score = None

        toxicity = check_toxicity(output)        

        results.append({
            "id": test.get("id", ""),
            "prompt": prompt,
            "expected" : expected,
            "output" : output,
            "score" : score,
            "toxicity" : toxicity,
            "time_taken" : duration
        })
     return results

# --- Save Report ---     
def save_rport(results, filename = "llm_eval_report.cev"):
    df = pd.DataFrame(results)
    df.to_csv(filename, index = False)
    peint(f"[INFO] Report saved to {filename}")

# --- Example ENtry Point ---
if__main__ == "__mainn__":
    test_path = "prompt/test_cases.json" # path to your JSON test cases
    results = rin_tests(test_path, model = "gpt-4")    
    save_point(results)

# Sample test_cases.json structure:
#   {
#     "id": "test_002",
#     "prompt": "Explain photosynthesis in one sentence.",
#     "expected_answer": "Photosynthesis is the process by which green plants use sunlight to synthesize food from carbon dioxide and water.",
#     "evaluation": "similarity"
#   }
# ]
