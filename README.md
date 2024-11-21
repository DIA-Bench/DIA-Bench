# Dynamic Intelligence Assessment Benchmark

<div align="center">
    <img width="550" alt="logo" src="https://github.com/user-attachments/assets/24e51155-375d-4831-82dd-6e13ef99abce">
</div>

## Description

The __DIA Benchmark Dataset__ is a benchmarking tool consisting of 150 dynamic question generators for the evaluation of the problem-solving capability of LLMs. It primarily focuses on CTF-style (Capture the Flag) challenges that require knowledge from the fields of mathematics, cryptography, cybersecurity, and computer science. The challenge generators were manually developed by industry experts and tested by multiple individuals to find errors and edge cases. The answers often consist of many characters and big numbers, making correct guessing highly unlikely. This repository contains the generated question and answer pairs that can be sent to AI models to run and assess the outputs. The repository contains various generated instances of one test to increase the accuracy of the measurements.

|File|K|Tests|
|-|-|-|
|[DIA-bench-1.json](./DIA-bench-1.json)|1|150|
|[DIA-bench-5.json](./DIA-bench-5.json)|5|750|
|[DIA-bench-10.json](./DIA-bench-10.json)|10|1,500|
|[DIA-bench-20.json](./DIA-bench-20.json)|20|3,000|
|[DIA-bench-100.json](./DIA-bench-100.json)|100|15,000|

## Architecture

The dataset was created manually by experts and the outputs validated for numberous generated instances of the questions. The following figure illustrates the generation process.

![architecture](https://github.com/user-attachments/assets/306f6f73-0a70-4a86-a5a8-668d932340a1)

## Evaluation

We tested 25 state-of-the-art LLM models on the DIA dataset through API calls, and ChatGPT-4o manually through its chat interface. Please note that these were tested on the `k=5` dataset and in November 2024.

<div align="center">
    <img alt="evaluation" src="https://github.com/user-attachments/assets/585ef918-b091-4795-b698-c9b5a4308db3">
</div>

## Testing

### 1. Download the repository

Via git
```bash
git clone https://github.com/DIA-Bench/DIA-Bench.git
```

Or by downloading a zipped version from __Code__ > __Download ZIP__

### 2. Configure up LLM provider

Choose a provider for testing the LLMs. Since most models are either large, or unavailable to download it's unlikely that you would be able to run it locally on your machine.

For testing GPT models we recommend https://openai.com/api/. For other models we used https://openrouter.ai/.

You will need to register, purchase credits and fill the necessary fields in the [DIA_bench_evalutor.py](DIA_bench_evalutor.py) script, including the tested model.

### 3. Run the benchmark

Run the benchmark and wait for the results. Please note that it may take a long time to run all tests.
```bash
python DIA_bench_evalutor.py
```

Your final oputput will contain the statistics for the model, including the Reliability Score (RS), the Confidence Index (CI), the number of correct answers, the number of skipped answers and the number of incorrect answers.
