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
    • seed: integer seed (0 = no seed), adjustable via arrows
    • control_after_generate: integer spinner (0 = random selection, 1 = deterministic seed-mode)
        - 0: random selection (seed seeds RNG if >0)
        - 1: deterministic selection using (seed - 1) % number_of_entries
    Outputs:
    • pos (STRING): selected positive prompt
    • neg (STRING): selected negative prompt
    """

    @classmethod
    def INPUT_TYPES(cls):(cls):
        return {
            "required": {
                "entries":                ("STRING", {"multiline": True, "default": ""}),
                "seed":                   ("INT",    {"default": 0, "min": 0}),
                "control_after_generate": ("INT",    {"default": 0, "min": 0, "max": 1}),
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

        # return empty if no entries
        if not sections:
            return "", ""

        # determine valid keys in sorted order
        keys = sorted(sections.keys())

        # choose index based on control flag
        if control_after_generate == 0:
            if seed:
                random.seed(seed)
            choice = random.choice(keys)
        else:
            choice = keys[(seed - 1) % len(keys)]

        # assemble prompts
        data = sections[choice]
        pos = "\n".join(data["pos"]).strip()
        neg = "\n".join(data["neg"]).strip()
        return pos, neg
