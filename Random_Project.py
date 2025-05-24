import random

class Random_Project:
    """
    Random Project Node:
    • Ein Textfeld “entries” mit Einträgen im Format:
        ###1
        positive Prompt-Zeilen
        ---
        negative Prompt-Zeilen

        ###2
        …
    • seed: ganzzahliger Seed für deterministische Auswahl (0 = kein Seed)
    • index: feste Auswahl (wenn randomize=0)
    • randomize: 0 = nutze index, 1 = wähle zufällig
    Outputs:
    • pos (STRING): ausgewählter positiver Prompt
    • neg (STRING): zugehöriger negativer Prompt
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "entries":   ("STRING", {"multiline": True, "default": ""}),
                "seed":      ("INT",    {"default": 0, "min": 0}),
                "index":     ("INT",    {"default": 1, "min": 1}),
                "randomize": ("INT",    {"default": 1, "min": 0, "max": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    FUNCTION     = "random_project"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    def random_project(self, entries, seed, index, randomize):
        # Parse entries nach ###Num / --- Struktur
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
                    if sections[current]["in_neg"]:
                        sections[current]["neg"].append(line)
                    else:
                        sections[current]["pos"].append(line)

        if not sections:
            return "", ""

        # Seed setzen, falls gewünscht
        if seed:
            random.seed(seed)

        # Auswahl des Index
        if randomize == 1:
            idx = random.choice(list(sections.keys()))
        else:
            idx = index

        chosen = sections.get(idx)
        if not chosen:
            return "", ""

        pos = "\n".join(chosen["pos"]).strip()
        neg = "\n".join(chosen["neg"]).strip()
        return pos, neg
