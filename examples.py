#!/usr/bin/env python3
"""
Example usage patterns for the Potential Failures Test Data Generator

This file demonstrates various ways to use the data generator.
Run this file to see the examples in action: python examples.py
"""

from config import DataGenerationConfig, SCENARIOS
from data_generator import DataGenerator, load_scenario
import pandas as pd


def example_1_basic_usage():
    """Example 1: Basic usage with default configuration."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    config = DataGenerationConfig()
    config.total_records = 1000  # Small dataset for demo
    config.output_filename = 'example_1_basic'
    
    generator = DataGenerator(config)
    df = generator.run()
    
    print(f"\n✅ Generated {len(df)} records")
    print(f"\nFirst 3 records:")
    print(df.head(3))


def example_2_use_scenario():
    """Example 2: Using a pre-configured scenario."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Using Pre-configured Scenario")
    print("="*80)
    
    config = DataGenerationConfig()
    config = load_scenario('graffiti', config)
    config.total_records = 1000  # Override for demo
    config.output_filename = 'example_2_graffiti'
    
    generator = DataGenerator(config)
    df = generator.run()
    
    print(f"\n✅ Generated {len(df)} records for graffiti scenario")
    print(f"\nKPI Distribution:")
    print(df['KPIDescription'].value_counts())


def example_3_custom_config():
    """Example 3: Custom configuration."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Custom Configuration")
    print("="*80)
    
    config = DataGenerationConfig()
    
    # Customize all settings
    config.total_records = 1500
    config.use_all_kpi_codes = False
    config.selected_kpi_codes = ['ESCALATOR_REPAIR', 'LIFT_MAINTENANCE']
    config.duplicate_test_percentage = 0.20
    config.output_filename = 'example_3_custom'
    
    # Custom duration distribution
    config.duration_distribution = {
        'short': 0.20,
        'medium': 0.40,
        'long': 0.30,
        'very_long': 0.10
    }
    
    # KPI frequency weights
    config.kpi_frequency_weights = {
        'ESCALATOR_REPAIR': 2.0,
        'LIFT_MAINTENANCE': 1.0
    }
    
    generator = DataGenerator(config)
    df = generator.run()
    
    print(f"\n✅ Generated {len(df)} records with custom configuration")
    print(f"\nKPI Distribution:")
    print(df['KPIDescription'].value_counts())


def example_4_validation():
    """Example 4: Generate and validate data."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Data Generation with Validation")
    print("="*80)
    
    config = DataGenerationConfig()
    config.total_records = 1000
    config.output_filename = 'example_4_validation'
    
    generator = DataGenerator(config)
    df = generator.run()
    
    # Manual validation
    print("\n🔍 Validation Checks:")
    
    # Check 1: All status = COMP
    all_comp = (df['Status'] == 'COMP').all()
    print(f"  ✓ All tasks COMP status: {all_comp}")
    
    # Check 2: Date logic
    date_logic = (
        (df['ReportedDate'] <= df['LoggedOn']).all() and
        (df['LoggedOn'] <= df['ScheduledFor']).all() and
        (df['ScheduledFor'] <= df['Finished']).all()
    )
    print(f"  ✓ Date logic correct: {date_logic}")
    
    # Check 3: No nulls in key fields
    no_nulls = not df[['TaskId', 'Building', 'KPIDescription']].isnull().any().any()
    print(f"  ✓ No nulls in key fields: {no_nulls}")
    
    # Check 4: Period format
    period_format = df['Period'].str.startswith('P').all()
    print(f"  ✓ Period format correct: {period_format}")
    
    # Duration analysis
    df['Duration_Hours'] = (df['Finished'] - df['LoggedOn']).dt.total_seconds() / 3600
    print(f"\n📊 Duration Statistics:")
    print(f"  Min: {df['Duration_Hours'].min():.1f} hours")
    print(f"  Max: {df['Duration_Hours'].max():.1f} hours")
    print(f"  Mean: {df['Duration_Hours'].mean():.1f} hours")
    print(f"  Median: {df['Duration_Hours'].median():.1f} hours")


def example_5_multiple_outputs():
    """Example 5: Generate with different output formats."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Multiple Output Formats")
    print("="*80)
    
    config = DataGenerationConfig()
    config.total_records = 500
    config.output_filename = 'example_5_formats'
    config.output_format = 'both'  # Generate both CSV and Parquet
    
    generator = DataGenerator(config)
    df = generator.run()
    
    print(f"\n✅ Generated {len(df)} records in both CSV and Parquet formats")


def example_6_status_progression():
    """Example 6: Generate status progression snapshots."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Status Progression Snapshots")
    print("="*80)
    
    config = DataGenerationConfig()
    config.total_records = 500
    config.output_filename = 'example_6_progression'
    config.simulate_status_progression = True
    config.status_progression_steps = ['WAPPR', 'APPR', 'COMP']
    
    generator = DataGenerator(config)
    df = generator.run()
    
    print(f"\n✅ Generated {len(df)} records with status progression snapshots")
    print("  Files created: snapshot_1_WAPPR, snapshot_2_APPR, snapshot_3_COMP")


