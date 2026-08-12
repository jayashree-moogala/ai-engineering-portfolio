# Goal - Build an AI agent that can:
User question
→ decide whether a tool is needed
→ call the right tool
→ use tool result
→ return final answer

Example tools:

calculator
current date/time
text summarizer
simple policy lookup

## Step 1 — Create project structure

From repo root:

cd C:\source\ai-engineering-portfolio

mkdir projects\03-ai-agent-tool-calling
mkdir projects\03-ai-agent-tool-calling\app
mkdir projects\03-ai-agent-tool-calling\app\tools
mkdir projects\03-ai-agent-tool-calling\tests

Create empty package files:

New-Item projects\03-ai-agent-tool-calling\app\__init__.py -ItemType File
New-Item projects\03-ai-agent-tool-calling\app\tools\__init__.py -ItemType File
New-Item projects\03-ai-agent-tool-calling\tests\__init__.py -ItemType File

## Step 1a — Create requirements file

Create:

projects/03-ai-agent-tool-calling/requirements.txt

Add:

fastapi==0.138.1
uvicorn==0.49.0
openai==2.44.0
python-dotenv==1.2.2
pydantic==2.13.4

## Step 1b— Create .env.example

Create:

projects/03-ai-agent-tool-calling/.env.example

Add:

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.4-mini

## Step 1c — Create README placeholder

Create:

projects/03-ai-agent-tool-calling/README.md

Add text


## Step 2 — Create and activate the Project 3 virtual environment

From the Project 3 folder:

cd C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling

Create the virtual environment:

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Verify the active Python:

python -c "import sys; print(sys.executable)"

It should point to:

...\projects\03-ai-agent-tool-calling\.venv\Scripts\python.exe

## Step 3 — Add configuration

Create: app/config.py
Create .env

Verify

Run:

python -c "from app.config import OPENAI_MODEL; print(OPENAI_MODEL)"

Expected output:

gpt-5.4-mini

## Step 4 — Create the calculator tool

Create: app/tools/calculator.py
Create: tests/test_calculator.py
Test/Run: python -m tests.test_calculator

Expected results include:

2 + 3 = 5
10 / 2 = 5.0
5 * 6 = 30
2 ** 3 = 8
(10 + 5) * 2 = 30

## Step 5 — Define the calculator as an OpenAI tool

Create: app/tools/tool_definitions.py

This schema tells the model:

the tool’s name
when it should be used
what argument it accepts
the required JSON structure

The OpenAI Responses API uses function definitions like this to let a model request application-side tool execution. 

Function calling : https://developers.openai.com/api/docs/guides/function-calling

## Step 6 — Create the agent loop

Create: app/agent.py
Create: tests/test_agent.py
Run: python -m tests.test_agent

## Step 7 — Test the agent end to end

Update:  tests/test_agent.py
Run: python -m tests.test_agent

## Step 8 — Add tool-call logging

Update app/agent.py so you can see whether the model used the calculator or answered directly.
Run: python -m tests.test_agent

This makes the agent’s decision process observable without exposing private model reasoning.

Output: 

