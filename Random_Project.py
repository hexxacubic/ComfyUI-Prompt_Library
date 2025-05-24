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
    • control_after_generate: dropdown selection with choices:
        - "fixed": deterministic selection using (seed - 1) % number_of_entries
        - "increment": selection at position (seed) % number_of_entries
        - "decrement": selection at position (seed - 2) % number_of_entries
        - "randomize": random selection (RNG seeded by seed if provided)
    Outputs:
    • pos (STRING): selected positive prompt
    • neg (STRING): selected negative prompt
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "entries": ("STRING", {"multiline": True, "default": ""}),
                "seed":    ("INT",    {"default": 1, "min": 1}),
                "control_after_generate": (
                    "STRING",
                    {
                        "default": "fixed",
                        "choices": ["fixed", "increment", "decrement", "randomize"]
                    }
                ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    FUNCTION     = "random_project"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    def random_project(self, entries, seed, control_after_generate):
        # parse entries into sections keyed by integer identifiers
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

        # return empty strings if no valid sections found
        if not sections:
            return "", ""

        # sorted keys ensures consistent ordering
        keys = sorted(sections.keys())
        n = len(keys)

        # determine selection index based on control_after_generate
        if control_after_generate == "fixed":
            idx = keys[(seed - 1) % n]
        elif control_after_generate == "increment":
            idx = keys[(seed) % n]
        elif control_after_generate == "decrement":
            idx = keys[(seed - 2) % n]
        elif control_after_generate == "randomize":
            if seed:
                random.seed(seed)
            idx = random.choice(keys)
        else:
            # fallback to fixed
            idx = keys[(seed - 1) % n]

        # assemble and return prompts
        data = sections[idx]
        pos = "\n".join(data["pos"]).strip()
        neg = "\n".join(data["neg"]).strip()
        return pos, neg
