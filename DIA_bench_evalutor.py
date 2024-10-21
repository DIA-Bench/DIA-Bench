################### DIA-bench v1.0 evalutor script ###################################
# Title: Dynamic Intelligence Assessment:Benchmarking LLMs on the Road to AGI with a Focus on Model Confidence
# Script: This script serves as an example of how to evaluate the an LLM model using the DIA-bench dataset (evaluator script).
# The script can connect to any OpenAI compatible API. Please note that you may incur charges by using this and may be subject to throttling.


import json
import re
import time

import openai
from openai import OpenAI as Client
from tqdm import tqdm


api_key = '' # TODO Create an api key at your LLM provider.
host = '' # TODO Get the URL for the LLM provider (examples: https://openrouter.ai/api/v1, https://api.openai.com/v1/chat/completions)
model = '' # TODO name of the model to test. Please note that different providers may name the same model differently.
dia_file = 'DIA-bench-5.json' # TODO Specify the file with the generated tests in the DIA JSON format
dia_k = 5 # TODO The DIA-bench-5.json is created with k=5, resulting in a total of 750 questions for the evaluation.


class LLMChallengeEvaluator:
    def __init__(self, host, api_key, model):
        self.client = Client(
            base_url=host,
            api_key=api_key
        )
        self.model = model

    def handler(self, signum, frame):
        raise TimeoutError("Timeout: LLM took too long to respond.")

    def ask_llm(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=1.0,
                messages=[
                    {"role": "system", "content": "You are a Cybersecurity and math expert who can solve complex tasks."},
                    {"role": "user", "content": prompt},
                ]
            )
            result = ""
            for choice in response.choices:
                result += choice.message.content
            return result
        except openai.AuthenticationError:
            print(f'[*] ERROR: The API key is invalid. Please update the API key in the script file.')
            exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def clean_and_extract_xml(self, response):
        match = re.search(r'```?\s*xml\s*(<xml>.*?</xml>)\s*```?', response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1)
        return response  # Return the original response if no match is found

    def evaluate_responses(self, filename, k):
        # Load the JSON file with challenges
        try:

            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"[*] ERROR: Failed to decode JSON from the file '{filename}'. Please ensure it is a valid JSON.")
            return
        except Exception as e:
            print(f"[*] ERROR: Can not find the provided JSON file.")
            return        
        results = []
        log_data = []
        reliability_score = 0  # Track the Reliability Score
        template_confidence = {}  # Store confidence for each template

        # Track the number of correct, skipped, and wrong answers
        total_correct_answers = 0
        skipped_count = 0
        wrong_count = 0
        confidence_index = 0

        q_templates = {challenge['challenge']['Q template'] for challenge in data['questions']}

        # Progress bar without time display, dynamic updates to the bar
        progress_bar = tqdm(sorted(q_templates), desc="Reliability Score: 0", unit="template", leave=False, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')

        for q_template in progress_bar:
            correct_answers = 0
            total_instances = 0

            # Start measuring time for the current Q template
            start_time = time.time()

            # Process each instance for the current Q template
            for challenge in [c for c in data['questions'] if c['challenge']['Q template'] == q_template]:
                instance = challenge['challenge']['instance']
                description = challenge['challenge']['description']
                instructions = challenge['challenge']['instructions']
                full_prompt = f"{description}\n{instructions}"

                llm_response = self.ask_llm(full_prompt)
                llm_response = self.clean_and_extract_xml(llm_response) if llm_response else None
                correct_solution = challenge['solution']['challenge_solution']
                # Evaluate the response and calculate the score
                if llm_response == correct_solution:
                    correct_answers += 1  # Increment correct answers for confidence score
                    reliability_score += 1  # +1 to total score
                    total_correct_answers += 1  # Track correct answer
                    status = "Correct"
                elif llm_response == "<xml>I-DO-NOT-KNOW</xml>":
                    skipped_count += 1  # Track skipped answer
                    status = "Skipped"
                else:
                    reliability_score -= 2  # -2 to total Reliability Score
                    wrong_count += 1  # Track wrong answer
                    status = "Incorrect"

                total_instances += 1

                # Store the log data
                log_data.append({
                    "Q template": q_template,
                    "instance": instance,
                    "llm_response": llm_response,
                    "expected_solution": correct_solution,
                    "status": status,
                })

            # Calculate confidence index
            if correct_answers == total_instances:
                confidence_index += 1

            task_success_rate = (correct_answers / total_instances) * 100
            template_confidence[q_template] = task_success_rate

            # End measuring time for the current Q template
            end_time = time.time()
            solving_time = end_time - start_time

            # Update progress bar description to show the total dataset score and solving time
            progress_bar.set_description(f"Reliability Score: {reliability_score}")

            # Print the confidence score for the current Q template
            print(f" Q {q_template} Task Success Rate (TSR): {task_success_rate:.2f}% ({correct_answers}/{total_instances} correct) | Solving Time: {solving_time:.2f}s")

        # Save the log to a file
        self.save_log_file(log_data, template_confidence)

        # Display final dataset score and other statistics
        print(f"\n[*] Reliability Score (RS): {reliability_score/k:.2f} points")
        print(f"[*] Confidence Index (CI): {confidence_index}")
        print(f"[*] Total Correct Answers: {total_correct_answers}")
        print(f"[*] Total Skipped Answers: {skipped_count}")
        print(f"[*] Total Wrong Answers: {wrong_count}")

    # Function to save the LLM responses and actual solutions to a log file
    def save_log_file(self, log_data, template_confidence):
        with open('llm_responses_log.json', 'w', encoding='utf-8') as log_file:
            json.dump(log_data, log_file, ensure_ascii=False, indent=4)

        with open('confidence_scores_log.json', 'w', encoding='utf-8') as confidence_log:
            json.dump(template_confidence, confidence_log, ensure_ascii=False, indent=4)

        print("[*] Log has been saved to 'llm_responses_log.json'.")
        print("[*] Confidence scores have been saved to 'confidence_scores_log.json'.")



evaluator = LLMChallengeEvaluator(host=host, api_key=api_key, model=model)
evaluator.evaluate_responses(dia_file, dia_k)
