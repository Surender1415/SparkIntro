"""
Potential Failures Test Data Generator

A scalable, flexible Python application for generating test data
for the app_potential_failures schema.

Author: Generated for test data creation
Version: 1.0
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional, Tuple
import logging
from pathlib import Path
import json
from dataclasses import asdict

from config import (
    DataGenerationConfig,
    SAMPLE_KPI_CODES,
    SAMPLE_STATIONS,
    SAMPLE_REPORTERS,
    SAMPLE_INSTRUCTION_CODES,
    SAMPLE_LOCATIONS,
    SCENARIOS
)


class DataGenerator:
    """Main class for generating test data."""
    
    def __init__(self, config: DataGenerationConfig):
        """
        Initialize the data generator.
        
        Args:
            config: Configuration object with generation parameters
        """
        self.config = config
        self.setup_logging()
        self.kpi_codes = self._load_kpi_codes()
        self.stations = self._load_stations()
        self.dates_df = self._generate_date_dimension()
        self.date_lookup = self.dates_df.set_index('Date').to_dict('index')
        self.all_tasks = []
        self.fy_spanning_tasks = set()
        self.tasks_by_station = {}
        
        self.logger.info(f"Initialized DataGenerator with {len(self.kpi_codes)} KPI codes and {len(self.stations)} stations")
    
    def setup_logging(self):
        """Configure logging for the application."""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        log_level = getattr(logging, self.config.log_level.upper())
        
        handlers = [logging.StreamHandler()]
        
        if self.config.log_to_file:
            log_file = Path(self.config.output_directory) / self.config.log_filename
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handlers.append(logging.FileHandler(log_file))
        
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=handlers
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _load_kpi_codes(self) -> List[Dict]:
        """Load KPI codes from configuration."""
        kpi_codes = SAMPLE_KPI_CODES.copy()
        
        # Filter if specific codes selected
        if not self.config.use_all_kpi_codes and self.config.selected_kpi_codes:
            kpi_codes = [k for k in kpi_codes if k['KPICode'] in self.config.selected_kpi_codes]
            self.logger.info(f"Using {len(kpi_codes)} selected KPI codes")
        else:
            self.logger.info(f"Using all {len(kpi_codes)} KPI codes")
        
        return kpi_codes
    
    def _load_stations(self) -> List[Dict]:
        """Load stations from configuration."""
        stations = SAMPLE_STATIONS.copy()
        
        # Exclude NULL sections if configured
        if self.config.exclude_null_sections:
            stations = [s for s in stations if s.get('Section')]
            self.logger.info(f"Excluded NULL sections, using {len(stations)} stations")
        
        return stations
    
    def _generate_date_dimension(self) -> pd.DataFrame:
        """Generate date dimension with period information."""
        date_range = pd.date_range(
            start=self.config.start_date,
            end=self.config.end_date,
            freq='D'
        )
        
        dates_df = pd.DataFrame({
            'Date': date_range,
            'RailPeriod': [(d.year - 2025) * 13 + ((d.month - 1) // 4) + 1 for d in date_range],
            'RailPeriodWeek': [((d - date_range[0]).days // 7) + 1 for d in date_range],
            'FiscalYear': [d.year if d.month >= 4 else d.year - 1 for d in date_range]
        })
        
        self.logger.info(f"Generated date dimension with {len(dates_df)} dates")
        return dates_df
    
    def get_random_datetime(self, start_date: str, end_date: str) -> datetime:
        """Generate a random datetime between start and end dates."""
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        delta = end - start
        random_days = random.randint(0, delta.days)
        random_seconds = random.randint(0, 86400)
        return start + timedelta(days=random_days, seconds=random_seconds)
    
    def get_duration_category(self) -> str:
        """Randomly select a duration category based on distribution weights."""
        categories = list(self.config.duration_distribution.keys())
        weights = list(self.config.duration_distribution.values())
        return random.choices(categories, weights=weights)[0]
    
    def get_duration_hours(self, category: str) -> int:
        """Get random duration in hours based on category."""
        ranges = {
            'short': self.config.short_duration_range,
            'medium': self.config.medium_duration_range,
            'long': self.config.long_duration_range,
            'very_long': self.config.very_long_duration_range
        }
        min_h, max_h = ranges[category]
        return random.randint(min_h, max_h)
    
    def get_period_info(self, date: datetime) -> Tuple[str, int, int]:
        """Get period information for a given date."""
        date_str = pd.to_datetime(date).strftime('%Y-%m-%d')
        date_key = pd.to_datetime(date_str)
        
        if date_key in self.date_lookup:
            info = self.date_lookup[date_key]
            period = f"P{info.get('RailPeriod', 1):02d}"
            period_week = info.get('RailPeriodWeek', 1)
            period_year = info.get('FiscalYear', date.year)
        else:
            # Fallback
            period = f"P{((date.month - 1) // 4) + 1:02d}"
            period_week = ((date - pd.to_datetime(self.config.start_date)).days // 7) + 1
            period_year = date.year if date.month >= 4 else date.year - 1
        
        return period, period_week, period_year
    
    def generate_task_id(self) -> str:
        """Generate a unique task ID."""
        return f"TSK-{random.randint(100000, 999999)}-{random.randint(1000, 9999)}"
    
    def generate_record_id(self) -> str:
        """Generate a unique record ID."""
        return f"REC-{random.randint(1000000, 9999999)}"
    
    def get_financial_year_dates(self, year: int) -> Tuple[datetime, datetime]:
        """Get start and end dates for a financial year."""
        fy_end_month, fy_end_day = map(int, self.config.financial_year_end.split('-'))
        fy_start = datetime(year - 1, fy_end_month, fy_end_day) + timedelta(days=1)
        fy_end = datetime(year, fy_end_month, fy_end_day)
        return fy_start, fy_end
    
    def create_task(self, kpi_info: Dict, station: Dict,
                   duration_category: Optional[str] = None,
                   force_fy_span: bool = False,
                   reference_task: Optional[Dict] = None) -> Dict:
        """
        Create a single task record.
        
        Args:
            kpi_info: KPI code information
            station: Station information
            duration_category: Force specific duration category
            force_fy_span: Force task to span financial year
            reference_task: Reference task for creating overlapping duplicates
        
        Returns:
            Dictionary containing task data
        """
        # Generate identifiers
        task_id = self.generate_task_id()
        record_id = self.generate_record_id()
        
        # Determine duration
        if duration_category is None:
            duration_category = self.get_duration_category()
        duration_hours = self.get_duration_hours(duration_category)
        
        # Generate dates
        if reference_task:
            # Create overlapping task for duplicate testing
            ref_logged = reference_task['LoggedOn']
            time_offset = random.randint(
                -self.config.duplicate_time_window_hours,
                self.config.duplicate_time_window_hours
            )
            logged_on = ref_logged + timedelta(hours=time_offset)
        elif force_fy_span:
            # Create task that spans financial year
            fy_year = 2026
            fy_start, fy_end = self.get_financial_year_dates(fy_year)
            days_before = random.randint(30, 90)
            logged_on = fy_end - timedelta(days=days_before)
            duration_hours = max(duration_hours, (days_before + 30) * 24)
        else:
            logged_on = self.get_random_datetime(
                self.config.start_date,
                self.config.end_date
            )
        
        # Calculate other dates
        reported_date = logged_on - timedelta(hours=random.randint(1, 48))
        scheduled_for = logged_on + timedelta(hours=random.randint(1, 24))
        finished = logged_on + timedelta(hours=duration_hours)
        
        # Ensure finished date is within range
        end_date = pd.to_datetime(self.config.end_date)
        if finished > end_date:
            finished = end_date - timedelta(hours=random.randint(1, 168))
        
        due_by = scheduled_for + timedelta(hours=random.randint(24, 168))
        modified_on = finished + timedelta(hours=random.randint(1, 4))
        
        # Get period information
        period, period_week, period_year = self.get_period_info(logged_on)
        
        # Sample data for various fields
        reporter = random.choice(SAMPLE_REPORTERS)
        reporter_email = f"{reporter.lower().replace(' ', '.')}@rail.com"
        
        # Create task record
        task = {
            'TaskId': task_id,
            'RecordID': record_id,
            'Instruction_Code': random.choice(SAMPLE_INSTRUCTION_CODES),
            'Building': station['StationCode'],
            'BuildingName': station['StationName'],
            'LocationName': f"{station['StationName']} - {random.choice(SAMPLE_LOCATIONS)}",
            'ShortDescription': f"{kpi_info['KPIDescription']} at {station['StationName']}",
            'LongDescription': f"Complete {kpi_info['KPIDescription'].lower()} work at {station['StationName']}. Duration: {duration_hours} hours. Category: {duration_category}.",
            'Reporter': reporter,
            'ReporterEmail': reporter_email,
            'Notes': f"Task completed. Duration category: {duration_category}. Threshold: {kpi_info['AnnualThresholdHours']}h/year.",
            'ReportedDate': reported_date,
            'DueBy': due_by,
            'ScheduledFor': scheduled_for,
            'Finished': finished,
            'Status': 'COMP',
            'LoggedBy': f"System-{random.randint(1, 10)}",
            'LoggedOn': logged_on,
            'ModifiedOn': modified_on,
            'SLAStatus': random.choice(['Met', 'Met', 'Met', 'Missed']),
            'CreatedTimestamp': logged_on,
            'LastUploaded': modified_on + timedelta(hours=1),
            'IsCurrent': 1,
            'Period': period,
            'PeriodWeek': period_week,
            'PeriodYear': period_year,
            'StationSection': station.get('Section', 'Unknown'),
            'KPIDescription': kpi_info['KPIDescription'],
            'KPICategory': kpi_info['KPICategory']
        }
        
        return task
    
    def generate_all_tasks(self) -> pd.DataFrame:
        """Generate all tasks based on configuration."""
        self.logger.info("="*80)
        self.logger.info("Starting test data generation")
        self.logger.info("="*80)
        
        total_records = self.config.total_records
        num_kpi_codes = len(self.kpi_codes)
        
        # Apply frequency weights
        if self.config.kpi_frequency_weights:
            weights = [
                self.config.kpi_frequency_weights.get(k['KPICode'], 1.0)
                for k in self.kpi_codes
            ]
        else:
            weights = [1.0] * num_kpi_codes
        
        # Normalize weights
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        # Calculate tasks per KPI code
        tasks_per_kpi = [int(total_records * w) for w in normalized_weights]
        
        # Adjust for rounding
        while sum(tasks_per_kpi) < total_records:
            tasks_per_kpi[random.randint(0, len(tasks_per_kpi) - 1)] += 1
        
        self.logger.info(f"Generating {total_records} tasks across {num_kpi_codes} KPI codes")
        self.logger.info(f"Average tasks per KPI code: {total_records / num_kpi_codes:.0f}")
        self.logger.info(f"Stations available: {len(self.stations)}")
        
        # Generate tasks for each KPI code
        for kpi_idx, kpi_info in enumerate(self.kpi_codes):
            kpi_code = kpi_info['KPICode']
            num_tasks = tasks_per_kpi[kpi_idx]
            
            self.logger.info(f"Generating {num_tasks} tasks for {kpi_code}...")
            
            duration_categories = list(self.config.duration_distribution.keys())
            tasks_generated = 0
            
            # 1. Generate FY-spanning task
            if self.config.ensure_fy_spanning_tasks and kpi_code not in self.fy_spanning_tasks:
                station = random.choice(self.stations)
                task = self.create_task(kpi_info, station, force_fy_span=True)
                self.all_tasks.append(task)
                self.fy_spanning_tasks.add(kpi_code)
                tasks_generated += 1
            
            # 2. Generate at least one task of each duration category
            for duration_cat in duration_categories:
                if tasks_generated >= num_tasks:
                    break
                station = random.choice(self.stations)
                task = self.create_task(kpi_info, station, duration_category=duration_cat)
                self.all_tasks.append(task)
                tasks_generated += 1
            
            # 3. Generate remaining tasks
            remaining_tasks = num_tasks - tasks_generated
            num_duplicates = int(remaining_tasks * self.config.duplicate_test_percentage)
            num_regular = remaining_tasks - num_duplicates
            
            # Regular tasks
            for _ in range(num_regular):
                station = random.choice(self.stations)
                task = self.create_task(kpi_info, station)
                self.all_tasks.append(task)
                
                # Store for duplicate creation
                station_code = station['StationCode']
                if station_code not in self.tasks_by_station:
                    self.tasks_by_station[station_code] = []
                self.tasks_by_station[station_code].append(task)
            
            # Duplicate test tasks
            for _ in range(num_duplicates):
                available_stations = [s for s in self.tasks_by_station.keys() 
                                    if self.tasks_by_station[s]]
                if available_stations:
                    station_code = random.choice(available_stations)
                    reference_task = random.choice(self.tasks_by_station[station_code])
                    station = next(s for s in self.stations if s['StationCode'] == station_code)
                    task = self.create_task(kpi_info, station, reference_task=reference_task)
                    self.all_tasks.append(task)
                else:
                    # Fallback
                    station = random.choice(self.stations)
                    task = self.create_task(kpi_info, station)
                    self.all_tasks.append(task)
            
            self.logger.info(f"  ✓ Generated {num_tasks} tasks for {kpi_code}")
        
        # Convert to DataFrame
        df = pd.DataFrame(self.all_tasks)
        
        self.logger.info("="*80)
        self.logger.info(f"Total tasks generated: {len(df)}")
        self.logger.info(f"FY-spanning tasks: {len(self.fy_spanning_tasks)}")
        self.logger.info("="*80)
        
        return df
    
    def validate_data(self, df: pd.DataFrame) -> Dict:
        """
        Validate generated data and return statistics.
        
        Args:
            df: DataFrame containing generated tasks
        
        Returns:
            Dictionary with validation statistics
        """
        self.logger.info("Validating generated data...")
        
        stats = {
            'total_records': len(df),
            'date_range': f"{df['LoggedOn'].min()} to {df['Finished'].max()}",
            'kpi_codes': df['KPIDescription'].nunique(),
            'stations': df['Building'].nunique(),
            'periods': df['Period'].nunique(),
            'status_comp': (df['Status'] == 'COMP').sum(),
        }
        
        # Duration statistics
        df['Duration_Days'] = (df['Finished'] - df['LoggedOn']).dt.total_seconds() / (24 * 3600)
        stats['duration_stats'] = df['Duration_Days'].describe().to_dict()
        
        # Period crossings
        df['Finished_Period'] = df['Finished'].apply(lambda x: self.get_period_info(x)[0])
        period_crossings = (df['Period'] != df['Finished_Period']).sum()
        stats['period_crossings'] = period_crossings
        stats['period_crossing_pct'] = period_crossings / len(df) * 100
        
        # Potential duplicates
        df['LoggedOn_Hour'] = df['LoggedOn'].dt.floor('H')
        duplicates = df.groupby(['Building', 'LoggedOn_Hour']).size()
        stats['duplicate_combinations'] = (duplicates > 1).sum()
        
        # Clean up temporary columns
        df.drop(['Duration_Days', 'Finished_Period', 'LoggedOn_Hour'], axis=1, inplace=True, errors='ignore')
        
        return stats
    
    def save_data(self, df: pd.DataFrame):
        """
        Save generated data to files.
        
        Args:
            df: DataFrame containing generated tasks
        """
        output_dir = Path(self.config.output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"{self.config.output_filename}_{timestamp}"
        
        # Save based on output format
        if self.config.output_format in ['csv', 'both']:
            csv_path = output_dir / f"{base_filename}.csv"
            df.to_csv(csv_path, index=False)
            self.logger.info(f"✓ Saved CSV: {csv_path}")
        
        if self.config.output_format in ['parquet', 'both']:
            parquet_path = output_dir / f"{base_filename}.parquet"
            df.to_parquet(parquet_path, index=False)
            self.logger.info(f"✓ Saved Parquet: {parquet_path}")
        
        # Save metadata
        metadata = {
            'generated_at': timestamp,
            'total_records': len(df),
            'config': asdict(self.config)
        }
        metadata_path = output_dir / f"{base_filename}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        self.logger.info(f"✓ Saved metadata: {metadata_path}")
    
    def generate_status_progression_files(self, df: pd.DataFrame):
        """
        Generate multiple snapshot files with status progression.
        
        Args:
            df: DataFrame containing generated tasks
        """
        if not self.config.simulate_status_progression:
            return
        
        self.logger.info("Generating status progression files...")
        
        output_dir = Path(self.config.output_directory)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for step_idx, status in enumerate(self.config.status_progression_steps):
            df_snapshot = df.copy()
            df_snapshot['Status'] = status
            
            if status != 'COMP':
                df_snapshot['Finished'] = pd.NaT
            
            time_offset = timedelta(hours=step_idx * 24)
            df_snapshot['ModifiedOn'] = df_snapshot['LoggedOn'] + time_offset
            
            filename = f"snapshot_{step_idx + 1}_{status}_{timestamp}.csv"
            filepath = output_dir / filename
            df_snapshot.to_csv(filepath, index=False)
            self.logger.info(f"  ✓ Saved {status} snapshot: {filepath}")
    
    def run(self) -> pd.DataFrame:
        """
        Main execution method.
        
        Returns:
            Generated DataFrame
        """
        # Generate data
        df = self.generate_all_tasks()
        
        # Validate
        stats = self.validate_data(df)
        
        # Log statistics
        self.logger.info("\n" + "="*80)
        self.logger.info("DATA VALIDATION SUMMARY")
        self.logger.info("="*80)
        for key, value in stats.items():
            if key != 'duration_stats':
                self.logger.info(f"{key}: {value}")
        
        # Save data
        self.save_data(df)
        
        # Generate status progression if enabled
        self.generate_status_progression_files(df)
        
        self.logger.info("\n" + "="*80)
        self.logger.info("✨ DATA GENERATION COMPLETED SUCCESSFULLY ✨")
        self.logger.info("="*80)
        
        return df


def load_scenario(scenario_name: str, config: DataGenerationConfig) -> DataGenerationConfig:
    """
    Load a pre-configured scenario and merge with base config.
    
    Args:
        scenario_name: Name of the scenario to load
        config: Base configuration object
    
    Returns:
        Updated configuration object
    """
    if scenario_name not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario_name}. Available: {list(SCENARIOS.keys())}")
    
    scenario_config = SCENARIOS[scenario_name]
    
    # Update config with scenario values
    for key, value in scenario_config.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    return config


if __name__ == "__main__":
    # Example usage
    config = DataGenerationConfig()
    
    # Optional: Load a scenario
    # config = load_scenario('graffiti', config)
    
    generator = DataGenerator(config)
    df = generator.run()
    
    print(f"\n✅ Generated {len(df)} records")
    print(f"📁 Output saved to: {config.output_directory}")
    print(f"\nSample records:")
    print(df.head())