(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> python -m tests.test_agent

===== AI AGENT TEST =====

Question: What is (125 * 8) + 45?

Agent received: What is (125 * 8) + 45?
Tool selected: calculate
Tool input: (125 * 8) + 45
Tool output: 1045
Answer: 1045
------------------------------------------------------------
Question: What is the current date and time?

Agent received: What is the current date and time?
Tool selected: get_current_datetime
Tool output: 2026-07-14 15:31:40
Answer: Current date and time: 2026-07-14 15:31:40
------------------------------------------------------------
Question: What time is it?

Agent received: What time is it?
Tool selected: get_current_datetime
Tool output: 2026-07-14 15:31:42
Answer: It’s 2026-07-14 15:31:42.
------------------------------------------------------------
Question: What's today's date?

Agent received: What's today's date?
Tool selected: get_current_datetime
Tool output: 2026-07-14 15:31:43
Answer: Today’s date is **2026-07-14**.
------------------------------------------------------------
Question: Current time?

Agent received: Current time?
Tool selected: get_current_datetime
Tool output: 2026-07-14 15:31:44
Answer: Current time: 2026-07-14 15:31:44
------------------------------------------------------------
Question: Explain prompt engineering in one sentence.

Agent received: Explain prompt engineering in one sentence.
No tool selected. Model answered directly.
Answer: Prompt engineering is the practice of designing and refining inputs to an AI model so it produces more accurate, useful, and predictable outputs.
------------------------------------------------------------


## Step 9 — Add a second tool: current date and time

Create: app/tools/date_time.py
Update app/tools/tool_definitions.py to add new tool
update the imports in app/agent.py
   Change both OpenAI calls
   Inside the loop, add code for new tool
Update test_agent
Run python -m tests.test_agent

## Step 10 — Improve tool selection

Update app/agent.py so the model is explicitly instructed to use available tools.
  input .. content ...
Update app/tools/tool_definitions.py to strengthen the date/time tool description 
Run: python -m tests.test_agent


(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> python -m tests.test_agent

===== AI AGENT TEST =====

Question: What is (125 * 8) + 45?

Agent received: What is (125 * 8) + 45?
Tool selected: calculate
Tool input: (125 * 8) + 45
Tool output: 1045
Answer: 1045
------------------------------------------------------------
Question: What is the current date and time?

Agent received: What is the current date and time?
Tool selected: get_current_datetime
Tool output: 2026-07-14 15:30:10
Answer: Current date and time: **2026-07-14 15:30:10**
------------------------------------------------------------
Question: What time is it?

Agent received: What time is it?
Tool selected: get_current_datetime
Tool output: 2026-07-14 15:30:11
Answer: It’s 2026-07-14 15:30:11.
------------------------------------------------------------
Question: What's today's date?

Agent received: What's today's date?
Tool selected: get_current_datetime
Tool output: 2026-07-14 15:30:13
Answer: Today’s date is **2026-07-14**.
------------------------------------------------------------
Question: Current time?,Explain prompt engineering in one sentence.

Agent received: Current time?,Explain prompt engineering in one sentence.
Tool selected: get_current_datetime
Tool output: 2026-07-14 15:30:15
Answer: Current time: 2026-07-14 15:30:15

Prompt engineering is the practice of designing and refining instructions to get more accurate, useful, and consistent outputs from an AI model.


## Step 11 — Refactor tool execution out of agent.py

Create: app/tool_executor.py
update app/agent.py - Replace the tool-specific logic inside the loop - use tool executor instead


## Step 12 — Create a tool registry

Create: app/tool_registry.py

Dcitionary of tools and functions.
TOOL_REGISTRY
       │
       ├───────────────┐
       │               │
"calculate"        "get_current_datetime"
       │               │
       ▼               ▼
 calculate()      get_current_datetime()

 Update: app/tool_executor.py

 Before:

if calculate
elif get_current_datetime
elif future_tool
...

Now:

tool name
→ registry lookup
→ execute function

Adding a new tool only requires registering it in one dictionary.
--


Explain result = tool_function(**arguments)
This is one of the nicest features in Python. It's called argument unpacking.
Python automatically matches the dictionary key (expression) to the function parameter (expression).
Imagine you add 50 tools.
Without unpacking, you'd end up writing multiple if elif statements
With unpacking, every tool can be called the same way, As long as:
    the dictionary keys match the function parameter names, and
    the tool schema matches the function signature.
It lets you add new tools without changing the invocation logic—only the registry and the tool definition need to grow.

Before unpacking:

arguments = {
    "expression": "5 * 6"
}

Using:

calculate(**arguments)

Python internally transforms it into:

calculate(
    expression="5 * 6"
)


---

Then:

tool_function(**arguments)

becomes:

get_current_datetime()

-- 

The complete flow
LLM
 │
 ▼
{
   "expression": "125 * 8 + 45"
}
 │
 ▼
json.loads()
 │
 ▼
arguments
{
   "expression": "125 * 8 + 45"
}
 │
 ▼
tool_function = calculate
 │
 ▼
tool_function(**arguments)
 │
 ▼
calculate(expression="125 * 8 + 45")
 │
 ▼
1045


## Step 13 — Separate Planning from Execution

Right now your agent does everything:

Receive Question
      │
      ▼
Call OpenAI
      │
      ▼
Execute Tool
      │
      ▼
Call OpenAI Again
      │
      ▼
Return Answer

This works, but it violates the Single Responsibility Principle.

Instead, let's split it into components.

                +----------------------+
                |      Agent           |
                +----------------------+
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
+------------------+          +-------------------+
| Planner          |          | Tool Executor     |
|                  |          |                   |
| Calls OpenAI     |          | Runs Python Tools |
| Decides Tool     |          | Returns Results   |
+------------------+          +-------------------+

Architecture is becoming
app/
│
├── agent.py              ← orchestrator
├── planner.py            ← talks to OpenAI
├── tool_executor.py      ← executes tools
├── tool_registry.py      ← registry
│
└── tools/
        calculator.py
        date_time.py

Create app/planner.py - it only plans - no tools, registry or json parsing
update agent.py
Test: python -m tests.test_agent

Before checking in , sanity check :

python -m tests.test_calculator
python -m tests.test_agent


## Step 15 - Add enhancements 

adding:

Logging (structured logging instead of print)
Custom exceptions
Configuration management improvements
Unit tests with pytest
Type hints throughout
Code formatting (black)
Linting (ruff)
GitHub Actions (run tests automatically on every push)

## Step 15a - Add development dependencies

update requirements.txt - 

Added following packages:
pytest>=8.0.0 
pytest-cov>=5.0.0 
httpx>=0.27.0 
black>=24.0.0 
ruff>=0.8.0

| Package        | Purpose                              | Do you need it?     |
| -------------- | ------------------------------------ | ------------------- |
| **pytest**     | Python testing framework             | ✅ Yes               |
| **pytest-cov** | Measures test coverage               | ✅ Yes               |
| **httpx**      | HTTP client used for testing APIs    | ✅ Yes (for FastAPI) |
| **black**      | Automatically formats Python code    | Recommended         |
| **ruff**       | Fast linter and code quality checker | Recommended         |

1. pytest

Purpose: Runs your unit tests.

Instead of writing code and manually checking if it works, you create test files and let pytest verify everything automatically.

Example:

calculator.py
def add(a, b):
    return a + b
test_calculator.py
from calculator import add

def test_add():
    assert add(2, 3) == 5

Run:

pytest

Output:

=================== test session starts ===================

1 passed in 0.02s

For your AI projects, you'll write tests like:

tests/
    test_tools.py
    test_agent.py
    test_api.py
2. pytest-cov

This extends pytest.

It tells you how much of your code is actually tested.

Example:

Suppose your project contains

app/
    agent.py
    tools.py
    api.py

Run

pytest --cov=app

Output

Name          Stmts   Miss Cover
--------------------------------
agent.py         60      2   97%
tools.py         40      0  100%
api.py           30      1   97%

TOTAL                   98%

This means:

98% of your code is tested
only a few lines were never executed

Employers like seeing this.

3. httpx

This is an HTTP client.

Think of it as Python's version of Postman or curl.

Instead of:

Browser
   ↓
FastAPI Server

your test code becomes

Python Test
      ↓
httpx
      ↓
FastAPI Server

Example:

import httpx

response = httpx.get("http://localhost:8000")

print(response.status_code)

Output

200

For FastAPI testing:

from fastapi.testclient import TestClient

client = TestClient(app)

response = client.post(
    "/ask",
    json={"question": "Hello"}
)

assert response.status_code == 200

Internally, FastAPI's testing tools rely on HTTP clients like httpx.

You'll use this extensively in Projects 2 and 3.

4. black

This automatically formats your Python code.

Suppose you write this:

def add(a,b):
 return a+b

Run

black .

It becomes

def add(a, b):
    return a + b

Benefits:

everyone on the team has identical formatting
no arguments over spacing
code looks professional

This is one of the most widely used Python formatters.

5. ruff

Ruff is a linter.

It finds mistakes before your code runs.

Example:

import math

x = 10

print("Hello")

Running:

ruff check .

might report:

Unused import 'math'
Unused variable 'x'

It catches things like:

unused imports
unused variables
missing imports
style violations
possible bugs
complexity issues

It is extremely fast and has become the preferred linter for many modern Python projects.

How they fit into your workflow
Write code
     │
     ▼
black
Formats the code
     │
     ▼
ruff
Checks for mistakes
     │
     ▼
pytest
Runs tests
     │
     ▼
pytest-cov
Measures test coverage
     │
     ▼
GitHub
Commit clean, tested code

These tools are widely recognized and demonstrate good engineering practices - automated testing, coverage reporting, consistent formatting, and linting - for code quality and maintainability.


## 15b. Enviroment 

Update .env and .env.example - control how the agent operates and how much information it logs.

1. AGENT_MAX_ITERATIONS=5

This tells the AI agent:

"You can think and use tools at most 5 times before you must stop."

Why is this needed?

Unlike a simple chatbot, an AI agent may perform several reasoning steps.

For example, suppose the user asks:

"What's the weather in Boston tomorrow and should I carry an umbrella?"

The agent might do this:

Iteration 1
↓
Understand the question

Iteration 2
↓
Call Weather Tool

Iteration 3
↓
Read weather results

Iteration 4
↓
Reason about rain probability

Iteration 5
↓
Generate final answer

Since AGENT_MAX_ITERATIONS=5, the agent stops after the fifth iteration.

Why not allow unlimited iterations?

Imagine a bug like this:

Need weather
↓
Call tool

Need weather
↓
Call tool

Need weather
↓
Call tool

Need weather
↓
Call tool

The agent could get stuck in an infinite loop.

AGENT_MAX_ITERATIONS acts as a safety limit.

Example in code
MAX_ITERATIONS = int(os.getenv("AGENT_MAX_ITERATIONS", 5))

for iteration in range(MAX_ITERATIONS):
    response = think()

    if response.finished:
        break

If .env contains

AGENT_MAX_ITERATIONS=3

the loop runs at most three times.

Typical values
Value	Meaning
1	Simple chatbot
3	Small tool-calling agent
5	Good default
10	Complex multi-step workflows
20+	Advanced autonomous agents

For your portfolio project, 5 is a sensible default.

2. LOG_LEVEL=INFO

This controls how much information the application prints while it runs.

Most Python applications use the built-in logging module:

import logging

Instead of using print(), you write:

logging.info("Loading documents...")
logging.warning("No documents found.")
logging.error("OpenAI API failed.")

The LOG_LEVEL determines which messages are displayed.

Logging levels
DEBUG
INFO
WARNING
ERROR
CRITICAL

From most detailed to least.

DEBUG

Shows everything.

logging.debug("Calling OpenAI")
logging.debug("Tool arguments: ...")
logging.info("Question received")
logging.warning("No documents found")
logging.error("API failed")

Output:

DEBUG Calling OpenAI
DEBUG Tool arguments ...
INFO Question received
WARNING No documents found
ERROR API failed

Useful when you're debugging.

INFO

Shows normal application activity.

logging.info("Loading documents")
logging.info("Creating embeddings")
logging.warning("No PDF files")
logging.error("Connection failed")

Output:

INFO Loading documents
INFO Creating embeddings
WARNING No PDF files
ERROR Connection failed

This is the most common setting for development.

WARNING

Only potential problems and errors.

WARNING No documents found
ERROR API failed
ERROR

Only errors.

ERROR OpenAI request failed
CRITICAL

Only very serious failures.

CRITICAL Database corrupted

Reading the value from .env

Your code might look like:

import os
import logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(level=LOG_LEVEL)

If .env contains

LOG_LEVEL=DEBUG

you'll see much more detailed output.

If it contains

LOG_LEVEL=ERROR

only errors are displayed.

Why use a .env file?

Suppose your code contains:

logging.basicConfig(level="INFO")

Changing the level requires editing the code.

Instead, with:

LOG_LEVEL=DEBUG

you simply change the .env file, restart the application, and the new setting takes effect—no code changes needed.

How these fit into your AI Agent project
User Question
      │
      ▼
Agent starts
      │
      ├── Can reason at most 5 times
      │      (AGENT_MAX_ITERATIONS)
      │
      ├── Logs every important step
      │      (LOG_LEVEL=INFO)
      │
      ▼
Final Answer
For your AI Agent portfolio

A typical .env file might look like this:

OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4.1-mini

AGENT_MAX_ITERATIONS=5
LOG_LEVEL=INFO

As you build more advanced agents, you can make AGENT_MAX_ITERATIONS configurable so different workflows (simple vs. complex) can have different limits without changing the code. This is a common pattern in production AI systems.

## 15c -app/config.py 

Why this is better than separate constants

Instead of:

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

you get:

one structured configuration object
startup validation
default values
correct type conversion
protection against accidental changes
clearer code throughout the project

The overall flow is:

.env
  ↓
load_dotenv()
  ↓
read environment variables
  ↓
validate and convert values
  ↓
Settings object
  ↓
used by Agent, Planner, and logging

Settings object -> Global -. loads and validates the configuration once when the module is imported
Other files can then use and and access values

## 15d - create app/exceptions.py  

Provides meaningful errors instead of generic ValueError exceptions.

## 15e - create app/logging_config.py

This is a logging utility module. Instead of every file configuring logging separately, your application configures it once and then every module can get its own logger.

Overall architecture
.env
│
├── LOG_LEVEL=INFO
│
▼
config.py
│
├── settings.log_level
│
▼
logging_config.py   ← (this file)
│
├── configure_logging()
├── get_logger()
│
▼
Every other Python file
│
├── logger = get_logger(__name__)
├── logger.info(...)
├── logger.error(...)

This is a common pattern in professional Python applications.

Line 1
import logging

This imports Python's built-in logging module.

It provides functions like:

logging.debug()
logging.info()
logging.warning()
logging.error()
logging.critical()

Instead of using:

print("Loading documents...")

you use

logging.info("Loading documents...")

Logging is much more powerful because it can include timestamps, severity levels, module names, and can write to files or monitoring systems.

Logging gives you:

Timestamp: When did it happen?
Severity: INFO, WARNING, ERROR, etc.
Source: Which module produced it?
Configurability: Show or hide messages based on LOG_LEVEL.

How this fits into your AI Agent
Application Starts
        │
        ▼
configure_logging()
        │
        ├── Reads LOG_LEVEL from .env
        ├── Configures logging format
        └── Sets global logging level
        │
        ▼
agent.py
        │
        ├── logger = get_logger(__name__)
        ├── logger.info("Received question")
        ├── logger.info("Selecting tool")
        ├── logger.error("Tool failed")
        │
        ▼
Console Output

2026-07-16 08:42:11 | INFO  | app.agent | Received question
2026-07-16 08:42:12 | INFO  | app.agent | Selecting tool
2026-07-16 08:42:13 | ERROR | app.tools | Calculator failed

This separation—one module to configure logging and every other module simply obtaining a logger—is a standard design used in production Python applications because it keeps logging behavior consistent across the entire codebase.

## 15f - create app/memory.py

memory.py provides the agent with short-term conversation memory. Without it, the agent treats every question as completely new. With it, the agent can remember previous user and assistant messages during the current session.

Where it fits
              User
                │
                ▼
           agent.py
                │
      ┌─────────┴─────────┐
      ▼                   ▼
 Planner             Memory
      │                   │
      ▼                   │
 Select Tool              │
      │                   │
      ▼                   │
 Execute Tool             │
      │                   │
      └─────────┬─────────┘
                ▼
          Final Answer
                │
                ▼
      Save conversation

The agent asks the memory object:

What has the user asked before?
What did I answer?
What conversation history should I send to the LLM?
Typical implementation

The file is likely structured like this:

class ConversationMemory:
    def __init__(self, max_messages=20):
        self.messages = []
        self.max_messages = max_messages

There are two instance variables.

self.messages
self.messages = []

This stores the conversation history.

Initially:

[]

After the first interaction:

[
    {
        "role": "user",
        "content": "What is Python?"
    }
]

After the assistant replies:

[
    {
        "role": "user",
        "content": "What is Python?"
    },
    {
        "role": "assistant",
        "content": "Python is a programming language."
    }
]

The list grows as the conversation continues.

self.max_messages
self.max_messages = 20

This limits how much conversation is retained.

Without a limit:

Day 1
100 messages

Day 2
300 messages

Day 10
3000 messages

Every LLM request would become larger, slower, and more expensive.

Instead, the memory keeps only the most recent messages.

add_user_message()

Example implementation:

def add_user_message(self, content):
    self.messages.append(
        {
            "role": "user",
            "content": content,
        }
    )
    self._trim()

Suppose the user asks:

"What's the weather?"

The list becomes:

[
    {
        "role": "user",
        "content": "What's the weather?"
    }
]

Then _trim() checks whether the list has become too long.

add_assistant_message()
def add_assistant_message(self, content):
    self.messages.append(
        {
            "role": "assistant",
            "content": content,
        }
    )
    self._trim()

After the response:

[
    {
        "role": "user",
        "content": "What's the weather?"
    },
    {
        "role": "assistant",
        "content": "Sunny."
    }
]
get_messages()

Typical implementation:

def get_messages(self):
    return self.messages

This simply returns the current conversation.

The agent can then send it to the LLM:

client.responses.create(
    model=model,
    input=memory.get_messages()
)

Instead of sending only:

User:
What's the weather?

it sends:

User:
Hi

Assistant:
Hello!

User:
What's the weather?

Now the model has context.

clear()
def clear(self):
    self.messages.clear()

Before:

[
    ...
]

After:

[]

This resets the conversation.

_trim()

This is the most interesting method.

A typical version looks like:

def _trim(self):
    if len(self.messages) > self.max_messages:
        self.messages = self.messages[-self.max_messages:]

Suppose:

max_messages = 5

Current memory:

1
2
3
4
5
6
7

After trimming:

3
4
5
6
7

The oldest messages are removed, and only the newest five remain.

How agent.py uses it

The flow typically looks like this:

memory.add_user_message(question)

answer = planner.run(...)

memory.add_assistant_message(answer)

So after several exchanges:

User: Hello
Assistant: Hi!

User: What is Python?
Assistant: Python is a language.

User: Who created it?
Assistant: Guido van Rossum.

The next LLM call receives the conversation history, allowing it to understand that "it" refers to Python.

Why is this useful?

Without memory:

User:
What is Python?

Assistant:
Programming language.

User:
Who created it?

Assistant:
Who are you referring to?

With memory:

User:
What is Python?

Assistant:
Programming language.

User:
Who created it?

Assistant:
Guido van Rossum.

The second answer is possible because the previous conversation is still available.

Current limitations

The version we built uses in-memory storage:

RAM
│
├── Conversation
├── Conversation
└── Conversation

If you stop the program:

Ctrl+C

the memory is lost.

When you restart:

memory.messages == []

This is perfectly fine for a learning project and demonstrates the concept clearly.

How this evolves in production

Production AI systems typically replace the in-memory list with persistent storage:

User
   │
   ▼
Agent
   │
   ▼
Memory Interface
   │
   ├── Redis
   ├── PostgreSQL
   ├── MongoDB
   ├── Vector Database
   └── Conversation Store

The agent code doesn't need to change much—it still calls methods like add_user_message() and get_messages(). Only the underlying implementation changes, which is a good example of separating an interface from its storage mechanism.

## 15g - update app/tools/calculator.py

Explain : dict[type[ast.AST], BinaryOperator | UnaryOperator] 

This is a type hint. It tells you exactly what kind of data a variable contains.

dict[type[ast.AST], BinaryOperator | UnaryOperator]

Let's read it from the inside out.

Step 1: dict

This means the variable is a Python dictionary.

{
    key: value
}
Step 2: type[ast.AST]

This is the type of the keys.

ast.AST is the base class for every AST node.

Examples of AST node classes include:

ast.Add
ast.Sub
ast.Mult
ast.Div
ast.USub
ast.Pow

Notice these are classes, not objects.

For example:

import ast

print(ast.Add)

Output:

<class '_ast.Add'>

So

type[ast.AST]

means

"The key is an AST class."

Examples:

ast.Add
ast.Sub
ast.Mult
Step 3: BinaryOperator | UnaryOperator

This is the type of the values.

The | means or (introduced in Python 3.10).

Equivalent older syntax:

Union[BinaryOperator, UnaryOperator]

So a value can be either

a BinaryOperator
or a UnaryOperator
Putting it together
dict[
    type[ast.AST],
    BinaryOperator | UnaryOperator
]

means

A dictionary whose:

keys are AST node classes
values are BinaryOperator or UnaryOperator objects/functions
A Real Example

Suppose you are building a calculator.

You define:

import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

Python infers this type as something like:

dict[type[ast.AST], Callable]

or, if you've created custom operator types:

dict[type[ast.AST], BinaryOperator]
Why Use AST Classes as Keys?

Imagine the AST for:

5 + 3

looks like:

BinOp
├── Constant(5)
├── Add
└── Constant(3)

The operator node is:

ast.Add

You can use it directly to find the corresponding Python function:

operator_function = OPERATORS[type(node.op)]

If

type(node.op)

returns

ast.Add

then

OPERATORS[ast.Add]

returns

operator.add

Then:

operator.add(5, 3)

returns

8
Visual Example

Suppose your dictionary is:

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.USub: operator.neg,
}

It looks like:

AST Node Class            Python Function
----------------------------------------------
ast.Add      ─────────►   operator.add
ast.Sub      ─────────►   operator.sub
ast.Mult     ─────────►   operator.mul
ast.USub     ─────────►   operator.neg
What Are BinaryOperator and UnaryOperator?

These are custom type aliases or protocols defined elsewhere in the code.

For example:

from typing import Callable

BinaryOperator = Callable[[float, float], float]

UnaryOperator = Callable[[float], float]

Meaning:

A binary operator accepts two arguments:

def add(a, b):
    return a + b

A unary operator accepts one argument:

def negate(a):
    return -a
Example from a Safe Calculator

You might see:

import ast
import operator

BinaryOperator = Callable[[float, float], float]

OPERATORS: dict[type[ast.AST], BinaryOperator] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

Then during evaluation:

op = OPERATORS[type(node.op)]

result = op(left, right)

If the parsed expression is:

5 * 8

then

type(node.op)

is

ast.Mult

which retrieves

operator.mul

and executes

operator.mul(5, 8)

to produce

40
Why This Is Common in AI Agent Projects

This pattern is often used in safe expression evaluators.

Instead of writing a long chain like:

if isinstance(node.op, ast.Add):
    ...

elif isinstance(node.op, ast.Sub):
    ...

elif isinstance(node.op, ast.Mult):
    ...

you use a lookup table:

OPERATORS[type(node.op)](left, right)

This is more concise, easier to extend, and a common Python design pattern.

Summary
dict[type[ast.AST], BinaryOperator | UnaryOperator]

can be read as:

"A dictionary whose keys are AST node classes (such as ast.Add or ast.USub) and whose values are functions or objects that implement either binary operations (like addition and multiplication) or unary operations (like negation)."

This exact pattern is commonly found in safe calculators, expression parsers, interpreters, and AI agent tools that need to map parsed syntax to executable operations.

## 15h - update app/tools/date_time.py

return datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

Using astimezone() includes the local timezone offset.

## 15i - update app/tools/tool_definitions.py

Added :

AVAILABLE_TOOLS = [
    CALCULATOR_TOOL,
    CURRENT_DATETIME_TOOL,
]

## 15j - update app/tool_registry.py

ToolFunction = Callable[..., Any]

This single line is a type alias. It doesn't change how your program runs—it simply makes the code clearer for developers, IDEs, and type checkers.

Whenever you see ToolFunction, think Callable[..., Any].

A function that can accept any number of arguments and return any type.

A callable is anything you can invoke with parentheses (). -> functions

... (ellipsis) means function can take any number of arguments
Any -> can return any return type

## 15k - update app/tool_executor.py

Adding logging and exception handling

## 15l - update app/planner.py

Added: messages dictionary, import settings

How the Planner fits into the AI Agent
                    User
                      │
                      ▼
              Conversation History
                      │
                      ▼
                 Planner.plan()
                      │
      ┌───────────────┴───────────────┐
      ▼                               ▼
Model returns answer           Model requests tool(s)
                                      │
                                      ▼
                             execute_tool()
                                      │
                                      ▼
                          Tool Output (e.g. "100")
                                      │
                                      ▼
             Planner.continue_with_tool_outputs()
                                      │
                                      ▼
                           Model generates
                           final response
                                      │
                                      ▼
                                   User
The two methods have distinct responsibilities
Method	Purpose	Called When
plan()	Starts a new reasoning step by sending the conversation, system prompt, and available tools to the model	When the user submits a new message
continue_with_tool_outputs()	Continues the same reasoning process after your Python code has executed one or more requested tools	After execute_tool() returns tool results

A helpful way to think about it is:

plan() asks the model: "Given this conversation and these tools, what do you want to do?"
continue_with_tool_outputs() tells the model: "You asked me to run these tools. Here are the results. Now finish your answer—or ask for another tool if you still need one."

This two-step interaction is the core pattern behind tool-calling AI agents using the OpenAI Responses API.

## 15m - update  app/agent.py

This is the heart of your AI Agent. It coordinates all the other components:

Memory (conversation history)
Planner (LLM interaction)
Tool Executor (runs Python functions)
Configuration (maximum iterations)
Logging

Added : import settings, custom exceptions, logging helper, conversation memory,supports multiple tool outputs

## 15n - add  app/api.py

How the API works
1. Health Check

Client sends

GET /health

FastAPI executes

health()

Response

{
  "status": "ok"
}

This is commonly used by load balancers, Kubernetes, or monitoring systems to verify that the service is running.

2. Agent Request

Client sends

POST /agent

Request body

{
    "message": "What is 25 * 4?"
}

Flow

Browser
     │
     ▼
FastAPI
     │
     ▼
Agent.run()
     │
     ▼
Planner
     │
     ▼
LLM requests calculator
     │
     ▼
execute_tool()
     │
     ▼
calculate()
     │
     ▼
100
     │
     ▼
Planner
     │
     ▼
Final Answer
     │
     ▼
FastAPI
     │
     ▼
JSON Response

Response

{
    "message": "What is 25 * 4?",
    "answer": "25 × 4 = 100."
}
3. Clear Memory

Client sends

DELETE /memory

Flow

DELETE /memory
        │
        ▼
agent.clear_memory()
        │
        ▼
ConversationMemory.clear()
        │
        ▼
[]

Response

{
    "status": "conversation memory cleared"
}
Overall architecture
                Client
     (Browser / Postman / curl)
                    │
                    ▼
               FastAPI Server
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   GET /health  POST /agent  DELETE /memory
                    │
                    ▼
                 Agent.run()
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
 ConversationMemory       Planner
                                 │
                                 ▼
                           OpenAI API
                                 │
                         Tool Requests?
                                 │
                                 ▼
                         execute_tool()
                                 │
                                 ▼
                           Python Tools

This file is intentionally "thin." It focuses on HTTP concerns—receiving requests, validating input, invoking the agent, and returning HTTP responses. All of the AI logic lives in the Agent class and its collaborators, which keeps the API layer simple and makes the core agent reusable from other entry points, such as a command-line interface or another


Run:

uvicorn app.api:app --reload

Swagger:

http://127.0.0.1:8000/docs

## 15o - update tests/test_calculator.py

use  pytest 

This file contains unit tests for your calculate() function. It verifies that the calculator behaves correctly for both valid inputs and invalid or unsafe inputs.

Below is the same code with detailed inline comments.

# Import the pytest testing framework.
#
# Pytest automatically discovers functions whose names
# begin with "test_" and executes them.
import pytest

# Import the function we want to test.
from app.tools.calculator import calculate


# -------------------------------------------------------------------
# Parameterized Test
# -------------------------------------------------------------------
#
# Instead of writing six separate test functions,
# pytest runs the same test multiple times with
# different input values.
#
@pytest.mark.parametrize(

    # Names of the parameters that will be passed
    # into the test function.
    ("expression", "expected"),

    # Test cases.
    #
    # Each tuple contains:
    #
    # (input_expression, expected_result)
    #
    [
        ("2 + 3", 5),
        ("10 / 2", 5),
        ("5 * 6", 30),
        ("2 ** 3", 8),
        ("(10 + 5) * 2", 30),
        ("-5 + 2", -3),
    ],
)
def test_calculate(
    expression: str,
    expected: float,
) -> None:

    # Execute the calculator and verify that
    # the returned value matches the expected result.
    #
    # If they are different,
    # pytest automatically reports the failure.
    assert calculate(expression) == expected


# -------------------------------------------------------------------
# Security Test
# -------------------------------------------------------------------
#
# Ensure that unsafe Python code is rejected.
#
# The calculator should evaluate arithmetic,
# NOT execute arbitrary Python code.
#
def test_calculate_rejects_unsafe_code() -> None:

    # Verify that calculate() raises a ValueError.
    #
    # If no exception is raised,
    # the test automatically fails.
    with pytest.raises(ValueError):

        # Attempt to execute operating system code.
        #
        # A secure calculator must reject this.
        calculate("__import__('os').system('dir')")


# -------------------------------------------------------------------
# Validation Test
# -------------------------------------------------------------------
#
# Verify that an empty expression is not allowed.
#
def test_calculate_rejects_empty_expression() -> None:

    # Expect a ValueError.
    with pytest.raises(ValueError):

        # Empty input should not be accepted.
        calculate("")
How @pytest.mark.parametrize works

This is one of pytest's most useful features.

Instead of writing:

def test_add():
    assert calculate("2 + 3") == 5

def test_divide():
    assert calculate("10 / 2") == 5

def test_multiply():
    assert calculate("5 * 6") == 30

def test_power():
    assert calculate("2 ** 3") == 8

you write one test:

@pytest.mark.parametrize(...)
def test_calculate(expression, expected):
    ...

Pytest expands it internally into multiple test runs.

Run #1
expression = "2 + 3"
expected = 5

Run #2
expression = "10 / 2"
expected = 5

Run #3
expression = "5 * 6"
expected = 30

...

Run #6
expression = "-5 + 2"
expected = -3

The test function is executed once for every row.

Understanding pytest.raises()

This is another very common pytest feature.

Suppose your code is:

calculate("")

Your calculator should raise

ValueError

Without pytest.raises, the test would stop with an error.

Instead, you tell pytest:

with pytest.raises(ValueError):
    calculate("")

This means:

"I expect this code to raise a ValueError. If it does, the test passes."

Success case
with pytest.raises(ValueError):
    calculate("")

Result:

ValueError raised

✅ Test passes.

Failure case

Suppose your calculator incorrectly returns:

0

instead of raising an exception.

Then:

No exception raised

Pytest reports:

Failed: DID NOT RAISE <class 'ValueError'>

This immediately tells you that your validation logic is broken.

What this test file verifies
                calculate()
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   Arithmetic     Unsafe Code   Empty Input
        │             │             │
        ▼             ▼             ▼
Correct Result   Raise Error   Raise Error
        │             │             │
        └─────────────┼─────────────┘
                      ▼
               Pytest verifies
               expected behavior

These three tests cover three important aspects of the calculator:

Correctness – Does it compute valid arithmetic expressions correctly?
Security – Does it reject attempts to execute arbitrary Python code?
Input validation – Does it reject invalid input, such as an empty expression?

This combination of positive and negative test cases is a good testing practice and demonstrates that you're verifying both expected behavior and error handling.

## 15p - update tests/test_memory.py

What these tests verify
               ConversationMemory
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Store Messages    Clear Memory    Trim History
      │               │               │
      ▼               ▼               ▼
Correct Order    Empty List      Remove Oldest
      │               │               │
      └───────────────┼───────────────┘
                      ▼
                 Pytest verifies
Why these three tests are important
Test 1
test_memory_stores_messages()

Verifies:

User messages are stored.
Assistant messages are stored.
Messages remain in the correct order.
Test 2
test_memory_can_be_cleared()

Verifies:

clear() completely resets the conversation.
No old messages remain.
Test 3
test_memory_trims_old_messages()

Verifies:

max_messages is respected.
The oldest messages are discarded first (FIFO behavior).
The newest conversation is preserved.
Example of the trimming behavior

Suppose:

memory = ConversationMemory(max_messages=2)

Initially:

[]

After:

memory.add_user_message("One")
One

After:

memory.add_assistant_message("Two")
One
Two

After:

memory.add_user_message("Three")

The list briefly becomes:

One
Two
Three

Since only 2 messages are allowed, the oldest message ("One") is removed:

Two
Three

That's exactly what the final assertion checks:

assert memory.get_messages()[0]["content"] == "Two"

This confirms that the trimming logic keeps the most recent messages, which is the desired behavior for a short-term conversation memory.

## 15q - add test_tool_executor.py 

Why SimpleNamespace is used

In production, the OpenAI Responses API returns a tool call object similar to:

tool_call
    │
    ├── name
    ├── arguments
    └── call_id

Instead of constructing the real OpenAI object (which would require an API call), the test creates a simple stand-in:

tool_call = SimpleNamespace(
    name="calculate",
    arguments='{"expression":"5 * 6"}',
    call_id="call-123",
)

This gives you an object with the same attributes:

tool_call.name
tool_call.arguments
tool_call.call_id

making it perfect for unit testing.

What each test verifies
Test 1
test_execute_calculator_tool()

Flow:

Fake Tool Call
      │
      ▼
execute_tool()
      │
      ▼
calculate()
      │
      ▼
30
      │
      ▼
Correct Response Object

Verifies:

Tool lookup works.
JSON arguments are parsed.
The calculator executes correctly.
The returned structure matches the Responses API format.
Test 2
test_execute_datetime_tool()

Flow:

Fake Tool Call
      │
      ▼
execute_tool()
      │
      ▼
get_current_datetime()
      │
      ▼
Current Date/Time

The exact timestamp changes every time the test runs, so instead of checking a fixed value:

assert result["output"] == "2026-07-17 ..."

the test simply verifies that:

assert result["output"]

meaning some non-empty output was produced.

Test 3
test_unknown_tool_raises_error()

Flow:

Tool Name
missing_tool
      │
      ▼
TOOL_REGISTRY
      │
      ▼
Not Found
      │
      ▼
UnknownToolError

This verifies that your application fails safely when the LLM requests a tool that isn't registered.

Overall test coverage

These three tests validate the three most important behaviors of execute_tool():

              execute_tool()
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
Valid Tool     Another Tool   Invalid Tool
     │              │              │
     ▼              ▼              ▼
Runs Tool     Runs Tool     Raises Exception
     │              │              │
     └──────────────┼──────────────┘
                    ▼
             Pytest verifies

Together they ensure that execute_tool() handles successful execution, different tool types, and error conditions, giving you good confidence that this critical bridge between the LLM and your Python functions behaves correctly.

## 15r - add tests/test_agent.py

This is an excellent unit test because it tests the Agent in isolation. Instead of calling the real OpenAI API, it uses a FakePlanner that pretends to be the LLM.

Why use a FakePlanner?

Normally, the Agent talks to OpenAI:

Agent
   │
   ▼
Planner
   │
   ▼
OpenAI API

That means:

Internet required
API key required
Costs money
Slower
Results can vary

For a unit test, you don't want any of those.

Instead, replace the real planner:

Agent
   │
   ▼
FakePlanner
   │
   ▼
Predefined Answer

Now the test is:

Fast
Free
Deterministic
Focused only on the Agent logic
What output=[] means

This line is very important:

output=[]

Remember your Agent.run() method:

tool_calls = [
    item
    for item in response.output
    if item.type == "function_call"
]

Since

response.output == []

the list comprehension produces

tool_calls == []

Therefore the Agent executes this branch:

if not tool_calls:

and immediately returns:

response.output_text

No tools are executed.

Why continue_with_tool_outputs() raises an error

Notice:

def continue_with_tool_outputs(...):

    raise AssertionError(...)

Why intentionally raise an error?

Because this method should never be called.

If your Agent accidentally did this:

Planner.plan()
       │
       ▼
Final Answer
       │
       ▼
continue_with_tool_outputs()

that would be a bug.

The test would immediately fail with

AssertionError:
No tool continuation was expected.

This is a clever way of proving that the Agent followed the correct execution path.

What this test verifies
User Question
       │
       ▼
Agent.run()
       │
       ▼
FakePlanner.plan()
       │
       ▼
Final Answer
       │
       ▼
Store in Memory
       │
       ▼
Return Answer

The test confirms all three behaviors:

✅ The Agent consulted the planner (planner.plan_called).
✅ The Agent returned the planner's answer unchanged.
✅ The Agent stored the assistant's reply in ConversationMemory.

This is a classic example of dependency injection in unit testing: you replace an external dependency (the Planner/OpenAI API) with a simple fake object so you can test the Agent's own behavior independently.


## 15s - add tests/test_api.py

What is TestClient?

Normally your application runs like this:

Browser
     │
HTTP Request
     │
     ▼
FastAPI Server
     │
     ▼
run_agent()

For testing, there is no real server.

Instead:

TestClient
     │
     ▼
FastAPI
     │
     ▼
run_agent()

Everything runs inside Python, making tests very fast.

Why set OPENAI_API_KEY?

This line:

os.environ.setdefault(
    "OPENAI_API_KEY",
    "test-key",
)

often confuses people.

When Python imports:

from app.api import app

it executes:

agent = Agent()

which eventually creates:

OpenAI(api_key=settings.openai_api_key)

If there is no API key, the application may fail during startup.

The tests never call OpenAI, but the object still needs to be created.

So we provide a fake key:

OPENAI_API_KEY=test-key

This is enough for the application to initialize successfully.

What is monkeypatch?

This is one of pytest's most useful features.

Normally:

agent.run(...)

calls:

Planner
     │
     ▼
OpenAI

Instead:

monkeypatch.setattr(
    agent,
    "run",
    lambda message: "Mock agent response",
)

temporarily changes:

agent.run

into:

lambda message:
    "Mock agent response"

Now:

agent.run("Hello")

immediately returns:

Mock agent response

No LLM.

No tools.

No internet.

No API cost.

Why does the third test return 422 instead of 400?

Your request model is:

class AgentRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
    )

