import uuid
import json
from datetime import datetime
import hashlib

class UserManager:
    def __init__(self, store):
        self.store = store

    def register(self, username, password, role, class_name=None):
        users = self.store.read_all(self.store.user_file)
        if any(u['username'] == username for u in users):
            return False, 'Username sudah digunakan.'
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        class_codes = [str(uuid.uuid4())[:8]] if role == 'guru' else []
        row = {
            'username': username,
            'password': hashed_password,
            'role': role,
            'class_codes': json.dumps(class_codes)
        }
        self.store.append(self.store.user_file, row)
        if role == 'guru' and class_name:
            class_row = {
                'class_code': class_codes[0],
                'class_name': class_name
            }
            self.store.append(self.store.class_file, class_row)
        return True, class_codes[0] if role == 'guru' else None

    def login(self, username, password):
        from models import User
        users = self.store.read_all(self.store.user_file)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for u in users:
            if u['username'] == username and u['password'] == hashed_password:
                return User(username, u['password'], u['role'], u['class_codes'])
        return None

    def join_class(self, username, class_code):
        classes = self.store.read_all(self.store.class_file)
        if not any(cls['class_code'] == class_code for cls in classes):
            return False, "Kode kelas tidak valid."
        users = self.store.read_all(self.store.user_file)
        for u in users:
            if u['username'] == username:
                class_codes = json.loads(u['class_codes'])
                if class_code in class_codes:
                    return False, "Anda telah bergabung ke kelas tersebut."
                class_codes.append(class_code)
                u['class_codes'] = json.dumps(class_codes)
                self.store.overwrite(self.store.user_file, users, users[0].keys())
                return True, "Berhasil bergabung ke kelas!"
        return False, "Pengguna tidak ditemukan."

    def list_users(self):
        from models import User
        rows = self.store.read_all(self.store.user_file)
        return [User(**r) for r in rows]

class ArticleManager:
    def __init__(self, store):
        self.store = store

    def list(self, class_code):
        from models import Article
        rows = self.store.read_all(self.store.article_file)
        return [Article(**r) for r in rows if r['class_code'] == class_code]

    def create(self, class_code, title, text, image_path):
        art_id = str(uuid.uuid4())[:8]
        row = {
            'id': art_id,
            'class_code': class_code,
            'title': title,
            'text': text,
            'image_path': image_path
        }
        self.store.append(self.store.article_file, row)
        return art_id

    def update(self, art_id, **kwargs):
        articles = self.store.read_all(self.store.article_file)
        for a in articles:
            if a['id'] == art_id:
                for k, v in kwargs.items():
                    a[k] = v
        self.store.overwrite(self.store.article_file, articles, articles[0].keys())

    def delete(self, art_id):
        articles = self.store.read_all(self.store.article_file)
        filtered = [a for a in articles if a['id'] != art_id]
        self.store.overwrite(self.store.article_file, filtered, articles[0].keys())

class QuizPackageManager:
    def __init__(self, store):
        self.store = store

    def list(self, class_code):
        from models import QuizPackage
        rows = self.store.read_all(self.store.quiz_file)
        return [QuizPackage(**r) for r in rows if r['class_code'] == class_code]

    def create(self, class_code, package_name, total_timer):
        package_id = str(uuid.uuid4())[:8]
        row = {
            'package_id': package_id,
            'class_code': class_code,
            'package_name': package_name,
            'total_timer': str(total_timer)
        }
        self.store.append(self.store.quiz_file, row)
        return package_id

    def delete(self, package_id):
        packages = self.store.read_all(self.store.quiz_file)
        filtered = [p for p in packages if p['package_id'] != package_id]
        self.store.overwrite(self.store.quiz_file, filtered, packages[0].keys())
        questions = self.store.read_all(self.store.question_file)
        filtered_questions = [q for q in questions if q['package_id'] != package_id]
        self.store.overwrite(self.store.question_file, filtered_questions, questions[0].keys())

class QuestionManager:
    def __init__(self, store):
        self.store = store

    def list(self, package_id):
        from models import Question
        rows = self.store.read_all(self.store.question_file)
        return [Question(**r) for r in rows if r['package_id'] == package_id]

    def create(self, package_id, question, options, answer, explanation):
        question_id = str(uuid.uuid4())[:8]
        row = {
            'question_id': question_id,
            'package_id': package_id,
            'question': question,
            'options': '|'.join(options),
            'answer': answer,
            'explanation': explanation
        }
        self.store.append(self.store.question_file, row)
        return question_id

    def update(self, question_id, **kwargs):
        questions = self.store.read_all(self.store.question_file)
        for q in questions:
            if q['question_id'] == question_id:
                for k, v in kwargs.items():
                    q[k] = '|'.join(v) if k == 'options' else v
        self.store.overwrite(self.store.question_file, questions, questions[0].keys())

    def delete(self, question_id):
        questions = self.store.read_all(self.store.question_file)
        filtered = [q for q in questions if q['question_id'] != question_id]
        self.store.overwrite(self.store.question_file, filtered, questions[0].keys())

class ProgressManager:
    def __init__(self, store):
        self.store = store

    def record(self, username, package_id, score, answers):
        row = {
            'username': username,
            'package_id': package_id,
            'score': str(score),
            'answers': '|'.join(answers),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.store.append(self.store.progress_file, row)

    def list_by_user(self, username):
        rows = self.store.read_all(self.store.progress_file)
        return [r for r in rows if r['username'] == username]

    def list_by_class(self, class_code):
        packages = self.store.read_all(self.store.quiz_file)
        package_ids = [p['package_id'] for p in packages if p['class_code'] == class_code]
        rows = self.store.read_all(self.store.progress_file)
        return [r for r in rows if r['package_id'] in package_ids]

    def list_by_user_and_class(self, username, class_code):
        progresses = self.list_by_class(class_code)
        return [p for p in progresses if p['username'] == username]

    def has_taken_package(self, username, package_id):
        rows = self.store.read_all(self.store.progress_file)
        return any(r['username'] == username and r['package_id'] == package_id for r in rows)