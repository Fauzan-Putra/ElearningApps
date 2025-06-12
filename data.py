import csv
import os

class CSVDataStore:
    def __init__(self, folder='data'):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)
        self.user_file = os.path.join(folder, 'users.csv')
        self.article_file = os.path.join(folder, 'articles.csv')
        self.quiz_file = os.path.join(folder, 'quizzes.csv')
        self.question_file = os.path.join(folder, 'questions.csv')
        self.progress_file = os.path.join(folder, 'progress.csv')
        self.class_file = os.path.join(folder, 'classes.csv')
        self._init_files()

    def _init_files(self):
        for file, headers in [
            (self.user_file, ['username', 'password', 'role', 'class_codes']),
            (self.article_file, ['id', 'class_code', 'title', 'text', 'image_path']),
            (self.quiz_file, ['package_id', 'class_code', 'package_name', 'total_timer']),
            (self.question_file, ['question_id', 'package_id', 'question', 'options', 'answer', 'explanation']),
            (self.progress_file, ['username', 'package_id', 'score', 'answers', 'timestamp']),
            (self.class_file, ['class_code', 'class_name'])
        ]:
            if not os.path.exists(file):
                with open(file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)

    def read_all(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def append(self, file_path, row_dict):
        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row_dict.keys())
            writer.writerow(row_dict)

    def overwrite(self, file_path, rows_list, fieldnames):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_list)

    def get_class_name(self, class_code):
        classes = self.read_all(self.class_file)
        for cls in classes:
            if cls['class_code'] == class_code:
                return cls['class_name']
        return None