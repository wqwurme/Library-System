import json
import datetime

path_books = r"your_path_books.json"
path_user = r"your_path_user.json"

def load_data():
    try:
        with open(path_books, 'r', encoding='utf-8') as file:
            data_book = json.load(file)
            if isinstance(data_book, dict):
                data_book = [data_book]
            elif isinstance(data_book, str):
                print("Ошибка: Books.json содержит строку!")
                return None, None
    except FileNotFoundError:
        data_book = []
    
    try:
        with open(path_user, 'r', encoding='utf-8') as file:
            data_user = json.load(file)
            if isinstance(data_user, dict):
                data_user = [data_user]
            elif isinstance(data_user, str):
                print("Ошибка: User.json содержит строку!")
                return None, None
    except FileNotFoundError:
        data_user = []
    
    return data_book, data_user

def save_data(data_book, data_user):
    with open(path_books, 'w', encoding='utf-8') as file:
        json.dump(data_book, file, ensure_ascii=False, indent=2)
    with open(path_user, 'w', encoding='utf-8') as file:
        json.dump(data_user, file, ensure_ascii=False, indent=2)

def issue_books():
    data_book, data_user = load_data()
    if not data_book or not data_user:
        print("Нет данных для работы!")
        return None
    
    print("=== ВЫДАЧА КНИГ ===")
    
    available_books = []
    for book in data_book:
        if isinstance(book, dict) and book.get('availability', True):
            available_books.append(book)
    
    if not available_books:
        print("Извините, нет доступных книг")
        return None
    
    print("\nДоступные книги:")
    for i, book in enumerate(available_books, 1):
        print(f"{i}. {book['title']} - {book['author']} ({book.get('year', 'Год неизвестен')})")
    
    while True:
        try:
            choice = input("\nВведите номер книги (или 'q' для выхода): ").strip()
            if choice.lower() == 'q':
                return None
            book_index = int(choice) - 1
            if 0 <= book_index < len(available_books):
                selected_book = available_books[book_index]
                break
            print("Неверный номер!")
        except ValueError:
            print("Введите число!")
    
    print("\nПользователи:")
    for i, user in enumerate(data_user, 1):
        if isinstance(user, dict):
            print(f"{i}. {user.get('fullname', 'Без имени')} (ID: {user.get('id', i)})")
    
    while True:
        try:
            user_choice = input("Введите номер пользователя: ").strip()
            user_index = int(user_choice) - 1
            if 0 <= user_index < len(data_user):
                selected_user = data_user[user_index]
                if isinstance(selected_user, dict):
                    break
            print("Неверный номер!")
        except ValueError:
            print("Введите число!")
    
    book_id = selected_book.get('id') or selected_book.get('title')
    user_id = selected_user.get('id')
    
    if 'issued_books' not in selected_user:
        selected_user['issued_books'] = []
    
    if any(b.get('id') == book_id for b in selected_user['issued_books']):
        print("У пользователя уже есть эта книга!")
        return None
    
    selected_user['issued_books'].append({
        'id': book_id,
        'title': selected_book['title'],
        'issue_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    selected_book['availability'] = False
    selected_book['issued_to'] = user_id
    selected_book['issue_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    save_data(data_book, data_user)
    
    print(f"\nКнига '{selected_book['title']}' выдана {selected_user.get('fullname', 'пользователю')}!")
    return True

if __name__ == "__main__":
    result = issue_books()