FastAPI validates the request before it calls your endpoint.

Flow:

POST /agent
      │
      ▼
Pydantic Validation
      │
      ├── Valid
      │      ▼
      │  run_agent()
      │
      └── Invalid
             ▼
       Return 422

Since:

{
    "message": ""
}

violates:

min_length=1

FastAPI rejects the request immediately.

Your code inside:

run_agent()

is never executed.

Overall test coverage
                 FastAPI API
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 GET /health    POST /agent     Validation
      │               │               │
      ▼               ▼               ▼
Status OK     Mock Agent      Empty Request
      │               │               │
      ▼               ▼               ▼
 200 Response   200 Response    422 Response

These tests verify three different aspects of your API:

Health endpoint – confirms the service is running.
Agent endpoint – confirms the API correctly delegates to the agent and formats the response.
Request validation – confirms invalid input is rejected automatically by FastAPI/Pydantic before your application logic runs.

## 15t - add pyproject.toml

Centralizes the configuration for your development tools, so you don't need separate configuration files like pytest.ini, .flake8, or black.toml.

What each tool does

Your development workflow looks like this:

           Write Code
                │
                ▼
           black .
                │
      Formats your code
                │
                ▼
       ruff check .
                │
 Finds mistakes & style issues
                │
                ▼
            pytest
                │
     Runs all your tests
                │
                ▼
        Coverage Report
                │
                ▼
          Commit to Git
