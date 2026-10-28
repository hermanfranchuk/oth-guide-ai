## Skill Implementation Documentation

The chatbot has a modular structure, so additional skills can be implemented without
changing the whole application. A skill is responsible for one specific area, for example
basic university information, current canteen data, etc., while most helper functions
needed for reading and preparing external information are already available in other
project files.

The first step is to create a separate Python file for the new skill. This file should
contain the main logic of the skill and return the information that will later be added
to the LLM messages. If the skill needs external information, helper functions from
`utils.py` can be imported directly:

```python
from utils import read_text_file, download_json_text, download_html_page_text
```

`read_text_file(file_path)` reads a local text file and returns its content as a string,
`download_json_text(url)` downloads JSON data and converts it into readable formatted
text for further use, and `download_html_page_text(page)` downloads an HTML page,
removes unnecessary elements such as scripts, styles, navigation and footer, and returns
readable page text together with the source title and source URL. These helper functions
already contain logging and error handling, so the same loading logic should not be
duplicated inside the skill file.

The next step is to add keywords for the automatic activation of the skill to `data.py`.
A keyword list can contain a manual command, normal words and multi-word expressions,
for example:

```python
YOUR_SKILL_KEYWORDS = [
    "/yourskill",
    "keyword1",
    "keyword2",
    "keyword3",
    # additional keywords
]
```

After that, register the list in the `SKILL_KEYWORDS` management table:

```python
SKILL_KEYWORDS = {
    # existing skills
    "YOUR_SKILL": YOUR_SKILL_KEYWORDS
}
```

The string `"YOUR_SKILL"` is the internal tag that connects the keyword list with
`keyword_match()` from `keyword_manager.py`. The keyword manager automatically expands
detected terms with their English translations and abbreviations stored in
`LANGUAGE_TERMS`, and it also uses fuzzy matching, so separate keyword entries for every
small spelling mistake are usually not required. If a term belongs to the general OTH
vocabulary but is not yet available in `LANGUAGE_TERMS`, it is better to add it there
with its German term, English translation, abbreviation and optional explanation, for
example:

```python
{
    "german": "Studierenden-Service-Portal",
    "english": "student service portal",
    "abbreviation": "SSP",
    "explanation": "Online portal for student documents, exam registration and grades."
}
```

A separate system prompt for the skill can also be added to `data.py`. This is optional
and mainly useful when the skill loads complex information that the LLM must interpret
carefully, because the prompt can explain the structure of the data, important
restrictions, the expected answer format and information that must not be invented.
A simple skill that returns clear and direct information may not need its own prompt.

If you create a more complex skill that uses several website sections or external
resources, every resource should have its own tag, title and URL, and every tag should
have a corresponding keyword list. `WEBSITE_PAGES` and `STUV_PAGES` can be used as
examples, since the website skill contains separate sections such as `WEB_TERMINE` and
`WEB_STANDORT`. This structure allows the program to load only relevant sources instead
of sending the complete website content with every request. For example:

```python
YOUR_SKILL_PAGES = [
    {
        "tag": "YOUR_SKILL_SECTION_ONE",
        "title": "First section",
        "url": "https://example.com/section-one"
    },
    {
        "tag": "YOUR_SKILL_SECTION_TWO",
        "title": "Second section",
        "url": "https://example.com/section-two"
    }
]
```

After the skill file and its configuration in `data.py` are ready, connect the skill to
the web application in `chatbot.py` and to the console application in `main.py`. It is
recommended to support the skill in both versions. First, import the required functions
from the new skill file:

```python
from your_skill import your_skill_info
```

In `chatbot.py`, add the automatic skill check inside `get_bot_answer(user_input)`,
while in `main.py`, add the same check inside the main conversation loop near the
existing skill checks:

```python
use_your_skill = keyword_match(user_input, "YOUR_SKILL")
```

Then add the new boolean flag to `ask_llm(...)` in both files and add a condition inside
`ask_llm(...)` that inserts the skill information when the flag is active:

```python
if use_your_skill:
    debug_print("your skill data will be added to prompt")
    messages.insert(1, {
        "role": "system",
        "content": your_skill_info()
    })
```

A manual command such as `/yourskill` should also be included in the keyword list,
because this gives the user a direct way to activate the skill and makes manual testing
easier, while automatic matching still works with all other keywords.

New methods should use the project logger. Import it with:

```python
from logger import logger
```

Successful actions can be written with debug or info messages, while failed operations
should use warnings or exceptions. Logging and error handling are already implemented
inside the helper functions from `utils.py`, so they should not be added again to the
skill file, while additional logging is mainly needed for new logic that is not covered
by existing helper functions.

New skills should also receive simple unit tests. Tests should check deterministic parts
of the implementation and should not send real requests to the LLM. Useful tests include
checking whether a representative user input activates the correct skill tag, whether
required files or URLs are configured, whether local test data can be loaded, and whether
a complex skill selects the correct subpage. External LLM answers should be checked
manually because they can change between requests and depend on an external API.

In summary, adding a new skill normally requires creating a separate skill file, adding
the required data configuration and keywords to `data.py` with an optional system prompt,
registering the keyword list in `SKILL_KEYWORDS`, implementing the skill logic and loading
the required data with helper functions from `utils.py`, importing and connecting the
skill in `chatbot.py` and preferably in `main.py`, adding logging for new logic, and
creating small unit tests.
