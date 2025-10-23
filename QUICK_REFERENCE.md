# Quick Reference Card

## 🚀 5-Minute Quick Start

```python
# 1. Open notebook
generate_potential_failures_test_data.ipynb

# 2. Modify Cell 2
CONFIG['TOTAL_RECORDS'] = 1000

# 3. Run all cells (Ctrl+Shift+Enter)

# 4. Check output
# → Lakehouse table: test_potential_failures_validation
```

---

## 🎯 Common Configurations

### Scenario 1: Default Test Data
```python
CONFIG['TOTAL_RECORDS'] = 15000  # Standard size
# Everything else: use defaults
```

### Scenario 2: Specific KPI Testing
```python
CONFIG['USE_ALL_KPI_CODES'] = False
CONFIG['SELECTED_KPI_CODES'] = ['GRAFFITI', 'TRACKSIDE_CLEAN']
CONFIG['TOTAL_RECORDS'] = 5000
```

### Scenario 3: Duplicate Testing
```python
CONFIG['DUPLICATE_TEST_PERCENTAGE'] = 0.30  # 30% duplicates
CONFIG['DUPLICATE_TIME_WINDOW_HOURS'] = 2   # Within 2 hours
```

### Scenario 4: Large Dataset
```python
CONFIG['TOTAL_RECORDS'] = 50000  # Performance testing
```

---

## 🔧 Key Configuration Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `TOTAL_RECORDS` | 15000 | Number of records to generate |
| `USE_ALL_KPI_CODES` | True | Use all KPI codes vs selected |
| `SELECTED_KPI_CODES` | [] | Specific codes to use |
| `DUPLICATE_TEST_PERCENTAGE` | 0.10 | % of overlapping tasks |
| `OUTPUT_TO_LH` | True | Write to Lakehouse |
| `OUTPUT_TO_SQL` | False | Write to SQL Server |
| `ENSURE_FY_SPANNING_TASKS` | True | Tasks crossing FY boundary |

---

## 📊 Validation Queries

### Quick Check
```sql
SELECT COUNT(*) FROM test_potential_failures_validation;
```

### Coverage Check
```sql
SELECT 
    COUNT(DISTINCT KPIDescription) as kpi_count,
    COUNT(DISTINCT Building) as station_count,
    MIN(LoggedOn) as start_date,
    MAX(Finished) as end_date
FROM test_potential_failures_validation;
```

### Duration Distribution
```sql
SELECT 
    CASE 
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 24 THEN 'Short'
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 168 THEN 'Medium'
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 720 THEN 'Long'
        ELSE 'Very Long'
    END as Duration,
    COUNT(*) as Count
FROM test_potential_failures_validation
GROUP BY 
    CASE 
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 24 THEN 'Short'
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 168 THEN 'Medium'
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 720 THEN 'Long'
        ELSE 'Very Long'
    END;
```

---

## 🛠️ CLI Tool Usage

### List Scenarios
```bash
python quick_config.py --list
```

### Generate Configuration
```bash
python quick_config.py --scenario graffiti
```

### Save to File
```bash
python quick_config.py --scenario realistic --output my_config.py
```

### Custom Record Count
```bash
python quick_config.py --scenario threshold --records 10000
```

---

## 📁 File Structure

```
/workspace/
├── generate_potential_failures_test_data.ipynb  ← Main notebook
├── TEST_DATA_GENERATOR_README.md                ← Full documentation
├── IMPLEMENTATION_GUIDE.md                      ← Setup guide
├── CONFIGURATION_EXAMPLES.md                    ← 15 scenarios
├── PROJECT_SUMMARY.md                           ← Overview
├── QUICK_REFERENCE.md                           ← This file
├── quick_config.py                              ← CLI tool
└── requirements.txt                             ← Dependencies
```

---

## ⚡ Workflow

```
1. Configure  → Set CONFIG parameters in Cell 2
2. Generate   → Run all cells
3. Validate   → Check Lakehouse table
4. Review     → Examine validation output
5. Scale      → Increase record count if needed
6. Deploy     → Enable SQL Server output
```

---

## 🎯 Pre-built Scenarios

| Scenario | Records | Focus | Use Case |
|----------|---------|-------|----------|
| `default` | 15k | All KPIs | General testing |
| `graffiti` | 10k | Cleaning | Specific KPI testing |
| `maintenance` | 8k | Repairs | Maintenance testing |
| `threshold` | 5k | Rollover | FY boundary testing |
| `duplicates` | 5k | Overlaps | Duplicate detection |
| `dev` | 1k | Quick test | Development |
| `large` | 50k | Volume | Performance testing |
| `realistic` | 20k | Production | Realistic simulation |

