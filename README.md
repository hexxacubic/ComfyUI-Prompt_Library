# ComfyUI Prompt Library

A collection of ComfyUI nodes for efficient prompt management and organization. Handle multi-line prompts with positive/negative separation, create prompt libraries, and extend prompts dynamically.

![grafik](https://github.com/user-attachments/assets/75f3b72e-13b3-4e3a-9b93-dbde5cc47308)

## Features

- **Double Prompt Format**: All nodes use a unified format where positive and negative prompts are separated by `---` (3-5 dashes)
- **Prompt Libraries**: Organize prompts in text files or directly in nodes
- **Smart Concatenation**: Intelligently combines prompts with proper punctuation
- **Comment Support**: Use `###` at line start for notes that won't be processed

## Nodes

### 🔤 Simple Prompt Library
Store multiple prompt projects directly in a text field within ComfyUI.
- **Projects**: Each project is separated by empty lines
- **Index**: Select which project to use (1, 2, 3, etc.)
- **Randomize**: Randomly select a project
- **Global Prompt**: When enabled, the first project is automatically added to all other projects

**Example:**
```
### Global settings (Project 1)
masterpiece, best quality
---
worst quality, ugly

### Portrait style (Project 2)
portrait photo, face focus
---
full body, cropped head

### Landscape style (Project 3)
scenic landscape, wide angle
---
people, portraits
```

![grafik](https://github.com/user-attachments/assets/bd140e38-8e21-4d97-95d7-2eefac7ec560)

### 📁 Prompt Library
File-based prompt management that reads `.txt` files containing complete scene descriptions.

**Setup:**
1. Navigate to `ComfyUI/models/prompts/`
2. Create folders for different themes/projects (e.g., `fantasy_rpg`, `cyberpunk_scenes`, `nature_photography`)
3. Add `.txt` files with complete scene descriptions
4. Files appear in the dropdown as `folder/filename`

**File Structure Example:**
```
ComfyUI/models/prompts/
├── fantasy_rpg/
│   ├── dungeon_exploration.txt
│   ├── tavern_scene.txt
│   └── boss_battle.txt
├── cyberpunk_scenes/
│   ├── neon_street.txt
│   └── hacker_hideout.txt
└── nature_photography/
    ├── mountain_sunrise.txt
    └── forest_creek.txt
```

**Inside dungeon_exploration.txt:**
```
### Dark Corridor (Project 1)
ancient stone corridor, torchlight, moss covered walls, dripping water, medieval dungeon
---
modern elements, bright lighting, clean surfaces

### Treasure Room (Project 2)
golden treasures, ancient artifacts, mystical glow, dust particles in light rays
---
empty room, poor, modern items

### Monster Encounter (Project 3)
massive stone chamber, lurking shadows, glowing eyes in darkness, battle ready stance
---
peaceful, well lit, safe environment
```

- Each file contains multiple scene variations (projects)
- Projects are separated by empty lines
- Use the **index** parameter to select which scene variation to use

### ➕ Prompt Extender
Add extensions to existing prompts from other nodes.
- **Input**: Connect a double prompt from another node
- **Additions**: Define what to add in the text field
- **Output**: Combined result maintaining the double prompt format

**Usage Example:**
1. Connect Simple Prompt Library output → Prompt Extender input
2. Add extensions like:
   ```
   dramatic lighting, fog atmosphere
   ---
   flat lighting, clear visibility
   ```
3. Result: Original prompts + your additions

### 🎨 Double Prompt Encode
Convert double prompt text directly to CLIP conditioning.
- **Input**: Any text using the `---` separator format
- **Output**: Separate positive and negative conditioning outputs
- Perfect for connecting prompt libraries directly to samplers

## Double Prompt Syntax

All nodes use this unified format:
```
positive prompt content here
---
negative prompt content here
```

- Everything above `---` → Positive prompt
- Everything below `---` → Negative prompt
- No separator → Everything becomes positive prompt
- Separator must be on its own line (3-5 dashes: `---`, `----`, or `-----`)

## Workflow Examples

### Scene-Based Workflow
1. Create a `ComfyUI/models/prompts/game_art/character_portraits.txt` file
2. Add multiple character descriptions separated by empty lines
3. In ComfyUI: **Prompt Library** → set to `game_art/character_portraits` → choose index → **Double Prompt Encode** → Sampler

### Modular Prompt Building
1. **Simple Prompt Library** (base quality settings)
2. → **Prompt Extender** (add environmental details)
3. → **Prompt Extender** (add mood/atmosphere)
4. → **Double Prompt Encode** → Sampler

### Global Prompt Example
With Simple Prompt Library:
- Project 1: `8k, professional photography --- lowres, amateur`
- Project 2: `warrior in armor --- modern clothing`
- Result when using index 2: `8k, professional photography, warrior in armor --- lowres, amateur, modern clothing`

## Tips

- **Comments**: Lines starting with `###` are ignored - perfect for notes
- **Complete Scenes**: Each project should be a complete scene description, not just keywords
- **Organization**: Name folders and files descriptively for your actual projects
- **Testing**: Use randomize to cycle through different scene variations
- **Chaining**: Connect multiple Prompt Extenders to layer details onto base scenes

## Installation

1. Clone to `ComfyUI/custom_nodes/`
2. Restart ComfyUI
3. Find nodes under "hexxacubic" category
