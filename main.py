import json
import datetime
import os

BOOKS_PATH = r"your_path_books.json"
USERS_PATH = r"your_path_user.json"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return [data]
            return data if isinstance(data, list) else []
    except:
        return []

def save_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data if isinstance(data, list) else [data], f, ensure_ascii=False, indent=2)

def main_menu():
    while True:
        print("\n" + "="*50)
        print("БИБЛИОТЕКА - ГЛАВНОЕ МЕНЮ")
        print("="*50)
        print("1. Добавить книгу")
        print("2. Добавить пользователя")
        print("3. Выдать книгу")
        print("4. Вернуть книгу")
        print("5. Список книг")
        print("6. Список пользователей")
        print("0. Выход")
        print("="*50)
        
        choice = input("Выбор: ").strip()
        
        if choice == "1":
            add_book()
        elif choice == "2":
            add_user()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            show_books()
        elif choice == "6":
            show_users()
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Неверный выбор!")

def add_book():
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    genre = input("Жанр: ").strip()
    avail = input("Доступна (y/n): ").strip().lower() == 'y'
    
    books = load_json(BOOKS_PATH)
    book_id = max([b.get('id', 0) for b in books], default=0) + 1
    
    new_book = {
        "id": book_id,
        "title": title,
        "author": author,
        "genre": genre,
        "availability": avail,
        "added_date": datetime.datetime.now().isoformat()
    }
    books.append(new_book)
    save_json(BOOKS_PATH, books)
    print(f"Книга '{title}' добавлена. ID: {book_id}")

def add_user():
    name = input("ФИО: ").strip()
    email = input("Email: ").strip()
    age = input("Возраст: ").strip()
    
    users = load_json(USERS_PATH)
    user_id = max([u.get('id', 0) for u in users], default=0) + 1
    
    new_user = {
        "id": user_id,
        "fullname": name,
        "email": email,
        "age": age,
        "issued_books": []
    }
    users.append(new_user)
    save_json(USERS_PATH, users)
    print(f"Пользователь '{name}' зарегистрирован. ID: {user_id}")

def issue_book():
    books = load_json(BOOKS_PATH)
    users = load_json(USERS_PATH)
    
    avail_books = [b for b in books if b.get('availability')]
    if not avail_books:
        print("Нет доступных книг")
        return
    if not users:
        print("Нет пользователей")
        return
        
    print("\nДоступные книги:")
    for i, b in enumerate(avail_books, 1):
        print(f"{i}. {b['title']} - {b['author']}")
    
    try:
        bid = int(input("Номер книги: ")) - 1
        uid = int(input("Номер пользователя: ")) - 1
        
        if 0 <= bid < len(avail_books) and 0 <= uid < len(users):
            book = avail_books[bid]
            user = users[uid]
            
            book['availability'] = False
            book['issued_to'] = user['id']
            book['issue_date'] = datetime.datetime.now().isoformat()
            
            user['issued_books'].append({
                'id': book['id'],
                'title': book['title'],
                'issue_date': book['issue_date']
            })
            
            save_json(BOOKS_PATH, books)
            save_json(USERS_PATH, users)
            print(f"Книга '{book['title']}' выдана пользователю '{user['fullname']}'")
        else:
            print("Неверный номер")
    except ValueError:
        print("Введите число")

def return_book():
    books = load_json(BOOKS_PATH)
    issued = [b for b in books if not b.get('availability')]
    if not issued:
        print("Все книги возвращены")
        return
        
    print("\nВыданные книги:")
    for i, b in enumerate(issued, 1):
        print(f"{i}. {b['title']} - {b['author']}")
    
    try:
        bid = int(input("Номер для возврата: ")) - 1
        if 0 <= bid < len(issued):
            book = issued[bid]
            book['availability'] = True
            book['issued_to'] = None
            book['issue_date'] = None
            
            users = load_json(USERS_PATH)
            for user in users:
                if 'issued_books' in user:
                    user['issued_books'] = [bk for bk in user['issued_books'] if bk['id'] != book['id']]
            
            save_json(BOOKS_PATH, books)
            save_json(USERS_PATH, users)
            print(f"Книга '{book['title']}' возвращена")
    except ValueError:
        print("Введите число")

def show_books():
    books = load_json(BOOKS_PATH)
    avail = sum(1 for b in books if b.get('availability'))
    print(f"\nВсего книг: {len(books)}, Доступно: {avail}, Выдано: {len(books)-avail}")
    for b in books[:5]:
        status = "Доступна" if b.get('availability') else "Выдана"
        print(f"{status}: {b['title']} - {b['author']}")

def show_users():
    users = load_json(USERS_PATH)
    print(f"\nВсего пользователей: {len(users)}")
    for u in users:
        books_cnt = len(u.get('issued_books', []))
        print(f"{u['fullname']} - выданных книг: {books_cnt}")

if __name__ == "__main__":
    main_menu()
