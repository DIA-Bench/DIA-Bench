import json
from datasets import load_dataset


with open('DIA-Benchmark-k100.json') as f:
    dataset = json.load(f)
    
for i, q in enumerate(dataset['questions']):
    # Challenge
    assert 'challenge' in q, f"Missing 'challenge' field in question {i}: \n{q}"
    challenge = q['challenge']
    assert isinstance(challenge['template_id'], int), f"Invalid 'template_id' field in question {i}:\n{q}"
    assert isinstance(challenge['instance'], int), f"Invalid 'instance' field in question {i}:\n{q}"
    assert isinstance(challenge['level'], str), f"Invalid 'level' field in question {i}:\n{q}"
    assert isinstance(challenge['category'], str), f"Invalid 'instance' field in question {i}:\n{q}"
    assert isinstance(challenge['adversarial'], bool), f"Invalid 'adversarial' field in question {i}:\n{q}"
    assert isinstance(challenge['description'], str), f"Invalid 'description' field in question {i}:\n{q}"
    assert isinstance(challenge['instructions'], str), f"Invalid 'instructions' field in question {i}:\n{q}"
    
    # Solution
    assert 'solution' in q, f"Missing 'solution' field in question {i}: \n{q}"
    solution = q['solution']
    assert isinstance(solution['challenge_solution'], str), f"Invalid 'challenge_solution' field in question {i}:\n{q}"
    assert isinstance(solution['solution_explanation'], str), f"Invalid 'solution_explanation' field in question {i}:\n{q}"
    

dataset = load_dataset("json", data_files="DIA-Benchmark-k100.json", field="questions")
