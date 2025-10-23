#!/usr/bin/env python3
"""
Quick Configuration Generator for Potential Failures Test Data

This script helps generate configuration dictionaries for different test scenarios
without manually editing the notebook.

Usage:
    python quick_config.py --scenario default
    python quick_config.py --scenario graffiti --records 10000
    python quick_config.py --custom
"""

import argparse
import json
from typing import Dict, Any

# Predefined scenario configurations
SCENARIOS = {
    "default": {
        "name": "Default Test Dataset",
        "description": "15k records, all KPI codes, standard distribution",
        "config": {
            'TOTAL_RECORDS': 15000,
            'USE_ALL_KPI_CODES': True,
            'SELECTED_KPI_CODES': [],
            'DURATION_DISTRIBUTION': {
                'short': 0.40,
                'medium': 0.35,
                'long': 0.20,
                'very_long': 0.05
            },
            'DUPLICATE_TEST_PERCENTAGE': 0.10,
        }
    },
    
    "graffiti": {
        "name": "Graffiti & Cleaning Focus",
        "description": "Focus on cleaning KPIs with short durations",
        "config": {
            'TOTAL_RECORDS': 10000,
            'USE_ALL_KPI_CODES': False,
            'SELECTED_KPI_CODES': ['GRAFFITI', 'TRACKSIDE_CLEAN', 'STATION_CLEAN'],
            'KPI_FREQUENCY_WEIGHTS': {
                'GRAFFITI': 3.0,
                'TRACKSIDE_CLEAN': 2.0,
                'STATION_CLEAN': 1.5
            },
            'DURATION_DISTRIBUTION': {
                'short': 0.60,
                'medium': 0.30,
                'long': 0.08,
                'very_long': 0.02
            },
        }
    },
    
    "maintenance": {
        "name": "Maintenance & Repair Focus",
        "description": "Focus on maintenance KPIs with longer durations",
        "config": {
            'TOTAL_RECORDS': 8000,
            'USE_ALL_KPI_CODES': False,
            'SELECTED_KPI_CODES': ['ESCALATOR_REPAIR', 'LIFT_MAINTENANCE', 'PLATFORM_REPAIR'],
            'DURATION_DISTRIBUTION': {
                'short': 0.20,
                'medium': 0.40,
                'long': 0.30,
                'very_long': 0.10
            },
        }
    },
    
    "threshold": {
        "name": "Threshold Rollover Testing",
        "description": "Test annual threshold rollover (24h, 48h, 100h)",
        "config": {
            'TOTAL_RECORDS': 5000,
            'USE_ALL_KPI_CODES': False,
            'SELECTED_KPI_CODES': ['GRAFFITI', 'TRACKSIDE_CLEAN', 'ESCALATOR_REPAIR'],
            'ENSURE_FY_SPANNING_TASKS': True,
            'STAGGERED_ROLLOVER_TASKS': True,
        }
    },
    
    "duplicates": {
        "name": "Duplicate Detection Testing",
        "description": "30% duplicate tasks for testing detection",
        "config": {
            'TOTAL_RECORDS': 5000,
            'DUPLICATE_TEST_PERCENTAGE': 0.30,
            'DUPLICATE_TIME_WINDOW_HOURS': 2,
        }
    },
    
    "period": {
        "name": "Period Boundary Testing",
        "description": "Many tasks crossing period boundaries",
        "config": {
            'TOTAL_RECORDS': 8000,
            'DURATION_DISTRIBUTION': {
                'short': 0.10,
                'medium': 0.20,
                'long': 0.40,
                'very_long': 0.30
            },
        }
    },
    
    "fy": {
        "name": "Financial Year Testing",
        "description": "FY boundary crossing and threshold rollover",
        "config": {
            'TOTAL_RECORDS': 6000,
            'START_DATE': '2025-02-01',
            'END_DATE': '2027-05-31',
            'ENSURE_FY_SPANNING_TASKS': True,
            'STAGGERED_ROLLOVER_TASKS': True,
            'DURATION_DISTRIBUTION': {
                'short': 0.25,
                'medium': 0.30,
                'long': 0.30,
                'very_long': 0.15
            },
        }
    },
    
    "dev": {
        "name": "Small Development Dataset",
        "description": "1k records for quick testing",
        "config": {
            'TOTAL_RECORDS': 1000,
            'USE_ALL_KPI_CODES': True,
            'DUPLICATE_TEST_PERCENTAGE': 0.05,
        }
    },
    
    "large": {
        "name": "Large Volume Testing",
        "description": "50k records for performance testing",
        "config": {
            'TOTAL_RECORDS': 50000,
            'USE_ALL_KPI_CODES': True,
        }
    },
    
    "status": {
        "name": "Status Progression Testing",
        "description": "Testing backload with status changes",
        "config": {
            'TOTAL_RECORDS': 3000,
            'SIMULATE_STATUS_PROGRESSION': True,
            'STATUS_PROGRESSION_STEPS': ['WAPPR', 'APPR', 'COMP'],
        }
    },
    
    "realistic": {
        "name": "Realistic Production Simulation",
        "description": "20k records mimicking production patterns",
        "config": {
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
    },
    
    "edge": {
        "name": "Edge Cases & Stress Testing",
        "description": "25k records with maximum edge cases",
        "config": {
            'TOTAL_RECORDS': 25000,
            'USE_ALL_KPI_CODES': True,
            'DURATION_DISTRIBUTION': {
                'short': 0.20,
                'medium': 0.20,
                'long': 0.30,
                'very_long': 0.30
            },
            'DUPLICATE_TEST_PERCENTAGE': 0.25,
            'DUPLICATE_TIME_WINDOW_HOURS': 1,
            'ENSURE_FY_SPANNING_TASKS': True,
            'STAGGERED_ROLLOVER_TASKS': True,
        }
    }
}


def get_base_config() -> Dict[str, Any]:
    """Return base configuration with all default values."""
    return {
        'TOTAL_RECORDS': 15000,
        'START_DATE': '2025-05-25',
        'END_DATE': '2027-05-25',
        'USE_ALL_KPI_CODES': True,
        'SELECTED_KPI_CODES': [],
        'INCLUDE_NON_KPI_TASKS': False,
        'NON_KPI_TASK_PERCENTAGE': 0.05,
        'SHORT_DURATION_RANGE': (1, 24),
        'MEDIUM_DURATION_RANGE': (25, 168),
        'LONG_DURATION_RANGE': (169, 720),
        'VERY_LONG_DURATION_RANGE': (721, 2160),
        'DURATION_DISTRIBUTION': {
            'short': 0.40,
            'medium': 0.35,
            'long': 0.20,
            'very_long': 0.05
        },
        'FINANCIAL_YEAR_END': '03-31',
        'ENSURE_FY_SPANNING_TASKS': True,
        'STAGGERED_ROLLOVER_TASKS': True,
        'DUPLICATE_TEST_PERCENTAGE': 0.10,
        'DUPLICATE_TIME_WINDOW_HOURS': 4,
        'EXCLUDE_NULL_SECTIONS': True,
        'OUTPUT_TO_LH': True,
        'LH_TABLE_NAME': 'test_potential_failures_validation',
        'OUTPUT_TO_SQL': False,
        'SQL_TABLE_NAME': 'app_potential_failures_test',
        'SIMULATE_STATUS_PROGRESSION': False,
        'STATUS_PROGRESSION_STEPS': ['WAPPR', 'APPR', 'COMP'],
        'KPI_FREQUENCY_WEIGHTS': {},
    }


def merge_configs(base: Dict, override: Dict) -> Dict:
    """Merge override config into base config."""
    result = base.copy()
    result.update(override)
    return result


def print_config(config: Dict, scenario_name: str = None):
    """Pretty print configuration."""
    if scenario_name and scenario_name in SCENARIOS:
        print(f"\n{'='*80}")
        print(f"SCENARIO: {SCENARIOS[scenario_name]['name']}")
        print(f"{'='*80}")
        print(f"{SCENARIOS[scenario_name]['description']}")
        print(f"{'='*80}\n")
    
    print("CONFIG = {")
    for key, value in config.items():
        if isinstance(value, str):
            print(f"    '{key}': '{value}',")
        elif isinstance(value, dict):
            print(f"    '{key}': {{")
            for k, v in value.items():
                if isinstance(k, str):
                    print(f"        '{k}': {v},")
                else:
                    print(f"        {k}: {v},")
            print(f"    }},")
        elif isinstance(value, list):
            if len(value) == 0:
                print(f"    '{key}': [],")
            else:
                print(f"    '{key}': {value},")
        else:
            print(f"    '{key}': {value},")
    print("}")


def list_scenarios():
    """List all available scenarios."""
    print("\n" + "="*80)
    print("AVAILABLE SCENARIOS")
    print("="*80 + "\n")
    
    for key, scenario in SCENARIOS.items():
        print(f"  {key:15} - {scenario['name']}")
        print(f"  {' '*15}   {scenario['description']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Generate configuration for Potential Failures test data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all scenarios
  python quick_config.py --list
  
  # Generate default configuration
  python quick_config.py --scenario default
  
  # Generate graffiti scenario with custom record count
  python quick_config.py --scenario graffiti --records 5000
  
  # Generate configuration with JSON output
  python quick_config.py --scenario threshold --json > config.json
  
  # Save to file
  python quick_config.py --scenario realistic --output my_config.py
        """
    )
    
    parser.add_argument('--scenario', '-s', 
                       choices=list(SCENARIOS.keys()),
                       help='Predefined scenario to use')
    
    parser.add_argument('--list', '-l', 
                       action='store_true',
                       help='List all available scenarios')
    
    parser.add_argument('--records', '-r',
                       type=int,
                       help='Override total records count')
    
    parser.add_argument('--json', '-j',
                       action='store_true',
                       help='Output as JSON instead of Python dict')
    
    parser.add_argument('--output', '-o',
                       help='Save configuration to file')
    
    parser.add_argument('--custom', '-c',
                       action='store_true',
                       help='Interactive custom configuration builder')
    
    args = parser.parse_args()
    
    # List scenarios
    if args.list:
        list_scenarios()
        return
    
    # Interactive custom builder
    if args.custom:
        print("Interactive configuration builder not yet implemented.")
        print("Please use --scenario or edit the notebook directly.")
        return
    
    # Default to 'default' scenario if none specified
    scenario = args.scenario or 'default'
    
    # Generate configuration
    base_config = get_base_config()
    scenario_config = SCENARIOS[scenario]['config']
    config = merge_configs(base_config, scenario_config)
    
    # Override record count if specified
    if args.records:
        config['TOTAL_RECORDS'] = args.records
    
    # Output
    if args.json:
        output = json.dumps(config, indent=2)
        print(output)
    else:
        output_lines = []
        print_config(config, scenario)
        
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            if args.json:
                f.write(json.dumps(config, indent=2))
            else:
                f.write("# Generated configuration\n")
                f.write(f"# Scenario: {SCENARIOS[scenario]['name']}\n")
                f.write(f"# Description: {SCENARIOS[scenario]['description']}\n\n")
                f.write("CONFIG = {\n")
                for key, value in config.items():
                    if isinstance(value, str):
                        f.write(f"    '{key}': '{value}',\n")
                    elif isinstance(value, dict):
                        f.write(f"    '{key}': {{\n")
                        for k, v in value.items():
                            if isinstance(k, str):
                                f.write(f"        '{k}': {v},\n")
                            else:
                                f.write(f"        {k}: {v},\n")
                        f.write(f"    }},\n")
                    elif isinstance(value, list):
                        f.write(f"    '{key}': {value},\n")
                    else:
                        f.write(f"    '{key}': {value},\n")
                f.write("}\n")
        print(f"\n✓ Configuration saved to {args.output}")


if __name__ == '__main__':
    main()
