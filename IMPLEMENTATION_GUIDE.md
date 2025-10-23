# Implementation Guide - Potential Failures Test Data Generator

## Quick Start (5 Minutes)

### Step 1: Open Notebook
1. Open `generate_potential_failures_test_data.ipynb` in Fabric/Databricks
2. Attach to your Spark cluster

### Step 2: Basic Configuration
```python
# Cell 2 - Modify these values only:
CONFIG['TOTAL_RECORDS'] = 1000  # Start small
CONFIG['OUTPUT_TO_LH'] = True
CONFIG['OUTPUT_TO_SQL'] = False  # Keep False until validated
```

### Step 3: Run
1. Run all cells (Ctrl+Shift+Enter or Cell > Run All)
2. Wait ~30 seconds
3. Check output table in Lakehouse

### Step 4: Validate
```sql
-- Run in SQL endpoint
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT KPIDescription) as kpi_codes,
    COUNT(DISTINCT Building) as stations,
    MIN(LoggedOn) as start_date,
    MAX(Finished) as end_date
FROM test_potential_failures_validation
```

### Step 5: Scale Up
Once validated, increase record count and enable SQL output:
```python
CONFIG['TOTAL_RECORDS'] = 15000
CONFIG['OUTPUT_TO_SQL'] = True  # Now safe to enable
```

---

## Detailed Implementation

### Environment Setup

#### Microsoft Fabric
1. Create new Notebook in your workspace
2. Copy notebook cells into new notebook
3. Update connection settings (usually pre-configured)
4. Run

#### Databricks
1. Import notebook
2. Attach to cluster with Spark 3.3+
3. Update JDBC connection strings
4. Run

#### Local/Standalone
1. Install dependencies: `pip install -r requirements.txt`
2. Install Spark locally
3. Update all connection strings
4. Configure authentication
5. Run

### Database Configuration

#### Option 1: Fabric Native (Recommended)
```python
# No additional configuration needed
# Fabric automatically handles Lakehouse connections
```

#### Option 2: SQL Server Direct
```python
CONFIG['SQL_SERVER'] = 'your_server.database.windows.net'
CONFIG['SQL_DATABASE'] = 'your_database'
CONFIG['SQL_USERNAME'] = 'your_username'
CONFIG['SQL_PASSWORD'] = 'your_password'  # Use Key Vault!
```

#### Option 3: Azure Key Vault (Production)
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net", credential=credential)

CONFIG['SQL_PASSWORD'] = client.get_secret("sql-password").value
```

### Data Source Configuration

The notebook requires access to these tables:

1. **bronze.fms_dimkpiclassification**
   - Purpose: KPI code definitions and thresholds
   - Required columns: KPICode, KPIDescription, KPICategory, AnnualThresholdHours, IsKPI
   
2. **customer_success.dimStation**
   - Purpose: Station master data
   - Required columns: StationCode, StationName, Section
   
3. **core_dimdate**
   - Purpose: Date dimension for period calculations
   - Required columns: Date, RailPeriod, RailPeriodWeek, FiscalYear
   
4. **customer_success.app_potential_failures** (optional)
   - Purpose: Reference for data patterns
   - Used for: Understanding real data structure

#### Fallback Mode
If tables are unavailable, the notebook uses sample data:
```python
# Automatically activated on connection failure
# Uses predefined sample KPI codes and stations
# Still generates valid test data
```

---

## Configuration Strategies

### Strategy 1: Start Simple
**Goal**: Get familiar with the tool

```python
CONFIG['TOTAL_RECORDS'] = 1000
CONFIG['USE_ALL_KPI_CODES'] = True
# Leave everything else as default
```

**Result**: 1k records covering all scenarios

### Strategy 2: Focused Testing
**Goal**: Test specific KPI codes in detail

```python
CONFIG['TOTAL_RECORDS'] = 5000
CONFIG['USE_ALL_KPI_CODES'] = False
CONFIG['SELECTED_KPI_CODES'] = ['GRAFFITI', 'TRACKSIDE_CLEAN']
CONFIG['DUPLICATE_TEST_PERCENTAGE'] = 0.20
```

**Result**: 5k records for 2 KPI codes with 20% duplicates

### Strategy 3: Production-Like
**Goal**: Realistic data distribution

```python
CONFIG['TOTAL_RECORDS'] = 20000
CONFIG['KPI_FREQUENCY_WEIGHTS'] = {
    'GRAFFITI': 2.5,
    'STATION_CLEAN': 2.0,
    # ... based on actual production frequency
}
```

**Result**: 20k records mimicking production patterns

### Strategy 4: Edge Cases
**Goal**: Test all boundary conditions

```python
CONFIG['TOTAL_RECORDS'] = 15000
CONFIG['ENSURE_FY_SPANNING_TASKS'] = True
CONFIG['STAGGERED_ROLLOVER_TASKS'] = True
CONFIG['DURATION_DISTRIBUTION'] = {
    'short': 0.25,
    'medium': 0.25,
    'long': 0.25,
    'very_long': 0.25  # Equal distribution
}
```

**Result**: Maximum edge case coverage

---

## Validation Checklist

After generation, verify:

### ✅ Data Quality
- [ ] Correct number of records generated
- [ ] All KPI codes represented
- [ ] All stations represented
- [ ] Date range correct (2025-05-25 onwards)
- [ ] All Status = 'COMP'
- [ ] No NULL values in required fields

### ✅ Business Logic
- [ ] ReportedDate < LoggedOn < ScheduledFor < Finished
- [ ] Duration variety present (short/medium/long)
- [ ] At least 1 FY-spanning task per KPI code
- [ ] Period values calculated correctly
- [ ] Period crossings present

### ✅ Test Scenarios
- [ ] Duplicate tasks exist (if configured)
- [ ] Long-duration tasks span periods
- [ ] FY rollover tasks start before and end after FY end
- [ ] Station distribution is reasonable

### Validation Queries

```sql
-- 1. Basic counts
SELECT 
    COUNT(*) as total,
    COUNT(DISTINCT KPIDescription) as kpi_count,
    COUNT(DISTINCT Building) as station_count
