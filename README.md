# OTH Guide AI

OTH Guide AI is a chatbot for questions about OTH Regensburg. It uses the internal
OTH Regensburg OpenWebUI service as its language model and extends it with additional
skills for university-related questions. The chatbot can provide basic university
information, current canteen menus, timetable data, information from official OTH and
StuV web pages, and explanations of important university terms. It can also connect
German terms with their English translations and common abbreviations.

The project contains two application versions:

* a console application, which is mainly intended for testing;
* a web application with a graphical interface, which is the main version intended
  for normal use.

## Project Structure

The project is divided into three main directories: `backend`, `frontend`, and `tests`.
The root directory also contains the documentations, `requirements.txt`, and
`.gitignore`:

```text
oth_guide_ai/
├── backend/
│   ├── logs/
│   │   └── app.log
│   ├── app.py
│   ├── basic_info.py
│   ├── basic_info.txt
│   ├── chat_history.json
│   ├── chat_storage.py
│   ├── chatbot.py
│   ├── config.py
│   ├── data.py
│   ├── keyword_manager.py
│   ├── language.py
│   ├── logger.py
│   ├── main.py
│   ├── mensa.py
│   ├── oth_website.py
│   ├── stundenplan.py
│   ├── stuv.py
│   └── utils.py
├── frontend/
│   ├── index.html
│   ├── index.js
│   └── style.css
├── tests/
│   └── test_project.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── SKILL_IMPLEMENTATION.md
```

The `backend` directory contains all Python files, the local chat history, and the
application logs. The `frontend` directory contains the HTML, CSS, and JavaScript files
required for the web interface, while the `tests` directory contains the Python unit
tests for the project.

## Requirements

Both application versions require Python and the external libraries listed in
`requirements.txt`. The chatbot communicates with an internal OTH Regensburg service,
so both the console application and the web application require a connection to the
OTH Regensburg network or to the OTH VPN through FortiClient.

Information about installing and configuring FortiClient can be found in the official
OTH Regensburg VPN documentation. A personal API key for the OTH OpenWebUI service
is also required and can be created in the account settings.

## Installation

First, download or clone the complete project repository. Then open a terminal in the
project root directory and install all required libraries:

```cmd
pip install -r requirements.txt
```

The libraries listed in `requirements.txt` are external Python libraries. Standard
Python modules such as `json`, `pathlib`, `unittest`, `tempfile`, and `sys` do not need
to be installed separately.

Before starting either application, create a `.env` file in the project root using
`.env.example` as a template. This file must contain three settings: `BASE_URL` (the OTH
OpenWebUI service URL), `API_KEY` (your personal API key from the OpenWebUI account
settings), and `MODEL` (the model to use). You can copy the URL and default model from
`.env.example`, or choose another available model on the OTH OpenWebUI server. The
`backend/config.py` module loads these settings. Keep your `.env` file private. It is
excluded from Git by `.gitignore`.

## Console Application

The console application is mainly intended for testing the chatbot and its skills.
Open a terminal in the `backend` directory and run:

```cmd
python main.py
```

After the application starts, messages can be entered directly into the terminal and
the chatbot answers in the same terminal, so the console version can be used like a
simple text chat.

## Web Application

The web application is the main version of OTH Guide AI. First, open a terminal in the
`backend` directory and start the Flask server:

```cmd
python app.py
```

The backend server runs locally on port `5000`. After that, open
`frontend/index.html` in a web browser. The frontend communicates with the running
Flask backend and can then be used like a normal online chatbot. The terminal running
`app.py` must remain open while the web application is being used.

## Web Interface

The web interface contains a sidebar, a chat area, and a message input field. To open
the welcome page and create a new conversation, press the `New Chat` button in the
sidebar or reload the page. The sidebar can be collapsed and expanded with the button
next to the application name, and it also contains a list of saved chats loaded from
the chat history.

A saved chat can be opened by clicking its title, while the delete button next to the
title removes the selected chat from the history. Each new chat receives a unique
numerical ID, beginning with `1`, and its title is generated from this ID, for example
`Chat #1`, `Chat #2`, and so on.

Saved conversations are stored in:

```text
backend/chat_history.json
```

This file can be opened manually to inspect the stored chat IDs, titles, and messages.
Manual editing is possible but not recommended, because invalid JSON formatting may
prevent the chat history from loading correctly. The settings button and the user
profile circle are currently visual interface elements only and do not provide
additional functionality.

## Sending Messages

Enter a question in the message field and press the arrow button to send it. A message
can also be sent by pressing `Enter`, while `Shift + Enter` creates a new line instead
of sending the message. Empty messages cannot be sent.

While the chatbot is generating an answer, a temporary `Thinking...` message is
displayed with an animated gradient. Some answers may take longer, especially when the
request activates several skills or requires large external data sources. During this
time, sending another message and switching between chats are temporarily disabled to
prevent several requests from changing the same active conversation. After the answer
is complete, normal interaction becomes available again.

## Chat History

Chats are saved automatically after messages are processed. The sidebar loads the
available chat titles from `backend/chat_history.json`, and users can switch between
saved chats and continue previous conversations. A chat can be deleted by clicking the
delete icon next to its title, and if the currently opened chat is deleted, the
application returns to the empty welcome page.

## Skills

The chatbot automatically selects relevant skills based on the words and terms in the
user request. It also expands important university terms with English translations and
abbreviations stored in the language glossary. Fuzzy matching helps the program
recognise small spelling mistakes, so the correct skill can still be activated even
when a term is not written perfectly.

Available skills include:

* basic OTH information;
* current canteen menus;
* timetable information;
* official OTH website information;
* StuV and student-life information;
* university language and terminology support.

Skills can also be activated manually for testing by writing a slash command in the
request, for example:

```text
/mensa
```

```text
/stundenplan
```

```text
/stuv
```

A manual command is treated as a keyword and forces the related skill to be included
in the request.

## Logging

The application stores runtime information in:

```text
backend/logs/app.log
```

The log contains information about application starts, activated skills, loaded
resources, saved or deleted chats, warnings, and errors. It can be opened at any time
to check which skills were used, whether external information was loaded correctly, or
whether a function failed.

## Tests

The project contains unit tests in:

```text
tests/test_project.py
```

To run all tests, open a terminal in the project root directory and use:

```cmd
python -m unittest discover -s tests -v
```

A successful test run ends with output similar to:

```text
Ran 27 tests in ...
OK
```

The tests check deterministic parts of the application, including keyword recognition,
language-term expansion, resource configuration, local file reading, and chat-history
operations. They do not send requests to the LLM because external model answers can
change, depend on the network connection, and may take a long time.

## Skill Extension

New skills can be added without rebuilding the whole application. Detailed instructions
about creating a new skill file, registering keywords, using helper functions, adding
optional prompts, connecting the skill, adding logging, and writing tests are available
in:

```text
SKILL_IMPLEMENTATION.md
```