Understanding pytest options

Suppose you run:

pytest

Because of:

addopts = "-v --cov=app --cov-report=term-missing"

pytest actually runs as if you typed:

pytest -v --cov=app --cov-report=term-missing

Example output:

=================== test session starts ===================

tests/test_agent.py ........
tests/test_memory.py .......
tests/test_tools.py ........

---------- coverage ----------
Name                 Stmts   Miss  Cover
-----------------------------------------
agent.py               70      2    97%
memory.py              25      0   100%
planner.py             30      1    97%
tool_executor.py       40      0   100%

TOTAL                         98%

If you use --cov-report=term-missing, pytest will even tell you which line numbers weren't executed.

Why both Black and Ruff use 88 characters

You'll notice both contain:

line-length = 88

This is intentional.

If Black wrapped at 88 characters but Ruff enforced 79, you'd constantly get lint errors after formatting.

Using the same value keeps the tools in agreement.

Why known-first-party = ["app"] matters

Without it, Ruff might treat:

from app.agent import Agent

as a third-party import and mix it with packages like pytest or fastapi.

With:

known-first-party = ["app"]

Ruff knows that app belongs to your project.

So imports are grouped neatly:

# Standard library
import json

# Third-party packages
import pytest
from fastapi import FastAPI

# Your application
from app.agent import Agent
from app.memory import ConversationMemory