FROM test_potential_failures_validation;

-- 2. Duration distribution
SELECT 
    CASE 
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 24 THEN 'Short'
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 168 THEN 'Medium'
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 720 THEN 'Long'
        ELSE 'Very Long'
    END as Duration_Category,
    COUNT(*) as Count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as Percentage
FROM test_potential_failures_validation
GROUP BY 
    CASE 
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 24 THEN 'Short'
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 168 THEN 'Medium'
        WHEN DATEDIFF(hour, LoggedOn, Finished) <= 720 THEN 'Long'
        ELSE 'Very Long'
    END;

-- 3. Period crossings
SELECT 
    COUNT(*) as tasks_crossing_periods
FROM test_potential_failures_validation
WHERE Period != (
    SELECT TOP 1 Period 
    FROM core_dimdate 
    WHERE Date = CAST(Finished AS DATE)
);

-- 4. Potential duplicates
SELECT 
    Building,
    CAST(LoggedOn AS DATE) as LogDate,
    DATEPART(HOUR, LoggedOn) as LogHour,
    COUNT(*) as TaskCount
FROM test_potential_failures_validation
GROUP BY Building, CAST(LoggedOn AS DATE), DATEPART(HOUR, LoggedOn)
HAVING COUNT(*) > 1
ORDER BY TaskCount DESC;

-- 5. FY spanning tasks
SELECT 
    KPIDescription,
    COUNT(*) as FY_Spanning_Tasks
FROM test_potential_failures_validation
WHERE (
    YEAR(LoggedOn) < YEAR(Finished)
    OR (YEAR(LoggedOn) = YEAR(Finished) - 1 AND MONTH(LoggedOn) < 4 AND MONTH(Finished) >= 4)
)
GROUP BY KPIDescription;
```

---

## Troubleshooting

### Issue: "Table not found" error

**Cause**: Reference tables not accessible

**Solution**:
1. Verify table names and schema
2. Check permissions
3. Use sample data mode (automatic fallback)

### Issue: "Out of memory" error

**Cause**: Record count too high for cluster

**Solution**:
```python
CONFIG['TOTAL_RECORDS'] = 10000  # Reduce
# Or scale up cluster
```

### Issue: Period values incorrect

**Cause**: core_dimdate not available or missing dates

**Solution**:
1. Check date range in core_dimdate
2. Extend date dimension if needed
3. Use fallback period calculation (automatic)

### Issue: No duplicates generated

**Cause**: Not enough tasks or percentage too low

**Solution**:
```python
CONFIG['DUPLICATE_TEST_PERCENTAGE'] = 0.20  # Increase
CONFIG['TOTAL_RECORDS'] = 10000  # More records
```

### Issue: SQL Server write fails

**Cause**: Connection or permissions issue

**Solution**:
1. Verify connection string
2. Check credentials
3. Verify table creation permissions
4. Use Lakehouse output instead

### Issue: Generation too slow

**Cause**: Large record count or complex configuration

**Solutions**:
- Reduce record count for testing
- Use more powerful cluster
- Disable status progression if not needed
- Reduce duplicate percentage

---

## Best Practices

### 1. Incremental Approach
Start small, validate, scale up:
```
1k records → validate → 5k records → validate → 15k records → production
```

### 2. Configuration Version Control
Save configurations with descriptive names:
```python
# graffiti_testing_v1.py
CONFIG = {
    'TOTAL_RECORDS': 5000,
    'SELECTED_KPI_CODES': ['GRAFFITI'],
    # ...
}
```

### 3. Document Test Scenarios
Keep a log of what each dataset tests:
```
dataset_001: Default configuration (15k records)
dataset_002: Graffiti focus (5k records, 30% duplicates)
dataset_003: FY rollover testing (6k records, FY spanning)
```

### 4. Validation Before Production
Always validate in Lakehouse before SQL Server:
```python
# Step 1: Generate and validate
CONFIG['OUTPUT_TO_LH'] = True
CONFIG['OUTPUT_TO_SQL'] = False

