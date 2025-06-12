import json

class User:
    def __init__(self, username, password, role, class_codes=None):
        self.username = username
        self.password = password
        self.role = role
        self.class_codes = json.loads(class_codes) if class_codes else []

class Article:
    def __init__(self, id, class_code, title, text, image_path):
        self.id = id
        self.class_code = class_code
        self.title = title
        self.text = text
        self.image_path = image_path

class QuizPackage:
    def __init__(self, package_id, class_code, package_name, total_timer):
        self.package_id = package_id
        self.class_code = class_code
        self.package_name = package_name
        self.total_timer = int(total_timer)

class Question:
    def __init__(self, question_id, package_id, question, options, answer, explanation):
        self.question_id = question_id
        self.package_id = package_id
        self.question = question
        self.options = options.split('|') if isinstance(options, str) else options
        self.answer = answer
        self.explanation = explanation