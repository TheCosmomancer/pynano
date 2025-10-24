# Terminal Simulator

A Python-based terminal simulator with a built-in text editor, created for an advanced programming class project.

## Versions

### V1: Multi-User Shell System
Full terminal simulator with user authentication and permission-based commands.

### V2: Enhanced Text Editor
Streamlined version focusing on advanced text editing features with multi-file support.

## V1 Features

- **User Authentication**: Three user roles with different privilege levels (root, support, guest)
- **Basic Shell Commands**: `pwd`, `ls`, `cd`, `mkdir`, `touch`, `rm`, `logout`, `exit`
- **Built-in Text Editor**: Nano-style text editor with read/write modes
- **Permission System**: Command restrictions based on user privileges

### User Credentials

| Username | Password | Privileges |
|----------|----------|------------|
| root | root | Full access (read, write, rm, touch) |
| support | support | Limited access (read, write) |
| guest | guest | Read-only access |

### Usage

```bash
python V1/main.py
```

Log in with one of the user credentials above and use standard Unix-like commands to navigate the filesystem.

## V2 Features

- **Multi-File Editing**: Navigate between multiple files in a directory
- **Undo/Redo**: Full undo/redo support with Ctrl+U and Ctrl+R
- **Clipboard System**: Copy/paste with highlighting (Ctrl+H to highlight, Ctrl+B for clipboard)
- **File Picker**: Quick file switching interface
- **No Authentication**: Direct access to editing functionality

### Usage

```bash
python V2/main.py <filepath_or_directory>
```

Provide a file path or directory as an argument. If a directory is given, all files within can be accessed through the file picker.

## Text Editor Controls

### V1 Controls
- **Arrow keys**: Navigate
- **Ctrl+O**: Save file
- **Ctrl+X**: Exit editor
- **Backspace**: Delete character (write mode only)

### V2 Controls
- **Arrow keys**: Navigate
- **Ctrl+O**: Save file
- **Ctrl+X**: Exit editor/application
- **Ctrl+H**: Toggle highlight mode for copying
- **Ctrl+B**: Open clipboard to paste
- **Ctrl+U**: Undo
- **Ctrl+R**: Redo
- **Backspace**: Delete character

## Requirements

- Python 3.x
- `curses` library (included in standard Python installation on Unix/Linux/macOS)

## Note

If you encounter display issues, increase your terminal window size.

---

*readme written with AI.*
