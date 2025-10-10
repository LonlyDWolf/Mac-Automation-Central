import argparse
import sys
from pathlib import Path

from system.os_handlers import smart_organizer

from config.setting import DEFAULT_TARGET_PATH

def parse_arguments():
  """Parse command line arguments. for the folder to organize."""
  parser = argparse.ArgumentParser(
    description="A smart, AI-powered file organizer."
  )
  parser.add_argument(
    "target_path",
    type=Path,
    help="The path to the folder to organize.",
    nargs='?',
    default=DEFAULT_TARGET_PATH
  )
  
  args = parser.parse_args()
  return args

def main():
  """Main execution function."""
  
  # 1. Get the parsed arguments
  args = parse_arguments()
  target_path: Path = args.target_path
  
  print(f"Starting smart organization for: {target_path}")
  
  # 2. Validate the target path
  if not target_path.exists() or not target_path.is_dir():
    print(f"Error: The path '{target_path}' does not exist or is not a directory.")
    sys.exit(1) # Exit with error code
    
  # 3. Call the core logic (system/os_handlers.py)
  try:
    smart_organizer(target_path)
    print("Organization complete.")
  except Exception as e:
    print(f"An error occurred during organization: {e}", file=sys.stderr)
    sys.exit(1) # Exit with error code
    
if __name__ == "__main__":
  main()