def example_7_batch_generation():
    """Example 7: Generate multiple batches."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Batch Generation")
    print("="*80)
    
    total_needed = 5000
    batch_size = 1000
    num_batches = total_needed // batch_size
    
    all_dfs = []
    
    for i in range(num_batches):
        print(f"\nGenerating batch {i+1}/{num_batches}...")
        
        config = DataGenerationConfig()
        config.total_records = batch_size
        config.output_filename = f'example_7_batch_{i+1}'
        config.log_level = 'WARNING'  # Reduce logging for batches
        
        generator = DataGenerator(config)
        df = generator.run()
        all_dfs.append(df)
    
    # Combine all batches
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    print(f"\n✅ Generated {len(combined_df)} records in {num_batches} batches")
    print(f"  Total unique tasks: {combined_df['TaskId'].nunique()}")


def example_8_specific_stations():
    """Example 8: Filter data for specific stations."""
    print("\n" + "="*80)
    print("EXAMPLE 8: Post-Generation Filtering")
    print("="*80)
    
    config = DataGenerationConfig()
    config.total_records = 2000
    config.output_filename = 'example_8_all'
    
    generator = DataGenerator(config)
    df = generator.run()
    
    # Filter for specific stations
    target_stations = ['KGX', 'VIC', 'WAT']
    filtered_df = df[df['Building'].isin(target_stations)]
    
    print(f"\n✅ Generated {len(df)} total records")
    print(f"  Filtered to {len(filtered_df)} records for stations: {target_stations}")
    print(f"\nDistribution:")
    print(filtered_df['Building'].value_counts())


def example_9_analytics():
    """Example 9: Generate and perform analytics."""
    print("\n" + "="*80)
    print("EXAMPLE 9: Data Analytics")
    print("="*80)
    
    config = DataGenerationConfig()
    config.total_records = 2000
    config.output_filename = 'example_9_analytics'
    
    generator = DataGenerator(config)
    df = generator.run()
    
    # Calculate durations
    df['Duration_Hours'] = (df['Finished'] - df['LoggedOn']).dt.total_seconds() / 3600
    df['Duration_Days'] = df['Duration_Hours'] / 24
    
    # Analytics
    print("\n📊 Analytics Summary:")
    
    # By KPI Category
    print("\n1. Average Duration by KPI Category:")
    category_stats = df.groupby('KPICategory')['Duration_Hours'].agg(['mean', 'count'])
    print(category_stats)
    
    # By Station Section
    print("\n2. Task Count by Station Section:")
    section_counts = df['StationSection'].value_counts()
    print(section_counts)
    
    # By Period
    print("\n3. Task Count by Period:")
    period_counts = df['Period'].value_counts().sort_index()
    print(period_counts.head())
    
    # SLA Status
    print("\n4. SLA Status Distribution:")
    sla_pct = df['SLAStatus'].value_counts(normalize=True) * 100
    print(sla_pct)


def example_10_save_load_config():
    """Example 10: Save and load configuration."""
    print("\n" + "="*80)
    print("EXAMPLE 10: Save and Load Configuration")
    print("="*80)
    
    import json
    from dataclasses import asdict
    
    # Create custom configuration
    config = DataGenerationConfig()
    config.total_records = 3000
    config.use_all_kpi_codes = False
    config.selected_kpi_codes = ['GRAFFITI', 'STATION_CLEAN']
    config.duplicate_test_percentage = 0.15
    
    # Save configuration
    config_dict = asdict(config)
    config_file = './output/my_custom_config.json'
    
    with open(config_file, 'w') as f:
        json.dump(config_dict, f, indent=2, default=str)
    
    print(f"✓ Saved configuration to: {config_file}")
    
    # Load configuration
    with open(config_file, 'r') as f:
        loaded_config_dict = json.load(f)
    
    # Apply to new config object
    loaded_config = DataGenerationConfig()
    for key, value in loaded_config_dict.items():
        if hasattr(loaded_config, key):
            setattr(loaded_config, key, value)
    
    loaded_config.output_filename = 'example_10_loaded'
    
    print(f"✓ Loaded configuration from: {config_file}")
    print(f"  Total records: {loaded_config.total_records}")
    print(f"  Selected KPIs: {loaded_config.selected_kpi_codes}")
    
    # Generate with loaded config
    generator = DataGenerator(loaded_config)
    df = generator.run()
    
    print(f"\n✅ Generated {len(df)} records from loaded configuration")


def run_all_examples():
    """Run all examples."""
    print("\n" + "="*80)
    print("RUNNING ALL EXAMPLES")
    print("="*80)
    
    examples = [
        ("Basic Usage", example_1_basic_usage),
        ("Pre-configured Scenario", example_2_use_scenario),
        ("Custom Configuration", example_3_custom_config),
        ("Validation", example_4_validation),
        ("Multiple Output Formats", example_5_multiple_outputs),
        ("Status Progression", example_6_status_progression),
        ("Batch Generation", example_7_batch_generation),
        ("Post-Generation Filtering", example_8_specific_stations),
        ("Analytics", example_9_analytics),
        ("Save/Load Configuration", example_10_save_load_config),
    ]
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{'='*80}")
        print(f"Running Example {i}: {name}")
        print(f"{'='*80}")
        try:
            func()
            print(f"\n✅ Example {i} completed successfully")
        except Exception as e:
            print(f"\n❌ Example {i} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("✅ ALL EXAMPLES COMPLETED")
    print("="*80)
    print("\nCheck the ./output directory for generated files")


if __name__ == "__main__":
    import sys
    
    # You can run specific examples or all
    if len(sys.argv) > 1:
        example_num = int(sys.argv[1])
        examples = [
            example_1_basic_usage,
            example_2_use_scenario,
            example_3_custom_config,
            example_4_validation,
            example_5_multiple_outputs,
            example_6_status_progression,
            example_7_batch_generation,
            example_8_specific_stations,
            example_9_analytics,
            example_10_save_load_config,
        ]
        
        if 1 <= example_num <= len(examples):
            examples[example_num - 1]()
        else:
            print(f"Invalid example number. Choose 1-{len(examples)}")
    else:
        # Run just a few key examples (not all to save time)
        print("Running key examples (use 'python examples.py [1-10]' for specific example)")
        example_1_basic_usage()
        example_2_use_scenario()
        example_4_validation()
        print("\n✅ Run 'python examples.py' to see all examples or specify number: python examples.py 3")