# Step 2: After validation passes
CONFIG['OUTPUT_TO_SQL'] = True
```

### 5. Use Quick Config Script
For common scenarios:
```bash
python quick_config.py --scenario graffiti --records 10000 > my_config.py
```

### 6. Regular Backups
Keep generated datasets for regression testing:
```python
# Add timestamp to table name
from datetime import datetime
CONFIG['LH_TABLE_NAME'] = f"test_data_{datetime.now().strftime('%Y%m%d_%H%M')}"
```

---

## Advanced Usage

### Custom KPI Frequency Distribution
Based on production analysis:
```python
# Analyze production data first
production_frequency = {
    'GRAFFITI': 450,  # tasks per month
    'STATION_CLEAN': 320,
    'TRACKSIDE_CLEAN': 280,
    # ...
}

# Convert to weights
total = sum(production_frequency.values())
CONFIG['KPI_FREQUENCY_WEIGHTS'] = {
    k: v / total for k, v in production_frequency.items()
}
```

### Seasonal Patterns
Simulate seasonal variations:
```python
# Summer: more cleaning
# Winter: more maintenance
# Adjust duration distribution accordingly
```

### Multi-Dataset Testing Suite
Generate complementary datasets:
```python
# Dataset 1: Normal operations (15k)
# Dataset 2: High duplicate scenario (5k)
# Dataset 3: FY boundary focus (6k)
# Dataset 4: Long duration focus (4k)
# Total: 30k records covering all scenarios
```

---

## Performance Tuning

### For Large Datasets (50k+)

1. **Increase Cluster Size**
   - More memory
   - More cores

2. **Batch Processing**
   ```python
   # Generate in batches
   for batch in range(5):
       CONFIG['TOTAL_RECORDS'] = 10000
       # Adjust random seed per batch
       # Append to same table
   ```

3. **Optimize Writes**
   ```python
   # Use partition by Period
   spark_df.write.partitionBy("Period").saveAsTable(...)
   ```

4. **Disable Optional Features**
   ```python
   CONFIG['SIMULATE_STATUS_PROGRESSION'] = False
   CONFIG['DUPLICATE_TEST_PERCENTAGE'] = 0.05  # Reduce
   ```

---

## Integration with Testing Pipeline

### Example: Automated Test Data Refresh

```python
# orchestration_pipeline.py

def refresh_test_data():
    # 1. Generate data
    run_notebook("generate_potential_failures_test_data")
    
    # 2. Validate
    validation_results = validate_data()
    
    # 3. If valid, promote to test environment
    if validation_results['is_valid']:
        promote_to_test_env()
    else:
        send_alert(validation_results['errors'])

# Schedule: Weekly on Sunday nights
```

---

## Support and Maintenance

### Regular Updates
- Review KPI codes quarterly
- Update station list as needed
- Adjust frequency weights based on production patterns
- Refresh test datasets monthly

### Monitoring
- Track generation time
- Monitor data quality metrics
- Validate against production patterns
- Review test coverage

---

## Summary

This test data generator provides:
- ✅ Scalable data generation (1k to 50k+ records)
- ✅ Comprehensive KPI coverage
- ✅ Realistic business scenarios
- ✅ Edge case testing
- ✅ Configurable distribution
- ✅ Validation workflows
- ✅ Production-ready output

**Start simple, validate thoroughly, scale confidently.**
