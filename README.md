A custom node for comfy UI.
The prompt library node gives you the ability to load prompt projects.
In the folder '/models/prompts' there are your category folders. In these category folders there should be your prompt project files.
A prompt project file can store 99 projects or variations. The marker for the project index number is ### and the marker before the negative prompt is ---

Project file path example:
/models/prompts/animals/cute_dog.txt


Here an example how a prompt project file should look.
Note: GitHub may automatically apply unintended formatting to the example syntax below (e.g., headers or horizontal lines). This is purely a visual issue and does not affect the actual file structure or functionality.

###1
cute dog, depth of field, (bokeh:0.3), plants in background, (park:0.5),
professional photo, high quality, dog portrait, animal photography
---
cat, horse, night, indoor, interior, simple background, boring background

###2
cute dog, depth of field, high quality, living room, dog on sofa, sunlight
---
outdoor, bad quality

