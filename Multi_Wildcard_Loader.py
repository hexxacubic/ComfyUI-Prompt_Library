import os
import random
import folder_paths

class Multi_Wildcard_Loader:
    """
    Multi Wildcard Loader - Load and randomly select from up to 4 wildcard files
    • Select up to 4 different wildcard files
    • Randomly picks one line from each selected file
    • Combines selections with commas
    • Use "none" to skip a wildcard slot
    """
    
    def __init__(self):
        self.wildcards_dir = os.path.join(folder_paths.base_path, "wildcards")
        if not os.path.exists(self.wildcards_dir):
            os.makedirs(self.wildcards_dir)
    
    @classmethod
    def INPUT_TYPES(s):
        instance = s()
        wildcard_files = instance.get_wildcard_files()
        
        return {
            "required": {
                "wildcard_1": (wildcard_files,),
                "wildcard_2": (wildcard_files,),
                "wildcard_3": (wildcard_files,),
                "wildcard_4": (wildcard_files,),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("wildcards",)
    FUNCTION = "load_wildcards"
    CATEGORY = "hexxacubic"
    
    def get_wildcard_files(self):
        """Get list of all wildcard text files"""
        wildcard_files = []  # Start with empty list
        
        # Walk through wildcards directory
        for root, dirs, files in os.walk(self.wildcards_dir):
            for file in files:
                if file.endswith('.txt'):
                    # Get relative path from wildcards directory
                    rel_path = os.path.relpath(os.path.join(root, file), self.wildcards_dir)
                    # Convert backslashes to forward slashes for consistency
                    rel_path = rel_path.replace('\\', '/')
                    wildcard_files.append(rel_path)
        
        return ["none"] + sorted(wildcard_files)
    
    def load_random_line(self, filepath):
        """Load a random line from the specified file"""
        if filepath == "none":
            return None
            
        full_path = os.path.join(self.wildcards_dir, filepath)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                # Read all non-empty lines
                lines = [line.strip() for line in f.readlines() if line.strip()]
                
            if lines:
                # Return random line
                return random.choice(lines)
        except Exception as e:
            print(f"Error reading wildcard file {filepath}: {e}")
            
        return None
    
    def load_wildcards(self, wildcard_1, wildcard_2, wildcard_3, wildcard_4):
        """Load random lines from selected wildcard files and combine them"""
        selected_wildcards = []
        
        # Process each wildcard selection
        for wildcard_file in [wildcard_1, wildcard_2, wildcard_3, wildcard_4]:
            line = self.load_random_line(wildcard_file)
            if line:
                selected_wildcards.append(line)
        
        # Combine with commas
        result = ", ".join(selected_wildcards) if selected_wildcards else ""
        
        return (result,)
    
    @classmethod
    def IS_CHANGED(s, wildcard_1, wildcard_2, wildcard_3, wildcard_4):
        # Always return a different value to ensure random selection on each run
        return float("nan")
