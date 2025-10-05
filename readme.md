# Terminal Simulator

A Python-based terminal simulator with a built-in text editor, created for an advanced programming class project.

## Features

- **User Authentication**: Three user roles with different privilege levels (root, support, guest)
- **Basic Shell Commands**: `pwd`, `ls`, `cd`, `mkdir`, `touch`, `rm`, `logout`, `exit`
- **Built-in Text Editor**: Nano-style text editor with read/write modes
- **Permission System**: Command restrictions based on user privileges

## User Credentials

| Username | Password | Privileges |
|----------|----------|------------|
| root | root | Full access (read, write, rm, touch) |
| support | support | Limited access (read, write) |
| guest | guest | Read-only access |

## Requirements

- Python 3.x
- `curses` library (included in standard Python installation on Unix/Linux/macOS)

## Usage

```bash
python main.py
```

Log in with one of the user credentials above and use standard Unix-like commands to navigate the filesystem.

### Text Editor Controls

- **Arrow keys**: Navigate
- **Ctrl+O**: Save file
- **Ctrl+X**: Exit editor
- **Backspace**: Delete character (write mode only)

## Note

If you encounter display issues, increase your terminal window size.

---

*written with AI.*