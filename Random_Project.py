import random
import hashlib

class Random_Project:
    """
    Random Project Node:
    • entries: Multiline-String mit Einträgen im Format
        ###X
        positive Prompt-Zeilen
        ---
        negative Prompt-Zeilen
      für beliebige X (nicht zwangsläufig lückenlos).
    • seed: String (beliebige Länge), wird per SHA256 → Integer gemappt.
    • control_after_generate: "randomize" oder "seed"
        - randomize: wähle echt zufällig (wenn seed gesetzt, initialisiere RNG damit)
        - seed: deterministische Auswahl via (seed_int-1) % Anzahl_Einträge
    Outputs:
    • pos (STRING): positiver Prompt
    • neg (STRING): negativer Prompt
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "entries":                ("STRING", {"multiline": True, "default": ""}),
                "seed":                   ("STRING", {"default": ""}),
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

        # 2) Seed-String → Integer via SHA256 (0 bei leerem String)
        if seed:
            h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
            seed_int = int(h, 16)
        else:
            seed_int = 0

        # sortierte Keys für Modulo-Logik
        sorted_keys = sorted(sections.keys())

        # 3) Auswahl
        if control_after_generate == "randomize":
            # wenn ein seed kommt, initialisiere RNG damit
            if seed_int:
                random.seed(seed_int)
            idx = random.choice(sorted_keys)
        else:  # control_after_generate == "seed"
            # (seed_int-1) mod N → wählt eine deterministische Position
            idx = sorted_keys[(seed_int - 1) % len(sorted_keys)]

        # 4) Prompt-Zeilen zusammensetzen
        chosen = sections[idx]
        pos = "\n".join(chosen["pos"]).strip()
        neg = "\n".join(chosen["neg"]).strip()
        return pos, neg
