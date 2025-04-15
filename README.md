# Simple Task Management Program

This is a lightweight task management application built with PyQt. The application lets you add tasks, drag and drop them between four sections, and delete them via the Delete key. All tasks are saved in a JSON file (`tasks.json`) so that your tasks persist between sessions.

## Features

- **Four Task Sections:**  
  - **TODO – Added:** New tasks appear here.
  - **TODO – Do Now:** Tasks that need immediate attention.
  - **TODO – Sometime:** Tasks planned for later.
  - **DONE:** Completed tasks.

- **Task Addition:**  
  - Add tasks by typing into an input field and clicking the **ADD** button or pressing **Enter**.

- **Drag-and-Drop:**  
  - Easily move tasks between sections by dragging them from one list to another.

- **Keyboard Deletion:**  
  - Remove a selected task by pressing the **Del** key.

- **Persistent Storage:**  
  - Tasks are automatically saved to a JSON file (`tasks.json`) and reloaded when the application starts.

## Installation

### Prerequisites

- Python 3
- PyQt5

### Installing PyQt5 on Ubuntu

Run the following commands to update your package list and install PyQt5:

```bash
sudo apt update
sudo apt install python3-pyqt5


## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/simple-task-manager.git
   cd simple-task-manager
   ```

2. **Run the Application:**

   ```bash
   python3 task_manager.py
   ```

3. **Using the Application:**
   - **Adding Tasks:** Type a task into the input field at the top and press **Enter** or click the **ADD** button. New tasks appear in the **TODO – Added** section.
   - **Moving Tasks:** Drag tasks between sections to organize them.
   - **Deleting Tasks:** Select a task and press the **Del** key to remove it.
   - **Persistence:** Your tasks are automatically saved when the program is closed and reloaded on startup.

## Customization & Styling

- **Interface Styling:**  
  The section headings are displayed in bold with distinct colors to enhance readability.
  
- **Window Size:**  
  The application starts with a window size of 1920×1080. You can adjust this value in the source code if needed.

## Contributing

Contributions are welcome! Feel free to fork the repository, create new features or improvements, and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for using the Simple Task Management Program. If you have any questions, suggestions, or issues, please open an issue in the repository.
```
```
