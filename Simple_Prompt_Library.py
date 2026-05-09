import random
import time

class Simple_Prompt_Library:
    """
    Simple Prompt Library – Text field + seed only
    • Empty lines separate projects (no empty lines inside a project)
    • Lines starting with ### are project titles/comments → ignored in output
    • --- or ---- separates positive/negative prompt (can be mid-line)
    • Positive prompt can be empty → separator at start allowed
    • No separator → entire text treated as positive prompt
    • Seed behavior:
        - -1 → random project (time-based seed), UI remains -1
        - 0 or 1 → first project
        - 1–999 → project index (1-based); if index exceeds count → treat as seed
        - ≥1000 → always treat as random seed
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_text": ("STRING", {
                    "multiline": True,
                    "default": "### Masterpiece\nmasterpiece, best quality --- low quality, blurry"
                }),
                "random_seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("prompt", "used_seed")
    FUNCTION = "get_prompt"
    CATEGORY = "hexxacubic"

    def get_prompt(self, prompt_text, random_seed, **kwargs):
        if not prompt_text.strip():
            return ("", random_seed)

        # --- 1. Parse projects: empty line = project boundary ---
        projects = []
        current_lines = []

        for line in prompt_text.split('\n'):
            stripped = line.strip()

            # Empty line ends current project
            if not stripped:
                if current_lines:
                    projects.append(current_lines)
                    current_lines = []
                continue

            # ### lines are titles/comments → keep in block but ignore in output
            if stripped.startswith("###"):
                current_lines.append("")  # placeholder to maintain block structure
                continue

            # Regular line → preserve original formatting
            current_lines.append(line)

        # Append final project
        if current_lines:
            projects.append(current_lines)

        if not projects:
            return ("", random_seed)

        num_projects = len(projects)
        available_indices = list(range(1, num_projects + 1))

        # --- 2. Seed / Index logic ---
        used_seed = random_seed
        project_idx = 1

        if random_seed == -1:
            # Random selection with time-based seed
            actual_seed = int(time.time() * 1000000) % 0xffffffffffffffff
            gen = random.Random(actual_seed)
            project_idx = gen.choice(available_indices)
            used_seed = -1  # UI stays -1
        elif random_seed >= 1000:
            # High values → treat as seed
            gen = random.Random(random_seed)
            project_idx = gen.choice(available_indices)
            used_seed = random_seed
        else:
            # 0 or 1–999: try as 1-based index
            desired_idx = 1 if random_seed <= 0 else random_seed
            if desired_idx <= num_projects:
                project_idx = desired_idx
                used_seed = random_seed
            else:
                # Index out of range → fall back to seed
                gen = random.Random(random_seed)
                project_idx = gen.choice(available_indices)
                used_seed = random_seed

        # --- 3. Build selected project (exclude ### lines) ---
        selected_lines = projects[project_idx - 1]
        clean_lines = []

        for line in selected_lines:
            if line.strip().startswith("###"):
                continue  # skip title lines in output
            if line != "":  # skip placeholder empty lines
                clean_lines.append(line)

        raw_project = '\n'.join(clean_lines).strip()
        if not raw_project:
            return ("", used_seed)

        # --- 4. Split positive / negative ---
        separator = None
        if '----' in raw_project:
            separator = '----'
        elif '---' in raw_project:
            separator = '---'

        if separator:
            pos_part, neg_part = raw_project.split(separator, 1)
            pos = pos_part.strip()
            neg = neg_part.strip()
            if pos:
                result = f"{pos}{separator}{neg}"
            else:
                result = f"{separator}{neg}"  # allow empty positive
        else:
            result = raw_project  # all positive

        return (result, used_seed)

    @classmethod
    def IS_CHANGED(s, prompt_text, random_seed, **kwargs):
        if random_seed == -1:
            return float("nan")
        return hash(prompt_text + str(random_seed))
