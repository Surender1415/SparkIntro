# Potential Failures Test Data Generator

## Overview

This Python notebook generates scalable, flexible test data for the `app_potential_failures` schema. It creates realistic task data with configurable parameters to test all edge cases and scenarios.

## Features

### ✅ Core Requirements
- **Schema Compliance**: All 29 columns populated according to the exact schema
- **KPI Code Coverage**: Covers all KPI codes from `bronze.fms_dimkpiclassification`
- **Configurable Selection**: Can generate data for all codes or selected subset
- **Duration Variety**: Short, medium, long, and very long tasks for each KPI group
- **Financial Year Spanning**: At least 1 task per KPI code crosses FY boundary
- **Staggered Dates**: Tests threshold rollover scenarios (24h, 48h, 100h thresholds)
- **Period Crossing**: Tasks span period boundaries for testing
- **Station Distribution**: Tasks distributed across all stations (excluding NULL sections)
- **Scalable Volume**: Default 15k records, easily adjustable
- **Status**: All tasks in COMP status
- **Date Range**: Two-year period starting 25/05/25

### 🎯 Advanced Features
- **Duplicate Testing**: Configurable percentage of overlapping tasks by station/time
- **Frequency Weights**: Adjust task distribution by KPI code
- **Status Progression**: Optional simulation of WAPPR → APPR → COMP transitions
- **Non-KPI Tasks**: Optional generation of non-KPI code tasks
- **Period Integration**: Joins with `core_dimdate` for rail period and period week
- **Validation Output**: Writes to Lakehouse first for validation before SQL Server

## Configuration

All configuration is done through the `CONFIG` dictionary in Cell 2:

### Key Configuration Flags

```python
CONFIG = {
    # Data Volume
    'TOTAL_RECORDS': 15000,  # Scale up/down as needed
    
    # KPI Code Selection
    'USE_ALL_KPI_CODES': True,  # False to use specific codes
    'SELECTED_KPI_CODES': [],  # e.g., ['GRAFFITI', 'TRACKSIDE_CLEAN']
    
    # Task Frequency by KPI Code
    'KPI_FREQUENCY_WEIGHTS': {},  # e.g., {'GRAFFITI': 2.0, 'LIFT_MAINT': 0.5}
    
    # Duration Distribution
    'DURATION_DISTRIBUTION': {
        'short': 0.40,    # 40% short (1-24 hrs)
        'medium': 0.35,   # 35% medium (1-7 days)
        'long': 0.20,     # 20% long (7-30 days)
        'very_long': 0.05 # 5% very long (30-90 days)
    },
    
    # Duplicate Testing
    'DUPLICATE_TEST_PERCENTAGE': 0.10,  # 10% overlapping tasks
    'DUPLICATE_TIME_WINDOW_HOURS': 4,   # Within 4 hours
    
    # Output Destinations
    'OUTPUT_TO_LH': True,   # Lakehouse for validation
    'OUTPUT_TO_SQL': False, # SQL Server (enable after validation)
    
    # Optional Features
    'SIMULATE_STATUS_PROGRESSION': False,  # Create history files
    'INCLUDE_NON_KPI_TASKS': False,        # Add non-KPI tasks
}
```

## Usage Scenarios

### Scenario 1: Generate Full Test Dataset (Default)
```python
# Use default configuration
# Run all cells
```
Generates 15k records covering all KPI codes with standard distribution.

### Scenario 2: Focus on Specific KPI Codes
```python
CONFIG['USE_ALL_KPI_CODES'] = False
CONFIG['SELECTED_KPI_CODES'] = ['GRAFFITI', 'TRACKSIDE_CLEAN', 'ESCALATOR_REPAIR']
CONFIG['TOTAL_RECORDS'] = 5000
```
Generates 5k records for only the specified KPI codes.

### Scenario 3: Test High-Volume Scenarios
```python
CONFIG['TOTAL_RECORDS'] = 50000
CONFIG['KPI_FREQUENCY_WEIGHTS'] = {
    'GRAFFITI': 3.0,  # 3x normal frequency
    'STATION_CLEAN': 2.0,  # 2x normal frequency
}
```
Generates 50k records with weighted distribution.

