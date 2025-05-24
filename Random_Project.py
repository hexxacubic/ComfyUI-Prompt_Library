import random

class Random_Project:
    """
    Random Project Node:
    • entries: Multiline-String mit Einträgen im Format
        ###X
        positive Prompt-Zeilen
        ---
        negative Prompt-Zeilen
      für beliebige X (nicht zwingend zusammenhängend).
    • seed: Ganzzahliger Seed (0 = kein Seed)
    • control_after_generate: "randomize" oder "seed"
        - randomize: wähle zufällig (optional vorinitialisiert mit seed)
        - seed: deterministische Auswahl via Wrap-Modulo
    Outputs:
    • pos (STRING): positiver Prompt
    • neg (STRING): negativer Prompt
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "entries":                ("STRING", {"multiline": True, "default": ""}),
                "seed":                   ("INT",    {"default": 0, "min": 0}),
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
        # 1) Einträge parsen
        sections = {}
        current = None
        for raw in entries.splitlines():
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("###"):
                try:
                    num = int(line[3:])
                    current = num
                    sections[current] = {"pos": [], "neg": [], "in_neg": False}
                except ValueError:
                    current = None
            elif current is not None:
                if line.strip() == "---":
                    sections[current]["in_neg"] = True
                else:
                    bucket = "neg" if sections[current]["in_neg"] else "pos"
                    sections[current][bucket].append(line)

        if not sections:
            return "", ""

        # 2) Auswahl des Keys
        sorted_keys = sorted(sections.keys())

        if control_after_generate == "randomize":
            if seed:
                random.seed(seed)
            idx = random.choice(sorted_keys)
        else:  # control_after_generate == "seed"
            # wrap mit Modulo auf die Länge der vorhandenen Keys
            idx = sorted_keys[(seed - 1) % len(sorted_keys)]

        # 3) Prompt-Zeilen zusammensetzen
        chosen = sections[idx]
        pos = "\n".join(chosen["pos"]).strip()
        neg = "\n".join(chosen["neg"]).strip()
        return pos, neg