**Full list**: See `CONFIGURATION_EXAMPLES.md`

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Table not found | Use sample data mode (automatic) |
| Out of memory | Reduce `TOTAL_RECORDS` |
| No duplicates | Increase `DUPLICATE_TEST_PERCENTAGE` |
| SQL write fails | Use Lakehouse output first |
| Slow generation | Reduce records or scale cluster |

---

## ✅ Validation Checklist

- [ ] Correct number of records generated
- [ ] All KPI codes present (or selected ones)
- [ ] All stations represented
- [ ] Date range correct (starts 25/05/25)
- [ ] All Status = 'COMP'
- [ ] Duration variety present
- [ ] Period values calculated
- [ ] No NULL values in required fields
- [ ] FY-spanning tasks exist
- [ ] Duplicates present (if configured)

---

## 📊 Duration Categories

| Category | Hours | Days | Use Case |
|----------|-------|------|----------|
| Short | 1-24 | < 1 day | Quick fixes |
| Medium | 25-168 | 1-7 days | Standard tasks |
| Long | 169-720 | 7-30 days | Complex work |
| Very Long | 721-2160 | 30-90 days | Major projects |

**Default Distribution**: 40% short, 35% medium, 20% long, 5% very long

---

## 🎨 Customization Tips

### Change Distribution
```python
CONFIG['DURATION_DISTRIBUTION'] = {
    'short': 0.50,    # 50% short
    'medium': 0.30,   # 30% medium
    'long': 0.15,     # 15% long
    'very_long': 0.05 # 5% very long
}
```

### Weight KPI Codes
```python
CONFIG['KPI_FREQUENCY_WEIGHTS'] = {
    'GRAFFITI': 3.0,  # 3x normal
    'STATION_CLEAN': 2.0,  # 2x normal
}
```

### Adjust Date Range
```python
CONFIG['START_DATE'] = '2025-01-01'
CONFIG['END_DATE'] = '2027-12-31'
```

---

## 📈 Expected Performance

| Records | Generation Time | Memory | Output Time |
|---------|----------------|--------|-------------|
| 1,000 | ~5 sec | ~50 MB | ~10 sec |
| 5,000 | ~8 sec | ~100 MB | ~20 sec |
| 15,000 | ~15 sec | ~200 MB | ~60 sec |
| 50,000 | ~60 sec | ~500 MB | ~3 min |

*Times approximate, vary by cluster size*

---

## 🎯 Best Practices

1. ✅ **Start small** (1k records) to verify config
2. ✅ **Validate in Lakehouse** before SQL Server
3. ✅ **Use pre-built scenarios** for common cases
4. ✅ **Check validation output** after generation
5. ✅ **Document configurations** for reproducibility
6. ✅ **Scale gradually** (1k → 5k → 15k → 50k)
7. ✅ **Version control** successful configs

---

## 🔗 Documentation Links

- **Full Guide**: `TEST_DATA_GENERATOR_README.md`
- **Setup**: `IMPLEMENTATION_GUIDE.md`
- **Examples**: `CONFIGURATION_EXAMPLES.md`
- **Overview**: `PROJECT_SUMMARY.md`

---

## 💡 Pro Tips

- Use `quick_config.py --list` to see all scenarios
- Start with `dev` scenario (1k records) for testing
- Enable `SIMULATE_STATUS_PROGRESSION` for history testing
- Set `DUPLICATE_TEST_PERCENTAGE = 0` to disable duplicates
- Use `KPI_FREQUENCY_WEIGHTS` for realistic distributions

---

## 🏆 Quick Wins

### Generate 1k test records in 1 minute:
```python
CONFIG['TOTAL_RECORDS'] = 1000
# Run all cells
```

### Test specific KPI in 2 minutes:
```python
CONFIG['USE_ALL_KPI_CODES'] = False
CONFIG['SELECTED_KPI_CODES'] = ['GRAFFITI']
CONFIG['TOTAL_RECORDS'] = 2000
# Run all cells
```

### Create production-like dataset in 5 minutes:
```bash
python quick_config.py --scenario realistic
# Copy to notebook, run all cells
```

---

## 🎉 You're Ready!

**Choose your path:**

- 👶 **Beginner**: Use `dev` scenario (1k records)
- 🎓 **Intermediate**: Use `default` scenario (15k records)
- 🚀 **Advanced**: Customize configuration
- 💪 **Expert**: Modify generation logic

**Start generating test data now!**
