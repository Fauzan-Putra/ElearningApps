# Aksanta - E-Learning Platform

## Overview
Aksanta is an e-learning platform designed to facilitate educational activities between teachers and students. This platform allows teachers to manage articles and quizzes, while students can join classes, read articles, take quizzes, and review their progress. The application is built using Python with a graphical user interface (GUI) powered by Tkinter, and it utilizes CSV files for data storage.

## Features
- **User Authentication**: Supports login and registration for both teachers and students.
- **Class Management**: Teachers can create classes with unique codes, and students can join using these codes.
- **Article Management**: Teachers can add, edit, and delete educational articles with optional image support.
- **Quiz Management**: Teachers can create, edit, and delete quiz packages with customizable questions and timers.
- **Student Activities**: Students can read articles, take timed quizzes, and review their quiz history with detailed feedback.
- **Progress Tracking**: Records student scores and provides statistical overviews for teachers.

## Installation

### Prerequisites
- Python 3.x
- Required Python libraries:
  - `tkinter` (usually included with Python)
  - `pillow` (for image handling)
  - `matplotlib` (for statistical charts)

Install the required libraries using pip:
```bash
pip install pillow matplotlib
```

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aksanta-elearning
   ```
2. Ensure all `.py` files are in the same directory.
3. Run the application:
   ```bash
   python gui.py
   ```

## Usage
1. **Registration/Login**:
   - New users can register as a teacher or student.
   - Teachers receive a unique class code upon registration.
   - Students can log in and join classes using the provided code.

2. **Teacher Interface**:
   - Manage articles and quizzes within their class.
   - View student statistics, including average scores and quiz completion rates.

3. **Student Interface**:
   - Select a class to access articles and quizzes.
   - Take timed quizzes and review past performances with explanations.

## File Structure
- `data.py`: Handles CSV data storage and retrieval.
- `auth.py`: Manages login and registration menus.
- `models.py`: Defines data models for users, articles, quizzes, and questions.
- `managers.py`: Contains logic for managing users, articles, quizzes, questions, and progress.
- `student.py`: Implements student-specific functionalities.
- `teacher.py`: Implements teacher-specific functionalities.
- `utils.py`: Provides utility functions like multiline input.
- `gui.py`: The main GUI application using Tkinter.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any questions or support, please open an issue on the GitHub repository or contact the maintainers.

## Acknowledgments
- Thanks to the open-source community for Tkinter, Pillow, and Matplotlib.
- Inspired by the need for accessible educational tools.
