# 🎯 START HERE

## Welcome! Choose Your Path

You have **TWO complete implementations**. Pick one based on your environment:

---

## 🟦 I'm Using Microsoft Fabric or Databricks

### ✅ Use: Jupyter Notebook Version

**Quick Start (5 minutes):**

1. **Open the notebook**
   ```
   generate_potential_failures_test_data.ipynb
   ```

2. **Modify Cell 2**
   ```python
   CONFIG['TOTAL_RECORDS'] = 1000  # Start small
   ```

3. **Run all cells**
   ```
   Ctrl+Shift+Enter (or Cell > Run All)
   ```

4. **Check output**
   ```
   Your Lakehouse table: test_potential_failures_validation
   ```

**📖 Next Steps:**
- Quick reference: `QUICK_REFERENCE.md`
- Full setup: `IMPLEMENTATION_GUIDE.md`
- 15 scenarios: `CONFIGURATION_EXAMPLES.md`

---

## 🟩 I'm Using VS Code or Local Python

### ✅ Use: Python Application Version

**Quick Start (3 minutes):**

1. **Install dependencies**
   ```bash
   pip install -r requirements_python.txt
   ```

2. **Run the generator**
   ```bash
   python main.py --scenario dev
   ```

3. **Check output**
   ```bash
   ls -lh output/
   ```

**📖 Next Steps:**
- Quick start: `QUICKSTART_PYTHON.md`
- Full guide: `PYTHON_APP_README.md`
- Run examples: `python examples.py`

---

## 🤔 Not Sure Which to Use?

### Use Jupyter Notebook If:
- ✅ You have Microsoft Fabric
- ✅ You have Databricks
- ✅ You need Lakehouse output
- ✅ You need SQL Server output
- ✅ You prefer interactive notebooks

### Use Python Application If:
- ✅ You want to run locally
- ✅ You prefer command-line tools
- ✅ You use VS Code or PyCharm
- ✅ You need programmatic API
- ✅ You don't have Spark/Databricks

**Still not sure?** Both do the same thing - both generate the exact same data!

---

## ⚡ Super Quick Commands

### Jupyter Notebook
```python
# In Cell 2:
CONFIG['TOTAL_RECORDS'] = 1000
# Then: Run all cells
```

### Python Application
```bash
python main.py --scenario dev
```

---

## 📚 Documentation Index

### For Jupyter Notebook:
1. `QUICK_REFERENCE.md` - Quick commands (3 min)
2. `IMPLEMENTATION_GUIDE.md` - Setup guide (15 min)
3. `CONFIGURATION_EXAMPLES.md` - 15 scenarios (10 min)
4. `TEST_DATA_GENERATOR_README.md` - Complete reference (20 min)

### For Python Application:
1. `QUICKSTART_PYTHON.md` - Quick start (3 min)
2. `PYTHON_APP_README.md` - Complete guide (15 min)
3. `PYTHON_APP_SUMMARY.md` - Overview (5 min)
4. Run: `python examples.py` - Working examples

### For Both:
- `README.md` - Project overview
- `README_COMPLETE.md` - Comprehensive guide
- `FINAL_DELIVERY_SUMMARY.md` - What you got

---

## 🎯 Common First Tasks

### Generate 1,000 test records

**Notebook:**
```python
CONFIG['TOTAL_RECORDS'] = 1000
# Run all cells
```

**Python:**
```bash
python main.py --scenario dev
```

### Generate 15,000 test records (default)

**Notebook:**
```python
# Use default CONFIG
# Run all cells
```

**Python:**
```bash
python main.py
```

### Generate for specific KPI codes

**Notebook:**
```python
CONFIG['SELECTED_KPI_CODES'] = ['GRAFFITI', 'STATION_CLEAN']
CONFIG['TOTAL_RECORDS'] = 5000
```

**Python:**
```bash
python main.py --kpi-codes GRAFFITI STATION_CLEAN --records 5000
```

---

## ❓ Quick FAQ

### Q: Do I need a database?
**A:** No! Both versions include sample data.

### Q: Can I run this locally?
**A:** Yes! Use the Python application version.

### Q: How many records can I generate?
**A:** 1,000 to 50,000+ records (both versions).

### Q: What data is included?
**A:** 10 KPI codes, 20 stations, all automatically.

### Q: Can I customize the data?
**A:** Yes! 20+ configuration options available.

### Q: Is this production-ready?
**A:** Yes! Both versions are fully tested and documented.

---

## 🏃 Ready? Start Now!

### If you're in Fabric/Databricks:
👉 **Open:** `generate_potential_failures_test_data.ipynb`

### If you're in VS Code:
👉 **Run:** `pip install -r requirements_python.txt && python main.py --scenario dev`

---

## 💡 Need Help?

### Jupyter Notebook:
- Quick help: `QUICK_REFERENCE.md`
- Detailed help: `IMPLEMENTATION_GUIDE.md`

### Python Application:
- Quick help: `QUICKSTART_PYTHON.md`
- Detailed help: `PYTHON_APP_README.md`

### Both:
- Complete guide: `README_COMPLETE.md`
- CLI help: `python main.py --help`

---

## ✅ What You'll Get

Both versions generate:
- ✅ All 29 schema columns
- ✅ Realistic test data
- ✅ Duration variety
- ✅ Financial year spanning
- ✅ Period crossings
- ✅ Duplicate scenarios
- ✅ Validated output

**Choose your version and start generating! 🚀**

---

**👉 Most Common Command:**

**Notebook:** Open notebook → Set `CONFIG['TOTAL_RECORDS'] = 1000` → Run all

**Python:** `python main.py --scenario dev`

**That's it! You're generating test data! 🎉**
