import random
import time
import os

class RandomLineNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "select_random_line"
    CATEGORY = "hexxacubic"

    def select_random_line(self, text, unique_id=None):
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        
        if not lines:
            return ("",)
        
        # Create truly unique, non-deterministic seed per node instance + run
        base = int(time.time() * 1000000)  # microsecond precision
        entropy = int.from_bytes(os.urandom(8), 'big')
        final_seed = base ^ entropy ^ hash(str(unique_id))
        
        rand = random.Random(final_seed)
        selected_line = rand.choice(lines)
        
        if selected_line and not selected_line.endswith(","):
            selected_line += ","
        
        return (selected_line,)

NODE_CLASS_MAPPINGS = {
    "RandomLine": RandomLineNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomLine": "Random Line"
}
