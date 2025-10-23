# Test Data Generator for Potential Failures

This repository contains a comprehensive, scalable Python notebook for generating test data for the `app_potential_failures` table.

## 📋 Overview

The `generate_test_data_potential_failures.ipynb` notebook generates realistic test data with full control over:
- **Data volume** (~15k records, fully configurable)
- **KPI code selection** (all or specific codes)
- **Task durations** (short, medium, long distributions)
- **Edge cases** (year-spanning, downtime thresholds, period boundaries)
- **Duplicate testing** (overlapping task groups)
- **Output destinations** (Lakehouse for validation, SQL Server for production)

## 🚀 Quick Start

### 1. Configuration

Open the notebook and modify the `CONFIG` dictionary in the first configuration cell:

```python
CONFIG = {
    'TOTAL_RECORDS': 15000,          # Adjust record count
    'START_DATE': '2025-05-25',      # GTS started EL
    'PERIOD_YEARS': 2,               # Generate over 2 years
    
    'USE_ALL_KPI_CODES': True,       # Or set to False and filter
    'KPI_CODES_FILTER': [],          # e.g., ['GRAFFITI', 'TRACKSIDE']
    
    'OUTPUT_MODE': 'LAKEHOUSE',      # Start with LAKEHOUSE, then SQL_SERVER
    # ... more options
}
```

### 2. Run the Notebook

Execute all cells sequentially. The notebook will:
1. Load reference data (KPI codes, stations, date dimensions)
2. Generate test data with all edge cases
3. Validate the output
4. Write to Lakehouse or SQL Server

### 3. Review & Deploy

1. **Initial run**: Set `OUTPUT_MODE` to `'LAKEHOUSE'` to validate
2. **Review**: Check the generated data in Lakehouse
3. **Deploy**: Change to `'SQL_SERVER'` and update JDBC connection details
4. **Re-run**: Execute to write to SQL Server

## 🎯 Features

### Core Requirements ✅
- ✅ **Configurable volume**: ~15k records (dial up/down)
- ✅ **All KPI codes**: From `bronze.fms_dimkpiclassification`
- ✅ **Selectable codes**: Filter to specific KPI codes
- ✅ **Various durations**: Short (1-24h), Medium (25-120h), Long (121-720h)
- ✅ **All COMP status**: All tasks completed
- ✅ **Station distribution**: Across all stations (excluding NULL sections)
- ✅ **Period integration**: Joins with `core_dimdate` for period/week info

### Edge Cases ✅
- ✅ **Year-spanning jobs**: At least 1 per KPI code crossing FY boundary
- ✅ **Downtime thresholds**: Jobs testing 24, 48, 100 hour thresholds with rollover
- ✅ **Period boundaries**: 30% of jobs cross period boundaries
- ✅ **Random timing**: Start and end times randomized over 2-year period
- ✅ **Date range**: Starting from 25/05/25 (GTS started EL)

### Testing Features ✅
- ✅ **Overlapping groups**: Configurable groups with close start/end dates
- ✅ **Duplicate detection**: Same station + KPI + time window
- ✅ **Frequency control**: Weight distribution per KPI code

### Optional Features ✅
- ✅ **Status history**: Generate WAPPR → APPR → COMP progression files
- ✅ **Non-KPI tasks**: Include non-KPI code tasks (configurable ratio)

## 📊 Configuration Options

### Data Volume
```python
'TOTAL_RECORDS': 15000,  # Target number of records
```

### KPI Code Selection
```python
'USE_ALL_KPI_CODES': True,  # Use all codes
# OR
'USE_ALL_KPI_CODES': False,
'KPI_CODES_FILTER': ['GRAFFITI', 'TRACKSIDE'],  # Specific codes
```

### Frequency Weights
```python
'KPI_FREQUENCY_WEIGHTS': {
    'GRAFFITI': 2.0,      # 2x more records
    'TRACKSIDE': 1.5,     # 1.5x more records
    # Empty dict = equal distribution
}
```

### Duration Categories
```python
'DURATION_CATEGORIES': {
    'short': {'min_hours': 1, 'max_hours': 24, 'weight': 0.4},    # 40% short
    'medium': {'min_hours': 25, 'max_hours': 120, 'weight': 0.4}, # 40% medium
    'long': {'min_hours': 121, 'max_hours': 720, 'weight': 0.2},  # 20% long
}
```

### Edge Cases
```python
'YEAR_SPANNING_PER_KPI': 1,              # 1 year-spanning job per KPI
'DOWNTIME_THRESHOLD_TESTS': True,        # Test 24, 48, 100 hour thresholds
'PERIOD_BOUNDARY_CROSSING_RATIO': 0.3,   # 30% cross period boundaries
```

### Duplicate Testing
```python
'CREATE_OVERLAPPING_GROUPS': True,       # Enable overlapping groups
'OVERLAPPING_GROUPS_COUNT': 50,          # Number of groups
'OVERLAP_WINDOW_HOURS': 6,               # Tasks within 6 hours overlap
```

### Output
```python
'OUTPUT_MODE': 'LAKEHOUSE',  # or 'SQL_SERVER'
'LAKEHOUSE_PATH': '/lakehouse/default/Tables/test_potential_failures',
'SQL_TABLE_NAME': 'customer_success.app_potential_failures_test',
```

### Optional Features
```python
'GENERATE_STATUS_HISTORY': False,  # Create status progression files
'INCLUDE_NON_KPI_CODES': False,    # Include non-KPI tasks
'NON_KPI_RATIO': 0.1,              # 10% non-KPI if enabled
```

## 🔍 Validation

