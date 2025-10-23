# Quick Start Guide - Python Application

Get started in 3 minutes! ⚡

## Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements_python.txt
```

## Step 2: Run the Generator (10 seconds)

```bash
python main.py --records 1000
```

## Step 3: Check Output (5 seconds)

```bash
ls -lh output/
```

**Done! 🎉** You now have test data in `./output/`

---

## What Just Happened?

✅ Installed required Python packages (pandas, numpy)  
✅ Generated 1,000 test records with realistic data  
✅ Created CSV file with all 29 schema columns  
✅ Generated metadata and log files  

---

## Next Steps

### Generate More Records

```bash
# 5,000 records
python main.py --records 5000

# 15,000 records (default)
python main.py

# 50,000 records
python main.py --records 50000
```

### Try Different Scenarios

```bash
# List scenarios
python main.py --list-scenarios

# Graffiti cleaning focus
python main.py --scenario graffiti

# Maintenance focus
python main.py --scenario maintenance

# Development (1k records)
python main.py --scenario dev
```

### Specific KPI Codes

```bash
python main.py --kpi-codes GRAFFITI TRACKSIDE_CLEAN --records 3000
```

### Change Output Format

```bash
# Parquet format (faster for large files)
python main.py --format parquet

# Both CSV and Parquet
python main.py --format both
```

### Custom Output Location

```bash
python main.py --output ./my_test_data
```

---

## View Your Data

### Using Python

```bash
python -c "import pandas as pd; df = pd.read_csv('output/potential_failures_test_data_*.csv'); print(df.info()); print(df.head())"
```

### Using pandas in VS Code

```python
import pandas as pd

# Read the data
df = pd.read_csv('output/potential_failures_test_data_*.csv')

# View summary
print(df.info())
print(df.describe())

# View first few records
print(df.head())

# Check KPI distribution
print(df['KPIDescription'].value_counts())
```

---

## Programmatic Usage

```python
from config import DataGenerationConfig
from data_generator import DataGenerator

# Create configuration
config = DataGenerationConfig()
config.total_records = 5000

# Generate
generator = DataGenerator(config)
df = generator.run()

# Use the DataFrame
print(df.head())
```

---

## Common Commands

```bash
# Quick test (1k records)
python main.py --scenario dev

# Standard test (15k records)
python main.py

# Large dataset (50k records)
python main.py --scenario large

# Custom configuration
python main.py --records 10000 --duplicate-pct 0.25 --format both

# Debugging
python main.py --records 100 --log-level DEBUG
```

---

## Run Examples

```bash
# Run all example code
python examples.py

# Run specific example
python examples.py 1   # Basic usage
python examples.py 4   # Validation
python examples.py 9   # Analytics
```

---

## Output Files

After running, check `./output/` directory:

- **CSV/Parquet file**: Your generated test data
- **Metadata JSON**: Configuration and statistics
- **Log file**: Detailed generation logs

---

## Need Help?

- **Full documentation**: See `PYTHON_APP_README.md`
- **Examples**: Run `python examples.py`
- **CLI options**: Run `python main.py --help`
- **Configuration**: See `config.py`

---

## Troubleshooting

### "No module named 'pandas'"
```bash
pip install -r requirements_python.txt
```

### Want to customize sample data?
Edit `config.py` and modify:
- `SAMPLE_KPI_CODES`
- `SAMPLE_STATIONS`
- `SAMPLE_REPORTERS`

### Want to add more KPI codes?
```python
# In config.py, add to SAMPLE_KPI_CODES:
{
    'KPICode': 'YOUR_CODE',
    'KPIDescription': 'Your Description',
    'KPICategory': 'Your Category',
    'AnnualThresholdHours': 48,
    'IsKPI': 1
}
```

---

## Success! 🎉

You're now ready to generate test data!

**Most used command:**
```bash
python main.py --records 5000
```

**Check documentation for more options:**
- `PYTHON_APP_README.md` - Full guide
- `python main.py --help` - CLI reference
- `examples.py` - Code examples
