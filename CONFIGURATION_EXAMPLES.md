# Configuration Examples - Quick Reference

## Quick Start Configurations

Copy and paste these into the CONFIG dictionary (Cell 2) for common scenarios.

---

## 1. Default Test Dataset (Recommended Start)

```python
CONFIG = {
    'TOTAL_RECORDS': 15000,
    'START_DATE': '2025-05-25',
    'END_DATE': '2027-05-25',
    'USE_ALL_KPI_CODES': True,
    'SELECTED_KPI_CODES': [],
    'INCLUDE_NON_KPI_TASKS': False,
    'DURATION_DISTRIBUTION': {
        'short': 0.40,
        'medium': 0.35,
        'long': 0.20,
        'very_long': 0.05
    },
    'ENSURE_FY_SPANNING_TASKS': True,
    'DUPLICATE_TEST_PERCENTAGE': 0.10,
    'OUTPUT_TO_LH': True,
    'OUTPUT_TO_SQL': False,
}
```
**Use Case**: General testing with good coverage of all scenarios.

---

## 2. Graffiti & Cleaning Focus

```python
CONFIG = {
    'TOTAL_RECORDS': 10000,
    'USE_ALL_KPI_CODES': False,
    'SELECTED_KPI_CODES': ['GRAFFITI', 'TRACKSIDE_CLEAN', 'STATION_CLEAN'],
    'KPI_FREQUENCY_WEIGHTS': {
        'GRAFFITI': 3.0,
        'TRACKSIDE_CLEAN': 2.0,
        'STATION_CLEAN': 1.5
    },
    'DURATION_DISTRIBUTION': {
        'short': 0.60,  # Cleaning tasks are typically short
        'medium': 0.30,
        'long': 0.08,
        'very_long': 0.02
    },
}
```
**Use Case**: Testing cleaning-specific KPIs with realistic short durations.

---

## 3. Maintenance & Repair Focus

```python
CONFIG = {
    'TOTAL_RECORDS': 8000,
    'USE_ALL_KPI_CODES': False,
    'SELECTED_KPI_CODES': ['ESCALATOR_REPAIR', 'LIFT_MAINTENANCE', 'PLATFORM_REPAIR'],
    'DURATION_DISTRIBUTION': {
        'short': 0.20,
        'medium': 0.40,  # Repairs take moderate time
        'long': 0.30,
        'very_long': 0.10  # Some complex repairs
    },
}
```
**Use Case**: Testing maintenance KPIs with longer durations.

---

## 4. Threshold Rollover Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 5000,
    'USE_ALL_KPI_CODES': False,
    'SELECTED_KPI_CODES': ['GRAFFITI', 'TRACKSIDE_CLEAN', 'ESCALATOR_REPAIR'],  # 24h, 48h, 100h thresholds
    'ENSURE_FY_SPANNING_TASKS': True,
    'STAGGERED_ROLLOVER_TASKS': True,
    'DURATION_DISTRIBUTION': {
        'short': 0.30,
        'medium': 0.40,
        'long': 0.25,
        'very_long': 0.05
    },
}
```
**Use Case**: Testing annual threshold rollover (24h, 48h, 100h limits).

---

## 5. Duplicate Detection Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 5000,
    'DUPLICATE_TEST_PERCENTAGE': 0.30,  # 30% duplicates
    'DUPLICATE_TIME_WINDOW_HOURS': 2,   # Very close timing
    'USE_ALL_KPI_CODES': True,
}
```
**Use Case**: Heavy duplicate scenarios to test detection logic.

---

## 6. Period Boundary Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 8000,
    'DURATION_DISTRIBUTION': {
        'short': 0.10,
        'medium': 0.20,
        'long': 0.40,     # More long tasks
        'very_long': 0.30  # More very long tasks
    },
}
```
**Use Case**: Many tasks crossing period boundaries.

---

## 7. Financial Year Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 6000,
    'START_DATE': '2025-02-01',  # Start before FY end
    'END_DATE': '2027-05-31',    # Cover multiple FY
    'ENSURE_FY_SPANNING_TASKS': True,
    'STAGGERED_ROLLOVER_TASKS': True,
    'DURATION_DISTRIBUTION': {
        'short': 0.25,
        'medium': 0.30,
        'long': 0.30,
        'very_long': 0.15  # More long tasks to span FY
    },
}
```
**Use Case**: Testing FY boundary crossing and threshold rollover.

---

## 8. Small Development Dataset

```python
CONFIG = {
    'TOTAL_RECORDS': 1000,
    'USE_ALL_KPI_CODES': True,
    'DUPLICATE_TEST_PERCENTAGE': 0.05,
    'OUTPUT_TO_LH': True,
}
```
**Use Case**: Quick testing during development.

---

## 9. Large Volume Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 50000,
    'USE_ALL_KPI_CODES': True,
    'DURATION_DISTRIBUTION': {
        'short': 0.45,
        'medium': 0.35,
        'long': 0.15,
        'very_long': 0.05
    },
}
```
**Use Case**: Performance testing with large datasets.

---

## 10. Status Progression Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 3000,
    'SIMULATE_STATUS_PROGRESSION': True,
    'STATUS_PROGRESSION_STEPS': ['WAPPR', 'APPR', 'COMP'],
    'OUTPUT_TO_LH': True,
}
```
**Use Case**: Testing backload with status changes over time.

