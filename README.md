# Todo List

A desktop todo app for Windows, built with Python and CustomTkinter.

## Features

- Add todos with an optional description (Enter key works too)
- Priority (High, Medium, Low) and category (programming language) per todo
- Separate tabs for active and completed todos
- Filter by category
- Statistics: how many todos are completed
- Edit and delete todos
- Automatic saving to `%LOCALAPPDATA%\ToDo\todos.json`

## Installation

**As a program:** Download `TodoListe.exe` from Release and run it.
Windows may show a Warning 

**From source:**

```
pip install customtkinter
python gui.py
```

## Note

The app uses Windows-specific features (save location and window icon), so it only runs on Windows.
