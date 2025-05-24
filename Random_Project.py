import random

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
        - "randomize": choose a truly random entry (RNG can be seeded via 'seed')
        - "seed": deterministic selection using (seed - 1) % number_of_entries
    Outputs:
    • pos (STRING): selected positive prompt
    • neg (STRING): selected negative prompt
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "entries": {
                    "type": "STRING",
                    "multiline": True,
                    "default": ""
                },
                "seed": {
                    "type": "INT",
                    "default": 0,
                    "min": 0
                },
                "control_after_generate": {
                    "type": "STRING",
                    "default": "randomize",
                    "choices": ["randomize", "seed"]
                }
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    FUNCTION     = "random_project"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    def random_project(self, entries, seed, control_after_generate):
        # Parse entries into sections keyed by integer identifiers
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

        # Return empty outputs if no valid sections found
        if not sections:
            return "", ""

        # Sort the available section keys for consistent ordering
        sorted_keys = sorted(sections.keys())

        # Choose the target section
        if control_after_generate == "randomize":
            if seed:
                random.seed(seed)
            idx = random.choice(sorted_keys)
        else:  # control_after_generate == "seed"
            idx = sorted_keys[(seed - 1) % len(sorted_keys)]

        # Build and return the outputs
        chosen = sections[idx]
        pos = "\n".join(chosen["pos"]).strip()
        neg = "\n".join(chosen["neg"]).strip()
        return pos, neg
