import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

console = Console()

OLLAMA_URL = "http://localhost:11434/api/generate"

# Models to benchmark
models = [
    "qwen3.5:0.8b",
    "qwen3.5:2b",
    "qwen3.5:4b",
    "qwen3.5:9b",
    "qwen3.5:27b",
    "qwen3.5:35b"
]

tests = {

"sheep_reasoning": {
"prompt": """
A farmer has 17 sheep. All but 9 die.
How many sheep remain?

Answer with only the number.
""",
"answers": ["9"]
},

"bat_ball_trick": {
"prompt": """
A bat and a ball cost $1.10 together.
The bat costs $1 more than the ball.
How much does the ball cost?

Answer only with the dollar value.
""",
"answers": ["0.05"]
},

"logic_syllogism": {
"prompt": """
All bloops are razzies.
All razzies are lazzies.

Are all bloops definitely lazzies?

Answer only YES or NO.
""",
"answers": ["yes"]
},

"math_multiply": {
"prompt": """
What is 23 × 17 ?

Answer with only the number.
""",
"answers": ["391"]
},

"math_sequence": {
"prompt": """
What is the next number in this sequence?

2, 4, 8, 16, 32, ?

Answer with only the number.
""",
"answers": ["64"]
},

"general_knowledge": {
"prompt": """
Which planet in the solar system currently has the most known moons?

Answer with the planet name only.
""",
"answers": ["saturn"]
},

"computer_science": {
"prompt": """
Which data structure follows FIFO (First In First Out)?

Answer with the name only.
""",
"answers": ["queue"]
},

"algorithm": {
"prompt": """
Which algorithm is commonly used to find the shortest path
in a graph with non-negative edge weights?

Answer with the algorithm name only.
""",
"answers": ["dijkstra"]
}

}


def run_prompt(model, prompt):

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 120000,
            "temperature": 0
        }
    }

    try:

        start = time.time()

        r = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        end = time.time()

        data = r.json()

        response = data.get("response", "").lower()

        latency = end - start

        tokens = data.get("eval_count", 0)

        tokens_per_sec = tokens / latency if latency > 0 else 0

        console.print(f"[cyan]Preview:[/cyan] {response[:80]}")

        return response, latency, tokens_per_sec

    except Exception as e:

        console.print(f"[red]Error calling {model}: {e}[/red]")

        return "", 0, 0


def evaluate(response, answers):

    response = response.lower()

    for a in answers:
        if a.lower() in response:
            return 1

    return 0


results = []

console.print("\n[bold cyan]Running Qwen Benchmark\n")

for model in models:

    for test_name, test in tests.items():

        console.print(f"[yellow]Testing {model} | {test_name}[/yellow]")

        response, latency, tps = run_prompt(model, test["prompt"])

        score = evaluate(response, test["answers"])

        results.append({

            "model": model,
            "task": test_name,
            "latency": round(latency, 2),
            "tokens_per_sec": round(tps, 2),
            "correct": score,
            "preview": response[:120].replace("\n", " ")

        })


# Create dataframe
df = pd.DataFrame(results)

df.to_csv("benchmark_results.csv", index=False)


# Leaderboard aggregation
leaderboard = df.groupby("model").agg({

    "correct": "sum",
    "tokens_per_sec": "mean",
    "latency": "mean"

}).reset_index()


# Score formula
leaderboard["score"] = leaderboard["correct"] * 20 + leaderboard["tokens_per_sec"]

leaderboard = leaderboard.sort_values("score", ascending=False)

leaderboard.to_csv("leaderboard.csv", index=False)


console.print("\n[bold green]Leaderboard\n")

table = Table()

table.add_column("Model")
table.add_column("Correct")
table.add_column("Avg Tokens/sec")
table.add_column("Score")

for _, row in leaderboard.iterrows():

    table.add_row(

        row["model"],
        str(row["correct"]),
        str(round(row["tokens_per_sec"], 2)),
        str(round(row["score"], 2))

    )

console.print(table)


# Chart
plt.figure()

leaderboard.plot(

    x="model",
    y="score",
    kind="bar",
    legend=False

)

plt.title("Qwen Model Benchmark Score")

plt.ylabel("Score")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig("leaderboard_chart.png")

console.print("\nSaved leaderboard_chart.png")


# Markdown report
with open("benchmark_report.md", "w") as f:

    f.write("# Qwen Model Benchmark\n\n")

    f.write(leaderboard.to_markdown(index=False))

console.print("Saved benchmark_report.md")