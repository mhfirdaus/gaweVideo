"""Pre-built markdown templates for the Streamlit web UI."""

from __future__ import annotations

from typing import Final

TEMPLATES: Final[list[dict[str, str]]] = [
    {
        "name": "Python Tutorial",
        "description": "Basic Python syntax, variables, loops, and functions.",
        "icon": "🐍",
        "content": """# Python Tutorial

## Introduction
Python is a beginner-friendly language used for automation, web apps, and data science.

## Variables
```python
name = "gaweVideo"
version = 1.0
print(name, version)
```

## Loops
- for loop
- while loop
- break and continue

```python
for i in range(3):
    print("Iteration", i)
```

## Functions
```python
def greet(user: str) -> str:
    return f"Hello, {user}!"
```
""",
    },
    {
        "name": "JavaScript Basics",
        "description": "Core JavaScript syntax, arrays, and DOM interaction.",
        "icon": "🟨",
        "content": """# JavaScript Basics

## Introduction
JavaScript powers interactivity in modern web applications.

## Variables and Types
```javascript
const title = "JavaScript Basics";
let count = 5;
console.log(title, count);
```

## Arrays
```javascript
const topics = ["variables", "functions", "DOM"];
topics.forEach((topic) => console.log(topic));
```

## DOM Example
```javascript
document.querySelector("#app").textContent = "Hello from JS!";
```
""",
    },
    {
        "name": "Web Development Guide",
        "description": "Roadmap for HTML, CSS, JavaScript, and deployment.",
        "icon": "🌐",
        "content": """# Web Development Guide

## Frontend Fundamentals
- HTML structure
- CSS styling
- JavaScript behavior

## Backend Basics
- API routing
- database integration
- authentication

## Deployment Checklist
1. Optimize assets
2. Set environment variables
3. Deploy to production platform

```bash
npm run build
npm run deploy
```
""",
    },
    {
        "name": "Data Science Introduction",
        "description": "Quick intro to analysis workflow with pandas and plotting.",
        "icon": "📊",
        "content": """# Data Science Introduction

## Typical Workflow
1. Data collection
2. Data cleaning
3. Analysis and visualization
4. Reporting insights

## Pandas Example
```python
import pandas as pd

df = pd.read_csv("sales.csv")
summary = df.groupby("region")["amount"].sum()
print(summary)
```

## Visualization
```python
import matplotlib.pyplot as plt

summary.plot(kind="bar", title="Sales by Region")
plt.show()
```
""",
    },
]
