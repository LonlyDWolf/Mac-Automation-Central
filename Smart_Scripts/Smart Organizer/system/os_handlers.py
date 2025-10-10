from pathlib import Path
from helpers.utils import get_destination_category, generate_safe_path

# This function is called from main.py
def smart_organizer(target_path: Path):
  """Organize files in the target directory based on their categories."""
  for item in target_path.iterdir():
    
    if not item.is_file():
      continue  # Skip directories or non-files
    
    # 1. Get the category for the file by passing the full Path object
    category_path_string = get_destination_category(item)
    
    # 2. Construct the destination directory path
    destination_dir = target_path / category_path_string
    
    # 3. Create the destination directory if it doesn't exist
    destination_dir.mkdir(parents=True, exist_ok=True)
    
    # 4. Move the file to the destination directory
    new_path = destination_dir / item.name
    # Use a try/expect for robust moving
    try:
      item.rename(new_path)
      print(f"Moved: {item.name} -> {category_path_string}/")
    except OSError as e:
      # Handle cases where the file might already exist or permission issues
      if new_path.exists():
        print(f"\nCollision: {new_path.name} already exists in {new_path.parent.name}/")
        
        move_success = False # Flag to track successful move
        
        while not move_success: # Loop until a file is skipped or successfully renamed
          choice = input("Action: (S)kip, (A)uto_Rename, (C)ustom_Rename? ").upper()
          
          if choice == 'S':
            print(f"Skipped: {item.name}")
            break  # Exit the loop and skip the file
          
          elif choice == 'A':
            final_path = generate_safe_path(new_path)
            item.rename(final_path)
            print(f"Auto-Renamed and Moved: {item.name} -> {final_path.name}")
            move_success = True  # Set flag to True after successful move
            break  # Exit the loop after successful rename and move
          
          elif choice == 'C':
            
            while True:
              
              # 1. Prompt for a custom name
              custom_name = input(f"Enter new name (without extension) for {item.name}: [Press Enter to Cancel] ").strip()
              
              if not custom_name: # Handle empty input
                print("Custom rename cancelled. Going back to actions.")
                break  # Exit to the action choice loop
              
              #2. Construct the custom path
              custom_path = destination_dir / f"{custom_name}{item.suffix}"
              
              verify = input(f"Confirm rename to {custom_path.name}? (Y/N): ").upper()
              if verify == 'Y':
                try:
                  item.rename(custom_path)
                  print(f"Custom-Renamed and Moved: {item.name} -> {custom_path.name}")
                  move_success = True  # Set flag to True after successful move
                  break  # Exit the loop after successful rename and move
                except OSError as e:
                  print(f"Error: The name '{custom_path.name}' still exists or is invalid. Please try again.")
                  continue
              
              elif verify == 'N':
                continue # Prompt for a new name again
              
              else:
                print("Invalid input. Please enter Y or N.")
                continue
          
            if move_success:
              break  # Exit the outer loop if move was successful
          else:
            print("Invalid choice. Please enter S, A, or C.")
            continue  # Prompt for action again
      else:
        # Other OSError cases  
        print(f"Skipping {item.name}. Error during move: {e}")