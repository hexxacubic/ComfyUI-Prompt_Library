import random
import hashlib

class Random_Project:
    """
    Random Project Node:
    • entries: multiline string containing entries in the format:
        ###X
        positive prompt lines
        ---
        negative prompt lines
      for arbitrary X values (not necessarily contiguous).
    • seed: integer seed (0 = no seed), adjustable via arrows or keyboard input
    • control_after_generate: dropdown selection with arrows
        - "randomize": choose a truly random entry (if seed is provided, RNG is seeded accordingly)
        - "seed": deterministic selection using (seed - 1) % number_of_entries
    Outputs:
    • pos (STRING): selected positive prompt
    • neg (STRING): selected negative prompt
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "entries": ("STRING", {"multiline": True, "default": ""}),
                "seed":    ("INT",    {"default": 0, "min": 0}),
                "control_after_generate": (
                    "STRING",
                    {
                        "default": "randomize",
                        "choices": ["randomize", "seed"]
                    }
                ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    FUNCTION     = "random_project"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    def random_project(self, entries, seed, control_after_generate):
        # Parse the entries into sections keyed by integer identifiers
        sections = {}
        current = None
        for raw_line in entries.splitlines():
            line = raw_line.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("###"):
                try:
                    section_id = int(line[3:])
                    current = section_id
                    sections[current] = {"pos": [], "neg": [], "in_neg": False}
                except ValueError:
                    current = None
            elif current is not None:
                if line.strip() == "---":
                    sections[current]["in_neg"] = True
                else:
                    bucket = "neg" if sections[current]["in_neg"] else "pos"
                    sections[current][bucket].append(line)

        # If no valid sections are found, return empty strings
        if not sections:
            return "", ""

        # Sort the available section keys
        sorted_keys = sorted(sections.keys())

        # Determine which section to choose
        if control_after_generate == "randomize":
            # Seed the RNG if provided
            if seed:
                random.seed(seed)
            idx = random.choice(sorted_keys)
        else:  # control_after_generate == "seed"
            # Use modulo to wrap the seed to a valid index
            idx = sorted_keys[(seed - 1) % len(sorted_keys)]

        # Build the output prompts
        chosen = sections[idx]
        pos = "\n".join(chosen["pos"]).strip()
        neg = "\n".join(chosen["neg"]).strip()
        return pos, neg