This is the style you'll see in most professional Python projects.

## 15 u - Test
pytest
black app tests
ruff check app tests
ruff check app tests --fix   -> did not run this

Explain 
ruff check app tests

The command

ruff check app tests

runs the Ruff linter on the app and tests directories.

Think of it as a spell checker and code reviewer for your Python code. It doesn't run your program—it analyzes your source code and points out potential mistakes, style issues, and code quality problems.

Breaking down the command
ruff check app tests

It consists of three parts:

ruff
   │
   ▼
Run the Ruff program

check
   │
   ▼
Analyze the code for problems

app tests
   │
   ▼
Directories to scan

So Ruff will examine:

project/
│
├── app/
│      agent.py
│      planner.py
│      memory.py
│      ...
│
└── tests/
       test_agent.py
       test_memory.py
       ...
What Ruff checks

Based on your pyproject.toml, Ruff is checking these rule categories:

select = [
    "E",
    "F",
    "I",
    "B",
    "UP",
]

These correspond to:

Rule	Checks
E	Style and formatting errors (pycodestyle)
F	Programming mistakes (Pyflakes)
I	Import ordering (isort)
B	Common bugs (Bugbear)
UP	Modern Python syntax (Pyupgrade)
Example 1: Unused import

Suppose you have:

import json
import math

