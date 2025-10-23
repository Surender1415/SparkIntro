"""
Configuration file for Potential Failures Test Data Generator

Modify these settings to customize data generation.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DataGenerationConfig:
    """Configuration for test data generation."""
    
    # Data Volume Settings
    total_records: int = 15000
    start_date: str = '2025-05-25'
    end_date: str = '2027-05-25'
    
    # KPI Code Settings
    use_all_kpi_codes: bool = True
    selected_kpi_codes: List[str] = field(default_factory=list)
    include_non_kpi_tasks: bool = False
    non_kpi_task_percentage: float = 0.05
    
    # Duration Settings (in hours)
    short_duration_range: tuple = (1, 24)
    medium_duration_range: tuple = (25, 168)
    long_duration_range: tuple = (169, 720)
    very_long_duration_range: tuple = (721, 2160)
    
    # Duration Distribution
    duration_distribution: Dict[str, float] = field(default_factory=lambda: {
        'short': 0.40,
        'medium': 0.35,
        'long': 0.20,
        'very_long': 0.05
    })
    
    # Financial Year Settings
    financial_year_end: str = '03-31'  # MM-DD format
    ensure_fy_spanning_tasks: bool = True
    staggered_rollover_tasks: bool = True
    
    # Duplicate Testing Settings
    duplicate_test_percentage: float = 0.10
    duplicate_time_window_hours: int = 4
    
    # Station Distribution
    exclude_null_sections: bool = True
    
    # Output Settings
    output_directory: str = './output'
    output_filename: str = 'potential_failures_test_data'
    output_format: str = 'csv'  # 'csv', 'parquet', or 'both'
    
    # Status Progression Simulation
    simulate_status_progression: bool = False
    status_progression_steps: List[str] = field(default_factory=lambda: ['WAPPR', 'APPR', 'COMP'])
    
    # Task Frequency Weights by KPI Code
    kpi_frequency_weights: Dict[str, float] = field(default_factory=dict)
    
    # Logging
    log_level: str = 'INFO'  # DEBUG, INFO, WARNING, ERROR
    log_to_file: bool = True
    log_filename: str = 'data_generation.log'


# Sample KPI Codes (replaces bronze.fms_dimkpiclassification)
SAMPLE_KPI_CODES = [
    {
        'KPICode': 'GRAFFITI',
        'KPIDescription': 'Graffiti Removal',
        'KPICategory': 'Cleaning',
        'AnnualThresholdHours': 24,
        'IsKPI': 1
    },
    {
        'KPICode': 'TRACKSIDE_CLEAN',
        'KPIDescription': 'Trackside Cleaning',
        'KPICategory': 'Cleaning',
        'AnnualThresholdHours': 48,
        'IsKPI': 1
    },
    {
        'KPICode': 'ESCALATOR_REPAIR',
        'KPIDescription': 'Escalator Repair',
        'KPICategory': 'Maintenance',
        'AnnualThresholdHours': 100,
        'IsKPI': 1
    },
    {
        'KPICode': 'LIFT_MAINTENANCE',
        'KPIDescription': 'Lift Maintenance',
        'KPICategory': 'Maintenance',
        'AnnualThresholdHours': 100,
        'IsKPI': 1
    },
    {
        'KPICode': 'STATION_CLEAN',
        'KPIDescription': 'Station Cleaning',
        'KPICategory': 'Cleaning',
        'AnnualThresholdHours': 48,
        'IsKPI': 1
    },
    {
        'KPICode': 'PLATFORM_REPAIR',
        'KPIDescription': 'Platform Repair',
        'KPICategory': 'Maintenance',
        'AnnualThresholdHours': 72,
        'IsKPI': 1
    },
    {
        'KPICode': 'LIGHTING_FIX',
        'KPIDescription': 'Lighting Repair',
        'KPICategory': 'Maintenance',
        'AnnualThresholdHours': 24,
        'IsKPI': 1
    },
    {
        'KPICode': 'SIGNAGE_UPDATE',
        'KPIDescription': 'Signage Update',
        'KPICategory': 'Maintenance',
        'AnnualThresholdHours': 24,
        'IsKPI': 1
    },
    {
        'KPICode': 'TOILET_CLEAN',
        'KPIDescription': 'Toilet Cleaning',
        'KPICategory': 'Cleaning',
        'AnnualThresholdHours': 36,
        'IsKPI': 1
    },
    {
        'KPICode': 'HVAC_MAINTENANCE',
        'KPIDescription': 'HVAC Maintenance',
        'KPICategory': 'Maintenance',
        'AnnualThresholdHours': 120,
        'IsKPI': 1
    }
]

# Sample Stations (replaces customer_success.dimStation)
SAMPLE_STATIONS = [
    {'StationCode': 'KGX', 'StationName': 'Kings Cross St Pancras', 'Section': 'North'},
    {'StationCode': 'LBG', 'StationName': 'London Bridge', 'Section': 'South'},
    {'StationCode': 'VIC', 'StationName': 'Victoria', 'Section': 'South'},
    {'StationCode': 'WAT', 'StationName': 'Waterloo', 'Section': 'South'},
    {'StationCode': 'EUS', 'StationName': 'Euston', 'Section': 'North'},
    {'StationCode': 'PAD', 'StationName': 'Paddington', 'Section': 'West'},
    {'StationCode': 'LST', 'StationName': 'Liverpool Street', 'Section': 'East'},
    {'StationCode': 'CHX', 'StationName': 'Charing Cross', 'Section': 'Central'},
    {'StationCode': 'MOG', 'StationName': 'Moorgate', 'Section': 'Central'},
    {'StationCode': 'CAN', 'StationName': 'Cannon Street', 'Section': 'Central'},
    {'StationCode': 'BFR', 'StationName': 'Blackfriars', 'Section': 'Central'},
    {'StationCode': 'FAR', 'StationName': 'Farringdon', 'Section': 'Central'},
    {'StationCode': 'OXC', 'StationName': 'Oxford Circus', 'Section': 'West'},
    {'StationCode': 'BDS', 'StationName': 'Bond Street', 'Section': 'West'},
    {'StationCode': 'TCR', 'StationName': 'Tottenham Court Road', 'Section': 'Central'},
    {'StationCode': 'BAK', 'StationName': 'Baker Street', 'Section': 'North'},
    {'StationCode': 'WAL', 'StationName': 'Waterloo East', 'Section': 'South'},
    {'StationCode': 'CLJ', 'StationName': 'Clapham Junction', 'Section': 'South'},
    {'StationCode': 'STR', 'StationName': 'Stratford', 'Section': 'East'},
    {'StationCode': 'CRY', 'StationName': 'Croydon', 'Section': 'South'},
]

# Sample Reporter Names
SAMPLE_REPORTERS = [
    'John Smith',
    'Jane Doe',
    'Robert Johnson',
    'Emily Williams',
    'Michael Brown',
    'Sarah Davis',
    'David Wilson',
    'Lisa Anderson',
    'James Taylor',
    'Mary Thomas',
    'Christopher Moore',
    'Patricia Martin',
    'Daniel Jackson',
    'Jennifer White',
    'Matthew Harris'
]

# Sample Instruction Codes
SAMPLE_INSTRUCTION_CODES = [
    'MAINT',
    'CLEAN',
    'REPAIR',
    'INSPECT',
    'REPLACE',
    'INSTALL',
    'REMOVE',
    'UPDATE'
]

# Sample Locations within stations
SAMPLE_LOCATIONS = [
    'Platform 1',
    'Platform 2',
    'Platform 3',
    'Main Concourse',
    'North Entrance',
    'South Entrance',
    'East Entrance',
    'West Entrance',
    'Ticket Hall',
    'Gateline',
    'Station Office',
    'Staff Room',
    'Public Toilets',
    'Lift Shaft A',
    'Escalator 1',
    'Escalator 2',
    'Stairwell A',
    'Waiting Room'
]


# Pre-configured scenarios
SCENARIOS = {
    'default': {
        'total_records': 15000,
        'use_all_kpi_codes': True,
    },
    'graffiti': {
        'total_records': 10000,
        'use_all_kpi_codes': False,
        'selected_kpi_codes': ['GRAFFITI', 'TRACKSIDE_CLEAN', 'STATION_CLEAN'],
        'kpi_frequency_weights': {
            'GRAFFITI': 3.0,
            'TRACKSIDE_CLEAN': 2.0,
            'STATION_CLEAN': 1.5
        },
        'duration_distribution': {
            'short': 0.60,
            'medium': 0.30,
            'long': 0.08,
            'very_long': 0.02
        },
    },
    'maintenance': {
        'total_records': 8000,
        'use_all_kpi_codes': False,
        'selected_kpi_codes': ['ESCALATOR_REPAIR', 'LIFT_MAINTENANCE', 'PLATFORM_REPAIR'],
        'duration_distribution': {
            'short': 0.20,
            'medium': 0.40,
            'long': 0.30,
            'very_long': 0.10
        },
    },
    'dev': {
        'total_records': 1000,
        'use_all_kpi_codes': True,
        'duplicate_test_percentage': 0.05,
    },
    'large': {
        'total_records': 50000,
        'use_all_kpi_codes': True,
    }
}
