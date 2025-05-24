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
    • seed: integer seed (1-based index), adjustable via arrows
    • control_after_generate: integer spinner (0 = fixed, 1 = increment, 2 = decrement, 3 = randomize)
    Outputs:
    • pos (STRING): selected positive prompt
    • neg (STRING): selected negative prompt
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "entries":                ("STRING", {"multiline": True, "default": ""}),
                "seed":                   ("INT",    {"default": 1, "min": 1}),
                "control_after_generate": (
                    "STRING",
                    {
                        "default": "fixed",
                        "choices": ["fixed","increment","decrement","randomize"]
                    }
                ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    FUNCTION = "random_project"
    OUTPUT_NODE = True
    CATEGORY = "hexxacubic"

    def random_project(self, entries, seed, control_after_generate):
        # Parse entries into sections keyed by integer identifiers
        sections = {}
        current = None
        for line in entries.splitlines():
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("###"):
                try:
                    key = int(line[3:])
                    current = key
                    sections[key] = {"pos": [], "neg": [], "in_neg": False}
                except ValueError:
                    current = None
            elif current is not None:
                if line.strip() == "---":
                    sections[current]["in_neg"] = True
                else:
                    bucket = "neg" if sections[current]["in_neg"] else "pos"
                    sections[current][bucket].append(line)

        # Return empty if no valid sections
        if not sections:
            return "", ""

        # Determine sorted keys
        keys = sorted(sections.keys())
        n = len(keys)

        # Selection logic
        if control_after_generate == 0:  # fixed
            idx = keys[(seed - 1) % n]
        elif control_after_generate == 1:  # increment
            idx = keys[(seed) % n]
        elif control_after_generate == 2:  # decrement
            idx = keys[(seed - 2) % n]
        elif control_after_generate == 3:  # randomize
            random.seed(seed)
            idx = random.choice(keys)
        else:  # fallback
            idx = keys[(seed - 1) % n]

        # Assemble outputs
        data = sections[idx]
        pos = "\n".join(data["pos"]).strip()
        neg = "\n".join(data["neg"]).strip()
        return pos, neg
