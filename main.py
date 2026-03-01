import json
import sys
import os
from typing import Dict, Any

from dashboard import print_header, print_section, display_config

from input import create_reader
from output import ConsoleWriter, FileWriter, GraphicsChartWriter, HTMLReportWriter
from core.contracts import DataSink, PipelineService
from core.engine import TransformationEngine


INPUT_DRIVERS = {
    'csv': 'CSVReader',
    'json': 'JSONReader', 
    'excel': 'ExcelReader'
}

OUTPUT_DRIVERS = {
    'console': ConsoleWriter,
    'file': FileWriter,
    'chart': GraphicsChartWriter,
    'html': HTMLReportWriter
}


def load_config(config_path: str = 'config.json') -> Dict[str, Any]:
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f" Config file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f" Invalid JSON: {str(e)}")
        sys.exit(1)

def validate_config(config: Dict[str, Any]) -> bool:
    required = ['input_file', 'output_type']
    missing = [field for field in required if field not in config]
    
    if missing:
        print(f" Missing config fields: {', '.join(missing)}")
        return False
    
    if config['output_type'] not in OUTPUT_DRIVERS:
        print(f" Invalid output_type: {config['output_type']}")
        return False
    
    return True

def bootstrap():

    print_header("GDP ANALYSIS SYSTEM - PHASE 2")
    
    try:
        print_section("LOADING CONFIGURATION")
        config = load_config()
        
        if not validate_config(config):
            sys.exit(1)
        
        print(" Configuration loaded\n")
        display_config(config)
        
        config.setdefault('region', 'Asia')
        config.setdefault('year', 2020)
        config.setdefault('operation', 'sum')
        config.setdefault('date_range', [2000, 2020])
        config.setdefault('decline_years', 5)
        
        print_section("INITIALIZING INPUT READER")
        try:
            reader = create_reader(config['input_file'])
            file_ext = os.path.splitext(config['input_file'])[1].upper()
            print(f" {file_ext} reader initialized\n")
        except Exception as e:
            print(f" Error: {str(e)}")
            sys.exit(1)
        
        print_section("READING DATA")
        try:
            raw_data = reader.read()
            reader.validate(raw_data)
            print(f" Data validated: {len(raw_data)} records\n")
        except Exception as e:
            print(f" Error: {str(e)}")
            sys.exit(1)
        
        print_section("INITIALIZING OUTPUT WRITER")
        try:
            output_type = config['output_type']
            
            if output_type == 'file':
                writer = FileWriter(
                    config.get('output_file', 'output.csv'),
                    config.get('output_format', 'csv')
                )
            elif output_type == 'chart':
                writer = GraphicsChartWriter(
                    config.get('output_dir', 'visualizations')
                )
            elif output_type == 'html':
                writer = HTMLReportWriter(
                    config.get('output_file', 'report.html')
                )
            else:  
                writer = ConsoleWriter()
            
            if not isinstance(writer, DataSink):
                print(f" Writer may not fully implement DataSink protocol")
            
            print(f" {output_type.upper()} writer initialized\n")
            
        except Exception as e:
            print(f" Error: {str(e)}")
            sys.exit(1)
        
  
        print_section("INITIALIZING TRANSFORMATION ENGINE")
        try:
            engine = TransformationEngine(sink=writer, config=config)
            
            if not isinstance(engine, PipelineService):
                print(f" Engine may not fully implement PipelineService protocol")
            
            print(" Engine initialized with injected dependencies\n")
            
        except Exception as e:
            print(f" Error: {str(e)}")
            sys.exit(1)
        
        print_section("EXECUTING PIPELINE")
        try:
            engine.execute(raw_data)
            
        except Exception as e:
            print(f" Error during execution: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        print("\n" + "="*80)
        print(" PIPELINE COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    bootstrap()