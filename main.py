#!/usr/bin/env python3
"""
Main entry point for Potential Failures Test Data Generator

Provides command-line interface for generating test data with various scenarios.

Usage:
    python main.py                          # Run with default config
    python main.py --scenario graffiti      # Run with pre-configured scenario
    python main.py --records 5000           # Custom record count
    python main.py --config my_config.json  # Load config from file
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

from config import DataGenerationConfig, SCENARIOS
from data_generator import DataGenerator, load_scenario


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate test data for app_potential_failures schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with default configuration (15k records)
  python main.py
  
  # Use pre-configured scenario
  python main.py --scenario graffiti
  
  # Custom record count
  python main.py --records 5000
  
  # List available scenarios
  python main.py --list-scenarios
  
  # Save configuration to file
  python main.py --save-config my_config.json
  
  # Load configuration from file
  python main.py --config my_config.json
  
  # Combine options
  python main.py --scenario maintenance --records 10000 --output ./test_output
        """
    )
    
    parser.add_argument(
        '--scenario', '-s',
        choices=list(SCENARIOS.keys()),
        help='Pre-configured scenario to use'
    )
    
    parser.add_argument(
        '--records', '-r',
        type=int,
        help='Number of records to generate'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output directory for generated files'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['csv', 'parquet', 'both'],
        help='Output format (csv, parquet, or both)'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Load configuration from JSON file'
    )
    
    parser.add_argument(
        '--save-config',
        help='Save current configuration to JSON file and exit'
    )
    
    parser.add_argument(
        '--list-scenarios',
        action='store_true',
        help='List available pre-configured scenarios'
    )
    
    parser.add_argument(
        '--kpi-codes',
        nargs='+',
        help='Specific KPI codes to generate (space-separated)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--no-fy-spanning',
        action='store_true',
        help='Disable FY-spanning task generation'
    )
    
    parser.add_argument(
        '--duplicate-pct',
        type=float,
        help='Percentage of duplicate tasks (0-1)'
    )
    
    parser.add_argument(
        '--status-progression',
        action='store_true',
        help='Generate status progression snapshot files'
    )
    
    return parser.parse_args()


def list_scenarios():
    """Display available scenarios."""
    print("\n" + "="*80)
    print("AVAILABLE SCENARIOS")
    print("="*80 + "\n")
    
    for name, config in SCENARIOS.items():
        print(f"  {name}:")
        for key, value in config.items():
            print(f"    {key}: {value}")
        print()


def save_config_to_file(config: DataGenerationConfig, filepath: str):
    """Save configuration to JSON file."""
    from dataclasses import asdict
    
    config_dict = asdict(config)
    
    with open(filepath, 'w') as f:
        json.dump(config_dict, f, indent=2, default=str)
    
    print(f"✓ Configuration saved to: {filepath}")


def load_config_from_file(filepath: str) -> DataGenerationConfig:
    """Load configuration from JSON file."""
    with open(filepath, 'r') as f:
        config_dict = json.load(f)
    
    # Convert dict to config object
    config = DataGenerationConfig()
    for key, value in config_dict.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    print(f"✓ Configuration loaded from: {filepath}")
    return config


def main():
    """Main execution function."""
    args = parse_arguments()
    
    # List scenarios if requested
    if args.list_scenarios:
        list_scenarios()
        return 0
    
    # Load or create configuration
    if args.config:
        config = load_config_from_file(args.config)
    else:
        config = DataGenerationConfig()
    
    # Load scenario if specified
    if args.scenario:
        config = load_scenario(args.scenario, config)
        print(f"✓ Loaded scenario: {args.scenario}")
    
    # Apply command-line overrides
    if args.records:
        config.total_records = args.records
    
    if args.output:
        config.output_directory = args.output
    
    if args.format:
        config.output_format = args.format
    
    if args.kpi_codes:
        config.use_all_kpi_codes = False
        config.selected_kpi_codes = args.kpi_codes
    
    if args.log_level:
        config.log_level = args.log_level
    
    if args.no_fy_spanning:
        config.ensure_fy_spanning_tasks = False
    
    if args.duplicate_pct is not None:
        config.duplicate_test_percentage = args.duplicate_pct
    
    if args.status_progression:
        config.simulate_status_progression = True
    
    # Save config if requested
    if args.save_config:
        save_config_to_file(config, args.save_config)
        return 0
    
    # Display configuration summary
    print("\n" + "="*80)
    print("CONFIGURATION SUMMARY")
    print("="*80)
    print(f"Total records: {config.total_records}")
    print(f"Date range: {config.start_date} to {config.end_date}")
    print(f"KPI codes: {'All' if config.use_all_kpi_codes else config.selected_kpi_codes}")
    print(f"Output directory: {config.output_directory}")
    print(f"Output format: {config.output_format}")
    print(f"Log level: {config.log_level}")
    print("="*80 + "\n")
    
    # Run generator
    try:
        generator = DataGenerator(config)
        df = generator.run()
        
        print("\n" + "="*80)
        print("✅ SUCCESS")
        print("="*80)
        print(f"Generated {len(df)} records")
        print(f"Output directory: {config.output_directory}")
        print(f"Format: {config.output_format}")
        print("\nFirst few records:")
        print(df.head(3))
        print("="*80)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