print("Hello")

Run:

ruff check app

Output:

app/example.py:2:8: F401 `math` imported but unused

Why?

Because:

import math

is never used.

You should either:

import json

print("Hello")

or actually use math.

Example 2: Undefined variable
def add():
    return x + 5

Output:

F821 Undefined name 'x'

Ruff found a real programming bug.

Example 3: Import order

Suppose you write:

from app.agent import Agent
import json
import pytest

Ruff says:

I001 Import block is un-sorted

The preferred order is:

import json

import pytest

from app.agent import Agent

Standard library → Third-party → First-party.

Example 4: Better Python syntax

Suppose you write:

x = list()

Ruff may suggest:

x = []

This comes from the UP (Pyupgrade) rules.

Example 5: Bug detection

Suppose you accidentally write:

if x == True:
    ...

Ruff may suggest a simpler version:

if x:
    ...

This improves readability.

What if there are no issues?

You might see:

All checks passed!

That means Ruff didn't find any problems based on your configured rules.

Does Ruff modify files?

No.

This command:

ruff check app tests

only reports problems.

It does not change your code.

How to automatically fix issues

Many issues can be fixed automatically with:

ruff check app tests --fix

For example:

Before:

import math
import json

print("Hello")

After:

import json

print("Hello")

Unused imports are removed automatically.

