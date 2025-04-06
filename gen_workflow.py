import yaml

with open("cph_symbols.txt") as f:
    symbols = [line.strip() for line in f if line.strip() and not line.startswith("#")]

workflow = {
    "name": "Fetch Copenhagen Stocks",
    "on": {
        "schedule": [{"cron": "*/5 7-15 * * 1-5"}],  # Every 5 mins, Mon–Fri, UTC time (09–17 DK)
        "workflow_dispatch": {}
    },
    "jobs": {
        "fetch": {
            "runs-on": "ubuntu-latest",
            "strategy": {
                "matrix": {
                    "symbol": symbols
                }
            },
            "steps": [
                {"name": "Sleep random seconds to spread load", "run": "sleep $(( RANDOM % 180 ))"},
                {"name": "Checkout repo", "uses": "actions/checkout@v3"},
                {
                    "name": "Set up Python",
                    "uses": "actions/setup-python@v4",
                    "with": {"python-version": "3.10"}
                },
                {"name": "Install dependencies", "run": "pip install yfinance pandas"},
                {
                    "name": "Fetch stock data",
                    "run": "python fetch_stock.py ${{ matrix.symbol }}"
                },
                {
                    "name": "Upload data",
                    "uses": "actions/upload-artifact@v4",
                    "with": {
                        "name": "${{ matrix.symbol }}-data",
                        "path": "data/"
                    }
                }
            ]
        }
    }
}

with open(".github/workflows/fetch_stocks.yml", "w") as f:
    yaml.dump(workflow, f, sort_keys=False)

print("✅ Workflow generated successfully.")
