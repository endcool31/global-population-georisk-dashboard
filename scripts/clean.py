import json
import os

def process_population_data(raw_path, output_path):
    data = {}
    with open(raw_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                year, pop = line.strip().split(':')
                data[int(year.strip())] = float(pop.strip())

    years = sorted(data.keys())
    values = [data[y] for y in years]

    mean_val = round(sum(values) / len(values), 2)
    base_val = data[years[0]]
    growth_rates = {
        f"{years[0]}-{y}": round(((data[y] - base_val) / base_val) * 100, 2)
        for y in years[1:]
    }
    n = years[-1] - years[0]
    cagr = round((((data[years[-1]] / base_val) ** (1 / n)) - 1) * 100, 3)

    result = {
        "source": "UN World Population Prospects (2024 Revision)",
        "unit": "Billion",
        "raw_series": data,
        "metrics": {
            "mean_population": mean_val,
            "cagr_2024_2100_percent": cagr,
            "period_growth_percent": growth_rates
        }
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(result, out_f, indent=2, ensure_ascii=False)

    print(f"Data processed successfully -> {output_path}")

if __name__ == "__main__":
    process_population_data('data/raw.txt', 'data/cleaned.json')