Difference between Ruff and Black

People often confuse these.

Black
black app tests

Purpose:

Format my code.

Example:

Before:

def add(a,b):
 return a+b

After:

def add(a, b):
    return a + b

Black changes spacing, indentation, and line wrapping.

Ruff
ruff check app tests

Purpose:

Find mistakes and code quality issues.

Example:

import math

print("Hello")

Ruff says:

Unused import 'math'

It doesn't reformat the code; it tells you about the issue.

Typical development workflow

For your AI Engineering Portfolio projects, a common sequence is:

# 1. Format the code
black app tests

# 2. Check for mistakes
ruff check app tests

# 3. Run unit tests
pytest

# 4. Commit if everything passes
git add .
git commit -m "Add new feature"

Or, if you want Ruff to automatically fix what it can:

black app tests
ruff check app tests --fix
pytest
Where Ruff fits in your project
         Write Code
              │
              ▼
     black app tests
              │
      Formats the code
              │
              ▼
  ruff check app tests
              │
 Finds mistakes & suggestions
              │
              ▼
         pytest
              │
Verifies the code works correctly
              │
              ▼
         Git Commit

A simple way to remember the difference:

Black answers: "Does the code look consistent?"
Ruff answers: "Does the code contain mistakes or quality issues?"
Pytest answers: "Does the code actually work as expected?"

## 15u - Test Output

