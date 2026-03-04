import json
from datetime import datetime

class CreateUserCard:
    user_id_counter = 1
    
    def __init__(self, fullname, email, password, id=None, age=None):
        self.id = id or CreateUserCard.user_id_counter
        CreateUserCard.user_id_counter += 1
        self.fullname = fullname
        self.email = email
        self.password = password
        self.age = age
        self.registration_date = datetime.now()
    
    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "password": self.password,
            "age": self.age,
            "issued_books": [],
            "registration_date": self.registration_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        user = cls(data["fullname"], data["email"], data["password"], 
                  data.get("id"), data.get("age"))
        user.registration_date = datetime.fromisoformat(data["registration_date"])
        return user

def NewUserCard():
    print("Введите данные пользователя:")
    fullname = input("ФИО: ").strip()
    email = input("Email: ").strip()
    password = input("Пароль (мин. 6 символов): ").strip()
    
    if len(password) < 6:
        print("Пароль слишком короткий!")
        return None
    
    try:
        age = int(input("Возраст: ").strip())
    except ValueError:
        print("Неверный возраст!")
        return None
    
    return CreateUserCard(fullname, email, password, age=age)

save_path = r"your_path_user.json"

my_user = NewUserCard()
if my_user:
    user_dict = my_user.to_dict()
    
    try:
        with open(save_path, 'r', encoding='utf-8') as f:
            users = json.load(f)
            if not isinstance(users, list):
                users = [users]
    except FileNotFoundError:
        users = []
    
    users.append(user_dict)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    print("Пользователь создан!")
    print(json.dumps(user_dict, indent=2, ensure_ascii=False))
