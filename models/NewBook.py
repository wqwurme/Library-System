import json
from datetime import datetime

class NewBook:
    def __init__(self, title, author, genre, availability):
        self.title = title
        self.author = author
        self.genre = genre
        self.availability = availability
        self.added_date = datetime.now()
    
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "availability": self.availability,
            "added_date": self.added_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        book = cls(data["title"], data["author"], data["genre"], data["availability"])
        book.added_date = datetime.fromisoformat(data["added_date"])
        return book

def create_book_from_input():
    print("Введите данные книги:")
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    genre = input("Жанр: ").strip()
    availability = input("Доступна (y/n): ").strip().lower() == 'y'
    
    return NewBook(title, author, genre, availability)

save_path = r"your_path_books.json"

my_book = create_book_from_input()
if my_book:
    book_dict = my_book.to_dict()
    
    try:
        with open(save_path, 'r', encoding='utf-8') as f:
            books = json.load(f)
            if not isinstance(books, list):
                books = [books]
    except FileNotFoundError:
        books = []
    
    books.append(book_dict)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    
    print("Книга добавлена!")
    print(json.dumps(book_dict, indent=2, ensure_ascii=False))