(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> pytest
==================================================================== test session starts =====================================================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.14.1, cov-7.1.0
collected 18 items                                                                                                                                            

tests/test_agent.py::test_agent_returns_direct_answer PASSED                                                                                            [  5%]
tests/test_api.py::test_health_endpoint PASSED                                                                                                          [ 11%]
tests/test_api.py::test_agent_endpoint PASSED                                                                                                           [ 16%]
tests/test_api.py::test_empty_message_is_rejected PASSED                                                                                                [ 22%]
tests/test_calculator.py::test_calculate[2 + 3-5] PASSED                                                                                                [ 27%]
tests/test_calculator.py::test_calculate[10 / 2-5] PASSED                                                                                               [ 33%]
tests/test_calculator.py::test_calculate[5 * 6-30] PASSED                                                                                               [ 38%]
tests/test_calculator.py::test_calculate[2 ** 3-8] PASSED                                                                                               [ 44%]
tests/test_calculator.py::test_calculate[(10 + 5) * 2-30] PASSED                                                                                        [ 50%]
tests/test_calculator.py::test_calculate[-5 + 2--3] PASSED                                                                                              [ 55%]
tests/test_calculator.py::test_calculate_rejects_unsafe_code PASSED                                                                                     [ 61%]
tests/test_calculator.py::test_calculate_rejects_empty_expression PASSED                                                                                [ 66%]
tests/test_memory.py::test_memory_stores_messages PASSED                                                                                                [ 72%]
tests/test_memory.py::test_memory_can_be_cleared PASSED                                                                                                 [ 77%]
tests/test_memory.py::test_memory_trims_old_messages PASSED                                                                                             [ 83%]
tests/test_tool_executor.py::test_execute_calculator_tool PASSED                                                                                        [ 88%]
tests/test_tool_executor.py::test_execute_datetime_tool PASSED                                                                                          [ 94%]
tests/test_tool_executor.py::test_unknown_tool_raises_error PASSED                                                                                      [100%]

====================================================================== warnings summary ======================================================================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================================================= tests coverage =======================================================================
______________________________________________________ coverage: platform win32, python 3.14.6-final-0 _______________________________________________________

Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app\__init__.py                     0      0   100%
app\agent.py                       35      9    74%   77, 147-179, 189-191
app\api.py                         31      8    74%   165-187, 204-207
app\config.py                      19      4    79%   30, 40-41, 46
app\exceptions.py                   5      0   100%
app\logging_config.py               6      0   100%
app\memory.py                      18      0   100%
app\planner.py                     14      2    86%   87, 137
app\tool_executor.py               20      3    85%   82-92
app\tool_registry.py                6      0   100%
app\tools\__init__.py               0      0   100%
app\tools\calculator.py            25      2    92%   51, 62
app\tools\date_time.py              3      0   100%
app\tools\tool_definitions.py       3      0   100%
-------------------------------------------------------------
TOTAL                             185     28    85%
=============================================================== 18 passed, 1 warning in 1.56s ================================================================
(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> black app tests
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\tool_executor.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\tools\date_time.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\planner.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\tool_registry.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\api.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\memory.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\logging_config.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\tools\tool_definitions.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\agent.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\exceptions.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\tools\calculator.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\tests\test_tool_definition.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\tests\test_agent.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\app\config.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\tests\test_calculator.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\tests\test_api.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\tests\test_memory.py
reformatted C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\tests\test_tool_executor.py

All done! ✨ 🍰 ✨
18 files reformatted, 3 files left unchanged.
(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> ruff check app tests
E501 Line too long (91 > 88)
  --> app\logging_config.py:17:89
   |
15 |             logging.INFO,  # default value
16 |         ),
17 |         # Format for log message - Current date and time, log level, logger's name, message
   |                                                                                         ^^^
18 |         format=("%(asctime)s | %(levelname)s | " "%(name)s | %(message)s"),
19 |     )
   |

E501 Line too long (89 > 88)
 --> app\tool_executor.py:1:89
  |
1 | import json  # Used to convert the tool arguments (JSON string) into a Python dictionary.
  |                                                                                         ^
2 | from typing import Any  # 'Any' means this parameter can be of any type.
  |

UP035 [*] Import from `collections.abc` instead: `Callable`
 --> app\tools\calculator.py:3:1
  |
1 | import ast
2 | import operator
3 | from typing import Callable
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^
4 |
5 | BinaryOperator = Callable[[float, float], float]
  |
help: Import from `collections.abc`

E501 Line too long (89 > 88)
  --> app\tools\tool_definitions.py:35:89
   |
33 |     "type": "function",
34 |     "name": "get_current_datetime",
35 |     "description": (  # tool prompting - provide explicit desc so the agent uses the tool
   |                                                                                         ^
36 |         "Use this tool whenever the user asks for the "
37 |         "current date, current time, today's date, "
   |

Found 4 errors.
[*] 1 fixable with the `--fix` option.



## 15v  - GitHub Actions

At repository root , create .github/workflows/project-03-tests.yml

This file is a GitHub Actions workflow. It tells GitHub:

"Whenever code is pushed (or a pull request is created), automatically build and test Project 03."

What happens when you push code?

Imagine you run:

git push origin main

GitHub automatically starts this workflow.

The execution looks like this:

Git Push
    │
    ▼
GitHub detects change
    │
    ▼
Create Ubuntu Virtual Machine
    │
    ▼
Checkout Repository
    │
    ▼
Install Python 3.12
    │
    ▼
Install Dependencies
    │
    ▼
Run Ruff
    │
    ▼
Run Black --check
    │
    ▼
Run Pytest
    │
    ▼
Pass ✓ or Fail ✗
What happens if Ruff finds a problem?

Suppose you accidentally commit:

import math

print("Hello")

GitHub reaches:

run: ruff check app tests

Output:

F401 'math' imported but unused

The workflow stops immediately.

Run Ruff
     │
     ▼
Failure
     │
     ▼
Workflow Failed ❌

Your pull request will show a failed check.

What happens if Black formatting is wrong?

Suppose you commit:

def add(a,b):
 return a+b

GitHub runs:

black --check app tests

Output:

would reformat app/example.py

Again:

Workflow Failed ❌
What happens if a unit test fails?

Suppose one test fails:

assert calculate("2+2") == 5

Pytest reports:

FAILED tests/test_calculator.py

Workflow:

Run Tests
     │
     ▼
1 Failed
     │
     ▼
Workflow Failed ❌
Why set working-directory?

Without:

defaults:
  run:
    working-directory: projects/03-ai-agent-tool-calling

every command would need:

run: |
  cd projects/03-ai-agent-tool-calling
  pytest

By setting the default once, all subsequent run commands execute from the project directory, keeping the workflow cleaner.

Overall workflow
               Git Push
                   │
                   ▼
         GitHub Actions Trigger
                   │
                   ▼
        Ubuntu Virtual Machine
                   │
                   ▼
        Checkout Repository
                   │
                   ▼
         Install Python 3.12
                   │
                   ▼
       Install Dependencies
                   │
                   ▼
            Ruff Check
                   │
                   ▼
         Black Formatting Check
                   │
                   ▼
             Pytest
                   │
          ┌────────┴────────┐
          ▼                 ▼
     All Pass ✓        Any Failure ✗
          │                 │
          ▼                 ▼
  Green Checkmark     Red X in GitHub

This kind of workflow is a fundamental part of Continuous Integration (CI). Every push or pull request is automatically validated, helping ensure that code quality, formatting, and tests remain consistent without requiring developers to remember to run those checks manually.

Why not run locally ? 

You should run these checks locally too.

GitHub Actions is not a replacement for local testing. It is a second, independent safety check.

Locally, you get fast feedback before committing:

ruff check app tests
black --check app tests
pytest

That helps you catch problems immediately.

GitHub Actions runs the same checks after you push, in a clean Ubuntu environment. That matters because your local Windows machine may differ from GitHub in Python version, installed packages, environment variables, file paths, or operating-system behavior.

A good workflow is:

Write code
   ↓
Run Ruff, Black, and pytest locally
   ↓
Fix issues
   ↓
Commit and push
   ↓
GitHub Actions runs everything again
   ↓
Repository gets a green check

The local checks answer:

Does it work on my machine?

GitHub Actions answers:

Does it also work from a clean, repeatable environment?

For your project, run this from the Project 03 folder before each commit:

ruff check app tests
black --check app tests
pytest

You can also run formatting automatically before the checks:

black app tests
ruff check app tests --fix
pytest

Then GitHub Actions provides the final verification after the push.

## 15w - Test everything

cd C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

black app tests
ruff check app tests --fix
pytest


Output
------

(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> black app tests
All done! ✨ 🍰 ✨
21 files left unchanged.
(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> ruff check app tests --fix
E501 Line too long (91 > 88)
  --> app\logging_config.py:17:89
   |
15 |             logging.INFO,  # default value
16 |         ),
17 |         # Format for log message - Current date and time, log level, logger's name, message
   |                                                                                         ^^^
18 |         format=("%(asctime)s | %(levelname)s | " "%(name)s | %(message)s"),
19 |     )
   |

E501 Line too long (89 > 88)
 --> app\tool_executor.py:1:89
  |
1 | import json  # Used to convert the tool arguments (JSON string) into a Python dictionary.
  |                                                                                         ^
2 | from typing import Any  # 'Any' means this parameter can be of any type.
  |

E501 Line too long (89 > 88)
  --> app\tools\tool_definitions.py:35:89
   |
33 |     "type": "function",
34 |     "name": "get_current_datetime",
35 |     "description": (  # tool prompting - provide explicit desc so the agent uses the tool
   |                                                                                         ^
36 |         "Use this tool whenever the user asks for the "
37 |         "current date, current time, today's date, "
   |

Found 4 errors (1 fixed, 3 remaining).
(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> pytest
=========================================================== test session starts ============================================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.14.1, cov-7.1.0
collected 18 items                                                                                                                          

tests/test_agent.py::test_agent_returns_direct_answer PASSED                                                                          [  5%]
tests/test_api.py::test_health_endpoint PASSED                                                                                        [ 11%]
tests/test_api.py::test_agent_endpoint PASSED                                                                                         [ 16%]
tests/test_api.py::test_empty_message_is_rejected PASSED                                                                              [ 22%]
tests/test_calculator.py::test_calculate[2 + 3-5] PASSED                                                                              [ 27%]
tests/test_calculator.py::test_calculate[10 / 2-5] PASSED                                                                             [ 33%]
tests/test_calculator.py::test_calculate[5 * 6-30] PASSED                                                                             [ 38%]
tests/test_calculator.py::test_calculate[2 ** 3-8] PASSED                                                                             [ 44%]
tests/test_calculator.py::test_calculate[(10 + 5) * 2-30] PASSED                                                                      [ 50%]
tests/test_calculator.py::test_calculate[-5 + 2--3] PASSED                                                                            [ 55%]
tests/test_calculator.py::test_calculate_rejects_unsafe_code PASSED                                                                   [ 61%]
tests/test_calculator.py::test_calculate_rejects_empty_expression PASSED                                                              [ 66%]
tests/test_memory.py::test_memory_stores_messages PASSED                                                                              [ 72%]
tests/test_memory.py::test_memory_can_be_cleared PASSED                                                                               [ 77%]
tests/test_memory.py::test_memory_trims_old_messages PASSED                                                                           [ 83%]
tests/test_tool_executor.py::test_execute_calculator_tool PASSED                                                                      [ 88%]
tests/test_tool_executor.py::test_execute_datetime_tool PASSED                                                                        [ 94%]
tests/test_tool_executor.py::test_unknown_tool_raises_error PASSED                                                                    [100%]

============================================================= warnings summary =============================================================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================== tests coverage ==============================================================
_____________________________________________ coverage: platform win32, python 3.14.6-final-0 ______________________________________________

Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app\__init__.py                     0      0   100%
app\agent.py                       35      9    74%   76, 134-162, 171-173
app\api.py                         31      8    74%   162-182, 199-202
app\config.py                      19      4    79%   34, 43-44, 47
app\exceptions.py                   5      0   100%
app\logging_config.py               6      0   100%
app\memory.py                      18      0   100%
app\planner.py                     14      2    86%   84, 130
app\tool_executor.py               20      3    85%   79-89
app\tool_registry.py                6      0   100%
app\tools\__init__.py               0      0   100%
app\tools\calculator.py            25      2    92%   47, 58
app\tools\date_time.py              3      0   100%
app\tools\tool_definitions.py       3      0   100%
-------------------------------------------------------------
TOTAL                             185     28    85%
====================================================== 18 passed, 1 warning in 2.28s =======================================================
(.venv) PS C:\source\ai-engineering-portfolio\projects\03-ai-agent-tool-calling> 

uvicorn app.api:app --reload
http://127.0.0.1:8000/docs

Try:

{
  "message": "What is (125 * 8) + 45?"
}

Output:
------


Code	Details
200	
Response body
Download
{
  "message": "What is (125 * 8) + 45?",
  "answer": "1045"
}


And:

{
  "message": "What is the current date and time?"


Output
------

	
Response body
Download
{
  "message": "What is the current date and time?",
  "answer": "The current date and time is **2026-07-20 13:42:37 -04:00**."
}