### Scenario 4: Test Duplicate Detection
```python
CONFIG['DUPLICATE_TEST_PERCENTAGE'] = 0.25  # 25% duplicates
CONFIG['DUPLICATE_TIME_WINDOW_HOURS'] = 2   # Very close timing
```
Generates dataset optimized for duplicate detection testing.

### Scenario 5: Test Status Progression
```python
CONFIG['SIMULATE_STATUS_PROGRESSION'] = True
CONFIG['STATUS_PROGRESSION_STEPS'] = ['WAPPR', 'APPR', 'COMP']
```
Creates 3 snapshot files showing status progression for backload testing.

### Scenario 6: Small Test Dataset
```python
CONFIG['TOTAL_RECORDS'] = 1000
CONFIG['USE_ALL_KPI_CODES'] = True
```
Quick generation for development/debugging.

## Data Quality Checks

The notebook includes built-in validation:

1. **Schema Compliance**: All required columns present with correct data types
2. **Date Logic**: ReportedDate < LoggedOn < ScheduledFor < Finished
3. **Duration Variety**: Mix of short/medium/long tasks per KPI code
4. **FY Spanning**: At least one task per KPI crosses financial year
5. **Period Distribution**: Tasks spread across multiple periods
6. **Station Coverage**: All stations represented
7. **Duplicate Detection**: Overlapping tasks identified

## Output

### Lakehouse Output (Validation)
- **Table**: `test_potential_failures_validation`
- **Format**: Delta table
- **Purpose**: Validate data quality before SQL Server load

### SQL Server Output (Production)
- **Table**: `app_potential_failures_test` (configurable)
- **Schema**: Exact match to `app_potential_failures`
- **Purpose**: Production testing environment

### CSV Files
- Fallback if Lakehouse/SQL unavailable
- Status progression snapshots (if enabled)

## Workflow

1. **Configure**: Set parameters in CONFIG dictionary
2. **Generate**: Run all cells in notebook
3. **Validate**: Check Lakehouse table for data quality
4. **Review**: Examine validation output and statistics
5. **Export**: Enable SQL Server output if validation passes
6. **Iterate**: Adjust configuration and regenerate as needed

## Testing Edge Cases

The generator automatically handles:

### Financial Year Testing
- ✅ Tasks spanning FY boundary (starts before, ends after)
- ✅ Staggered start/end for threshold rollover testing
- ✅ Tasks consuming full annual threshold

### Duration Edge Cases
- ✅ Very short tasks (< 1 hour)
- ✅ Medium duration tasks (days)
- ✅ Long duration tasks (weeks)
- ✅ Very long tasks (months)

### Period Testing
- ✅ Tasks within single period
- ✅ Tasks crossing period boundaries
- ✅ Period week calculation accuracy

### Duplicate Scenarios
- ✅ Same station, overlapping time windows
- ✅ Configurable time proximity
- ✅ By-station duplicate grouping

## Database Connections

### Required Tables
- `bronze.fms_dimkpiclassification` - KPI code definitions
- `customer_success.dimStation` - Station master data
- `core_dimdate` - Date dimension for period info
- `customer_success.app_potential_failures` - Reference examples

### Connection Setup
Update these in CONFIG:
```python
'SQL_SERVER': 'your_server.database.windows.net',
'SQL_DATABASE': 'your_database',
'SQL_USERNAME': 'your_username',
'SQL_PASSWORD': 'your_password',  # Use Key Vault in production
```

## Customization Examples

### Example 1: Graffiti-Heavy Dataset
```python
CONFIG['KPI_FREQUENCY_WEIGHTS'] = {'GRAFFITI': 5.0}
CONFIG['DURATION_DISTRIBUTION'] = {
    'short': 0.70,  # Most graffiti tasks are short
    'medium': 0.25,
    'long': 0.05,
    'very_long': 0.0
}
```