---

## 11. Specific Stations Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 5000,
    'USE_ALL_KPI_CODES': True,
    'EXCLUDE_NULL_SECTIONS': True,  # No depots
}
```
**Use Case**: Only station-based tasks (no depot tasks).

---

## 12. Non-KPI Tasks Included

```python
CONFIG = {
    'TOTAL_RECORDS': 10000,
    'USE_ALL_KPI_CODES': True,
    'INCLUDE_NON_KPI_TASKS': True,
    'NON_KPI_TASK_PERCENTAGE': 0.15,  # 15% non-KPI
}
```
**Use Case**: Mixed dataset with non-KPI tasks.

---

## 13. Single KPI Code Deep Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 5000,
    'USE_ALL_KPI_CODES': False,
    'SELECTED_KPI_CODES': ['GRAFFITI'],
    'DURATION_DISTRIBUTION': {
        'short': 0.33,
        'medium': 0.33,
        'long': 0.33,
        'very_long': 0.01
    },
    'DUPLICATE_TEST_PERCENTAGE': 0.20,
}
```
**Use Case**: Deep testing of a single KPI code with all scenarios.

---

## 14. Realistic Production Simulation

```python
CONFIG = {
    'TOTAL_RECORDS': 20000,
    'USE_ALL_KPI_CODES': True,
    'KPI_FREQUENCY_WEIGHTS': {
        'GRAFFITI': 2.5,
        'STATION_CLEAN': 2.0,
        'TRACKSIDE_CLEAN': 1.8,
        'LIGHTING_FIX': 1.5,
        'ESCALATOR_REPAIR': 1.2,
        'LIFT_MAINTENANCE': 1.0,
        'PLATFORM_REPAIR': 0.8,
        'SIGNAGE_UPDATE': 0.5,
    },
    'DURATION_DISTRIBUTION': {
        'short': 0.50,
        'medium': 0.30,
        'long': 0.15,
        'very_long': 0.05
    },
    'DUPLICATE_TEST_PERCENTAGE': 0.08,
}
```
**Use Case**: Realistic distribution mimicking production patterns.

---

## 15. Edge Cases & Stress Testing

```python
CONFIG = {
    'TOTAL_RECORDS': 25000,
    'USE_ALL_KPI_CODES': True,
    'DURATION_DISTRIBUTION': {
        'short': 0.20,
        'medium': 0.20,
        'long': 0.30,
        'very_long': 0.30  # Many edge cases
    },
    'DUPLICATE_TEST_PERCENTAGE': 0.25,
    'DUPLICATE_TIME_WINDOW_HOURS': 1,  # Very tight window
    'ENSURE_FY_SPANNING_TASKS': True,
    'STAGGERED_ROLLOVER_TASKS': True,
}
```
**Use Case**: Maximum edge cases for comprehensive testing.

---

## Output Configuration Options

### Lakehouse Only (Validation)
```python
CONFIG = {
    # ... other settings ...
    'OUTPUT_TO_LH': True,
    'LH_TABLE_NAME': 'test_potential_failures_validation',
    'OUTPUT_TO_SQL': False,
}
```

### SQL Server Only
```python
CONFIG = {
    # ... other settings ...
    'OUTPUT_TO_LH': False,
    'OUTPUT_TO_SQL': True,
    'SQL_TABLE_NAME': 'app_potential_failures_test',
}
```

### Both Outputs
```python
CONFIG = {
    # ... other settings ...
    'OUTPUT_TO_LH': True,
    'LH_TABLE_NAME': 'test_potential_failures_validation',
    'OUTPUT_TO_SQL': True,
    'SQL_TABLE_NAME': 'app_potential_failures_test',
}
```

---

## Duration Range Customization

### Conservative Durations
```python
CONFIG = {
    'SHORT_DURATION_RANGE': (1, 12),      # 1-12 hours
    'MEDIUM_DURATION_RANGE': (13, 72),    # 0.5-3 days
    'LONG_DURATION_RANGE': (73, 336),     # 3-14 days
    'VERY_LONG_DURATION_RANGE': (337, 720), # 14-30 days
}
```

### Aggressive Durations (More Edge Cases)
```python
CONFIG = {
    'SHORT_DURATION_RANGE': (1, 48),       # 1-48 hours
    'MEDIUM_DURATION_RANGE': (49, 240),    # 2-10 days
    'LONG_DURATION_RANGE': (241, 1440),    # 10-60 days
    'VERY_LONG_DURATION_RANGE': (1441, 4320), # 60-180 days
}
```

---

## Tips

1. **Start Small**: Use 1000-5000 records first to verify configuration
2. **Validate First**: Always write to Lakehouse before SQL Server
3. **Mix Scenarios**: Combine multiple configurations for comprehensive testing
4. **Document**: Keep track of which configuration generated each dataset
5. **Iterate**: Adjust based on validation results

## Common Combinations

### Comprehensive Testing Suite
Run these 3 configurations to cover all scenarios:

**Config 1**: Default (15k records, all KPIs, standard distribution)
**Config 2**: Duplicate Heavy (5k records, 30% duplicates)
**Config 3**: FY Rollover (6k records, FY spanning focus)

This gives you ~26k total records covering all edge cases.
