import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel, QFrame
from PyQt5.QtCore import Qt
import subprocess


def auto_commit_and_push():
    try:
        # Stage all changes. Adjust the path if needed.
        subprocess.run(["git", "add", "."], check=True)
        # Commit with a message containing the launch date/time
        commit_message = "TODO task updated on " + subprocess.check_output(["date"]).decode().strip()
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        # Push changes to the remote repository
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError as e:
        # Optionally, print the error or handle it as needed.
        print("Auto commit failed:", e)


class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Enforce single selection to avoid selecting extra items.
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(QListWidget.DragDrop)
        self.dragged_item = None  # To store the item being dragged

    def keyPressEvent(self, event):
        # Remove the selected item if the "Del" key is pressed.
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                row = self.row(item)
                self.takeItem(row)
            event.accept()
        else:
            super().keyPressEvent(event)

    def dropEvent(self, event):
        source = event.source()
        if source and source != self:
            # Use the explicitly stored dragged item instead of selectedItems/currentItem.
            if source.dragged_item is not None:
                item = source.dragged_item
                # Check that the item is still in the source list.
                row = source.row(item)
                if row != -1:
                    source.takeItem(row)
                    self.addItem(item)
                # Clear the stored item after handling drop.
                source.dragged_item = None
                event.accept()
            else:
                super().dropEvent(event)
        else:
            super().dropEvent(event)


class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Task Management Program")
        self.setupUI()
        self.load_tasks()  # Load saved tasks on startup

    def setupUI(self):
        # Main layout (vertical)
        main_layout = QVBoxLayout(self)

        # ----- Input Section -----
        input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter a new task")
        # Connect both the "Enter" key and button click.
        self.input_line.returnPressed.connect(self.add_task)
        self.add_button = QPushButton("ADD")
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)

        # ----- Task Sections Layout (horizontal) -----
        sections_layout = QHBoxLayout()

        # Section 1: TODO – Added
        self.todo_added = self.create_task_section("TODO – Added")
        sections_layout.addWidget(self.todo_added)

        # Section 2: TODO – Do Now
        self.todo_do_now = self.create_task_section("TODO – Do Now")
        sections_layout.addWidget(self.todo_do_now)

        # Section 3: TODO – Sometime
        self.todo_sometime = self.create_task_section("TODO – Sometime")
        sections_layout.addWidget(self.todo_sometime)

        # Section 4: DONE
        self.done = self.create_task_section("DONE")
        sections_layout.addWidget(self.done)

        main_layout.addLayout(sections_layout)

        self.setLayout(main_layout)

    def create_task_section(self, title):
        # Create a frame to group a label and our custom draggable list widget vertically.
        frame = QFrame()
        layout = QVBoxLayout(frame)
        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)

        list_widget = DraggableListWidget()
        layout.addWidget(label)
        layout.addWidget(list_widget)
        frame.list_widget = list_widget  # Store a reference for later use.
        return frame

    def add_task(self):
        task_text = self.input_line.text().strip()
        if task_text:
            # Create a new list item and add it to the "TODO – Added" section.
            item = QListWidgetItem(task_text)
            self.todo_added.list_widget.addItem(item)
            self.input_line.clear()

    def load_tasks(self):
        """Load tasks from a JSON file and populate the lists."""
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r") as f:
                    tasks = json.load(f)
                # Map section titles to our list widgets.
                sections = {
                    "TODO – Added": self.todo_added.list_widget,
                    "TODO – Do Now": self.todo_do_now.list_widget,
                    "TODO – Sometime": self.todo_sometime.list_widget,
                    "DONE": self.done.list_widget,
                }
                for section, list_widget in sections.items():
                    for task in tasks.get(section, []):
                        list_widget.addItem(QListWidgetItem(task))
            except Exception as e:
                print("Error loading tasks:", e)

    def save_tasks(self):
        """Save tasks from all sections into a JSON file."""
        tasks = {}
        # Create the mapping for the sections.
        sections = {
            "TODO – Added": self.todo_added.list_widget,
            "TODO – Do Now": self.todo_do_now.list_widget,
            "TODO – Sometime": self.todo_sometime.list_widget,
            "DONE": self.done.list_widget,
        }
        for section, list_widget in sections.items():
            tasks[section] = []
            for index in range(list_widget.count()):
                item = list_widget.item(index)
                tasks[section].append(item.text())
        try:
            with open("tasks.json", "w") as f:
                json.dump(tasks, f)
        except Exception as e:
            print("Error saving tasks:", e)

    def closeEvent(self, event):
        self.save_tasks()  # Save tasks when closing the program.
        event.accept()


if __name__ == "__main__":
    # Optionally, run the auto commit before launching the app.
    auto_commit_and_push()

    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