### Example 2: Test Threshold Rollover
```python
CONFIG['TOTAL_RECORDS'] = 5000
CONFIG['ENSURE_FY_SPANNING_TASKS'] = True
CONFIG['STAGGERED_ROLLOVER_TASKS'] = True
# Focus on KPI codes with 24/48/100 hour thresholds
CONFIG['SELECTED_KPI_CODES'] = ['GRAFFITI', 'TRACKSIDE_CLEAN', 'ESCALATOR_REPAIR']
```

### Example 3: Period Boundary Testing
```python
CONFIG['TOTAL_RECORDS'] = 3000
# Adjust duration to ensure period crossings
CONFIG['DURATION_DISTRIBUTION'] = {
    'short': 0.1,
    'medium': 0.3,
    'long': 0.4,
    'very_long': 0.2  # More long tasks = more period crossings
}
```

## Performance

- **Generation Speed**: ~10-15 seconds for 15k records
- **Lakehouse Write**: ~30-60 seconds for 15k records
- **SQL Server Write**: ~2-5 minutes for 15k records (batch insert)
- **Memory Usage**: < 500MB for typical datasets

## Troubleshooting

### Issue: Cannot connect to database
**Solution**: Use sample data mode (automatically enabled on connection failure)

### Issue: Period data incorrect
**Solution**: Verify `core_dimdate` table has data for date range

### Issue: Too many/few records
**Solution**: Adjust `CONFIG['TOTAL_RECORDS']` and verify weights sum correctly

### Issue: Missing KPI codes
**Solution**: Check `bronze.fms_dimkpiclassification` table or add to sample data

### Issue: Validation fails
**Solution**: Review validation output, check schema compliance, verify date logic

## Best Practices

1. **Always validate in Lakehouse first** before SQL Server
2. **Start small** (1k records) to verify configuration
3. **Use frequency weights** to simulate realistic workload
4. **Enable duplicate testing** for robust testing
5. **Generate multiple datasets** for different test scenarios
6. **Document configuration** used for each test dataset
7. **Version control** configuration for reproducibility

## Schema Reference

```
ColumnName           DataType    Description
-------------------- ----------- ----------------------------------
TaskId               nvarchar    Unique task identifier
RecordID             nvarchar    Unique record identifier
Instruction_Code     nvarchar    Work instruction code
Building             nvarchar    Station code
BuildingName         nvarchar    Station name
LocationName         nvarchar    Specific location within station
ShortDescription     nvarchar    Brief task description
LongDescription      nvarchar    Detailed task description
Reporter             nvarchar    Person who reported issue
ReporterEmail        nvarchar    Reporter's email
Notes                nvarchar    Additional notes
ReportedDate         datetime2   When issue was reported
DueBy                datetime2   Due date
ScheduledFor         datetime2   Scheduled start date
Finished             datetime2   Completion date
Status               nvarchar    Task status (all COMP)
LoggedBy             nvarchar    Who logged the task
LoggedOn             datetime2   When task was logged
ModifiedOn           datetime2   Last modification date
SLAStatus            nvarchar    SLA compliance status
CreatedTimestamp     datetime2   Record creation timestamp
LastUploaded         datetime2   Last upload timestamp
IsCurrent            bit         Current record flag
Period               nvarchar    Rail period
PeriodWeek           bigint      Period week number
PeriodYear           bigint      Period year
StationSection       nvarchar    Station section/area
KPIDescription       nvarchar    KPI description
KPICategory          nvarchar    KPI category
```

## Support

For issues or questions:
1. Check validation output for errors
2. Review configuration settings
3. Verify database connectivity
4. Check sample data is loaded correctly
5. Review this README for relevant scenario

## Version History

- **v1.0**: Initial release with all core features
  - 15k scalable records
  - All KPI codes coverage
  - Duration variety
  - FY spanning logic
  - Period crossing
  - Duplicate testing
  - Lakehouse + SQL output
  - Status progression (optional)