The notebook includes comprehensive validation:
- ✅ All required columns present
- ✅ No null values in critical columns
- ✅ Valid date sequences (Reported → Scheduled → Finished)
- ✅ Year-spanning task count verification
- ✅ Status distribution check
- ✅ Unique ID verification
- ✅ Record count vs target

## 📁 Output Schema

The generated data matches the exact schema of `app_potential_failures`:

| Column | Data Type | Description |
|--------|-----------|-------------|
| TaskId | nvarchar | Unique task identifier |
| RecordID | nvarchar | Unique record identifier |
| Instruction_Code | nvarchar | KPI code from dimkpiclassification |
| Building | nvarchar | Station code |
| BuildingName | nvarchar | Station name |
| LocationName | nvarchar | Location/city |
| ShortDescription | nvarchar | Brief task description |
| LongDescription | nvarchar | Detailed description with duration info |
| Reporter | nvarchar | Person who reported the task |
| ReporterEmail | nvarchar | Reporter's email |
| Notes | nvarchar | Additional notes (includes edge case markers) |
| ReportedDate | datetime2 | When task was reported |
| DueBy | datetime2 | SLA deadline based on KPI threshold |
| ScheduledFor | datetime2 | Scheduled start time |
| Finished | datetime2 | Completion time |
| Status | nvarchar | Task status (all COMP by default) |
| LoggedBy | nvarchar | Who logged the task |
| LoggedOn | datetime2 | When task was logged |
| ModifiedOn | datetime2 | Last modification time |
| SLAStatus | nvarchar | Within SLA / Near SLA / SLA Breach |
| CreatedTimestamp | datetime2 | Record creation time |
| LastUploaded | datetime2 | Last upload timestamp |
| IsCurrent | bit | Current record flag (always 1) |
| Period | nvarchar | Rail period (from core_dimdate) |
| PeriodWeek | bigint | Period week number |
| PeriodYear | bigint | Period year |
| StationSection | nvarchar | Station section/depot |
| KPIDescription | nvarchar | KPI description |
| KPICategory | nvarchar | KPI category |

## 🎨 Usage Examples

### Example 1: Generate 20k Records with All KPI Codes
```python
CONFIG = {
    'TOTAL_RECORDS': 20000,
    'USE_ALL_KPI_CODES': True,
    'OUTPUT_MODE': 'LAKEHOUSE',
}
```

### Example 2: Focus on Graffiti and Trackside Cleaning
```python
CONFIG = {
    'TOTAL_RECORDS': 5000,
    'USE_ALL_KPI_CODES': False,
    'KPI_CODES_FILTER': ['GRAFFITI', 'TRACKSIDE'],
    'KPI_FREQUENCY_WEIGHTS': {
        'GRAFFITI': 2.0,      # More graffiti tasks
        'TRACKSIDE': 1.0,
    },
}
```

### Example 3: Test Long-Duration Tasks
```python
CONFIG = {
    'TOTAL_RECORDS': 10000,
    'DURATION_CATEGORIES': {
        'short': {'min_hours': 1, 'max_hours': 24, 'weight': 0.1},
        'medium': {'min_hours': 25, 'max_hours': 120, 'weight': 0.2},
        'long': {'min_hours': 121, 'max_hours': 1440, 'weight': 0.7},  # 70% long tasks
    },
}
```

### Example 4: Generate Status History for Backload Testing
```python
CONFIG = {
    'TOTAL_RECORDS': 15000,
    'GENERATE_STATUS_HISTORY': True,  # Creates WAPPR → APPR → COMP files
    'OUTPUT_MODE': 'LAKEHOUSE',
}
```

## 🔧 Customization

### Adding Custom KPI Codes
If using mock data, edit the `create_mock_reference_data()` function to add custom KPI codes.

### Changing Date Logic
Modify the period calculation in the `get_period_info()` function to match your organization's fiscal calendar.

### Custom Descriptions
Update the `SHORT_DESCRIPTIONS` dictionary to add custom task descriptions per KPI code.

## 📝 Notes

- **Database Connection**: The notebook uses Fabric Spark by default. Update connection details for custom SQL connections.
- **Mock Data**: If database tables aren't accessible, the notebook falls back to mock reference data.
- **Reproducibility**: Uncomment the random seed lines to generate identical datasets across runs.
- **Performance**: Generating 15k records typically takes 1-2 minutes.

## 🛠️ Troubleshooting

### Issue: "Reference data not found"
**Solution**: The notebook will automatically create mock data. Review and update if needed.

### Issue: "JDBC connection failed"
**Solution**: Update the JDBC connection string in the SQL Server output cell with your credentials.

### Issue: "Record count mismatch"
**Solution**: This is expected due to mandatory edge cases. The variance check allows up to 10%.

### Issue: "Validation errors"
**Solution**: Review the validation output. Most issues are informational and don't prevent data generation.

## 📚 Reference

- **Source Table**: `customer_success.app_potential_failures`
- **KPI Codes**: `bronze.fms_dimkpiclassification`
- **Stations**: `customer_success.dimStation`
- **Date Dimension**: `core_dimdate`
- **Example Notebook**: [Fabric Notebook 5141d3c8](https://app.fabric.microsoft.com/groups/dfff67d4-ccfe-45de-a776-d32e2773291f/synapsenotebooks/5141d3c8-6bcb-4972-97ed-4ce46560ee3f?experience=fabric-developer)

## 🤝 Contributing

To customize this generator:
1. Fork the notebook
2. Update configuration as needed
3. Test with `OUTPUT_MODE = 'LAKEHOUSE'`
4. Deploy with `OUTPUT_MODE = 'SQL_SERVER'`

---

**Generated**: 2025-10-23  
**Version**: 1.0  
**Branch**: cursor/generate-scalable-test-data-for-potential-failures-b160
