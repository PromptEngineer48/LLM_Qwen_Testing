# Qwen Local Model Benchmark (0.8B → 35B)

A simple **automated benchmark framework** to compare different sizes of Qwen models running locally with **Ollama**.

This project tests how model capability scales from **0.8B → 35B parameters** by running the same set of reasoning, math, logic, and knowledge tasks across all models.

The script automatically:

* Runs prompts across all models
* Measures **latency**
* Measures **tokens/sec**
* Evaluates **correct answers**
* Produces a **leaderboard**
* Generates **charts and reports**

This is useful for:

* Comparing **small vs large LLMs**
* Creating **YouTube demonstrations**
* Understanding **performance vs intelligence tradeoffs**
* Evaluating **local AI setups**

---

# Models Tested

The benchmark evaluates the following Qwen models:

```
qwen3.5:0.8b
qwen3.5:2b
qwen3.5:4b
qwen3.5:9b
qwen3.5:27b
qwen3.5:35b
```

These are run locally using **Ollama**.

---

# Benchmark Tasks

The benchmark runs **8 short tasks** covering different reasoning abilities.

| Task                    | Skill Tested                  |
| ----------------------- | ----------------------------- |
| Sheep puzzle            | Logical reasoning             |
| Bat & Ball              | Cognitive trap                |
| Logic syllogism         | Deductive reasoning           |
| Multiplication          | Arithmetic                    |
| Sequence prediction     | Pattern recognition           |
| Planet with most moons  | General knowledge             |
| FIFO data structure     | Computer science fundamentals |
| Shortest path algorithm | Algorithm knowledge           |

Each task has a **deterministic answer** so scoring can be automated.

---

# Installation

Install Python dependencies:

```bash
pip install requests rich pandas matplotlib seaborn
```

---

# Install Models

Download the Qwen models with Ollama:

```bash
ollama pull qwen3.5:0.8b
ollama pull qwen3.5:2b
ollama pull qwen3.5:4b
ollama pull qwen3.5:9b
ollama pull qwen3.5:27b
ollama pull qwen3.5:35b
```

You can confirm installation using:

```bash
ollama list
```

---

# Run the Benchmark

Execute:

```bash
python qwen_benchmark.py
```

The script will automatically:

1. Send each prompt to each model
2. Measure response speed
3. Evaluate correctness
4. Generate reports

---

# Example Console Output

```
Running Qwen Benchmark

Testing qwen3.5:0.8b | sheep_reasoning
Preview: the answer is 9

Testing qwen3.5:2b | sheep_reasoning
Preview: 9 sheep remain

Testing qwen3.5:4b | sheep_reasoning
Preview: 9
```

At the end a **leaderboard** is printed:

```
Model          Correct   Avg Tokens/sec   Score
------------------------------------------------
qwen3.5:35b        8          25.1        185
qwen3.5:27b        8          22.8        182
qwen3.5:9b         7          38.5        178
qwen3.5:4b         6          52.3        172
qwen3.5:2b         5          63.4        168
qwen3.5:0.8b       3          85.7        145
```

---

# Generated Outputs

After the benchmark completes, several files are generated:

```
benchmark_results.csv
leaderboard.csv
leaderboard_chart.png
benchmark_report.md
```

### benchmark_results.csv

Raw results for each model and test.

### leaderboard.csv

Aggregated model performance.

### leaderboard_chart.png

Visual comparison chart.

### benchmark_report.md

Markdown report suitable for GitHub.

---

# Scoring Method

Each model is evaluated on:

* **Correct answers**
* **Average tokens/sec**
* **Latency**

Final score:

```
score = (correct_answers * 20) + tokens_per_sec
```

This rewards both **accuracy** and **speed**.

---

# Example Chart

The benchmark generates a chart like this:

```
Qwen Model Benchmark Score
```

```
0.8B   ███████
2B     █████████
4B     ███████████
9B     █████████████
27B    ███████████████
35B    █████████████████
```

This visually shows how **model capability scales with size**.

---

# Monitoring GPU Usage (Optional)

While running benchmarks on a GPU machine you can monitor usage:

```bash
watch -n 1 nvidia-smi
```

This shows which model is currently loaded.

---

# Project Structure

```
.
├── qwen_benchmark.py
├── benchmark_results.csv
├── leaderboard.csv
├── leaderboard_chart.png
├── benchmark_report.md
└── README.md
```

---

# Why This Benchmark Exists

Many developers ask:

* How much better is **9B vs 4B**?
* Is **27B worth the GPU cost?**
* How capable are **sub-1B models**?

This project helps answer those questions using **simple reproducible tests**.

---

# Possible Extensions

Future improvements could include:

* More reasoning tasks
* Code execution tests
* Long-context evaluation
* Multi-turn conversations
* LLM-as-a-judge scoring

---

# License

MIT License

---

# Author

Built for experimenting with **local LLM benchmarking using Ollama and Qwen models**.
