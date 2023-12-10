import hashlib
import re
import random
from faker import Faker

# Класс для хранения и генерации уникальных идентификаторов
class IdCounter:
    def __init__(self):
        self._id = 0

    def get_id(self):
        self._id += 1
        return self._id

# Класс для создания и проверки пароля
class Password:
    @staticmethod
    def get(password):
        if not isinstance(password, str) or len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[a-zA-Z]', password):
            raise ValueError('Invalid password')
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check(password, hash_value):
        return hashlib.sha256(password.encode()).hexdigest() == hash_value

# Класс для хранения информации о продукте
class Product:
    id_counter = IdCounter()

    def __init__(self, name, price, rating):
        if not isinstance(name, str) or not isinstance(price, (int, float)) or not isinstance(rating, (int, float)):
            raise TypeError('Invalid attribute type')
        if not name:
            raise ValueError('Name cannot be empty')
        if price <= 0 or rating < 0:
            raise ValueError('Invalid attribute value')

        self._id = Product.id_counter.get_id()
        self._name = name
        self._price = price
        self._rating = rating

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError('Invalid price')
        self._price = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError('Invalid rating')
        self._rating = value

    def __str__(self):
        return f'{self._id}_{self._name}'

    def __repr__(self):
        return f'Product(id={self._id}, name={self._name}, price={self._price}, rating={self._rating})'

# Класс для хранения информации о корзине пользователя
class Cart:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError('Invalid product')
        self._items.append(product)

    def remove_product(self, product):
        if product in self._items:
            self._items.remove(product)

    def calculate_total_price(self):
        total_price = 0
        for item in self._items:
            total_price += item.price
        return total_price

# Класс для хранения информации о пользователе
class User:
    id_counter = IdCounter()

    def __init__(self, username, password):
        if not isinstance(username, str) or not re.search(r'^\w+$', username):
            raise ValueError('Invalid username')
        if not isinstance(password, str) or len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[a-zA-Z]', password):
            raise ValueError('Invalid password')

        self._id = User.id_counter.get_id()
        self._username = username
        self._password = Password.get(password)
        self._cart = Cart()

    @property
    def cart(self):
        return self._cart

    def __str__(self):
        return f'User(id={self._id}, username={self._username}, password=password1)'

    def __repr__(self):
        return f'User(id={self._id}, username={self._username}, password=password1'

# Класс для работы с магазином, включая аутентификацию и управление корзиной
class Store:
    # Инициализация магазина
    def __init__(self):
        self._users = []
        self.fake = Faker()
        self.products = self.generate_products(10)

    # Метод для аутентификации пользователя
    def authenticate_user(self):
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        for user in self._users:
            if user._username == username and Password.check(password, user._password):
                return user
        return None

    # Метод для добавления продукта в корзину пользователя
    def add_product_to_cart(self):
        user = self.authenticate_user()
        if user:
            print('Available products:')
            for product in self.products:
                print(f'Product ID: {product._id}')
                print(f'Product Name: {product._name}')
                print(f'Product Price: ${product._price}')
                print(f'Product Rating: {product._rating}')
                print()

            product_id = int(input('Enter product ID to add to cart: '))
            product = self.get_product_by_id(product_id)
            if product:
                user.cart.add_product(product)
                print(f'Product {product._name} added to cart')
            else:
                print(f'Product with ID {product_id} not found')
        else:
            print('Authentication failed')

    # Метод для удаления  продукта в корзину пользователя
    def remove_product_from_cart(self):
        user = self.authenticate_user()
        if user:
            print('Cart:')
            for item in user.cart.items:
                print(f'Product ID: {item._id}')
                print(f'Product Name: {item._name}')
                print(f'Product Price: ${item._price}')
                print(f'Product Rating: {item._rating}')
                print()

            product_id = int(input('Enter product ID to remove from cart: '))
            for product in user.cart.items:
                if product._id == product_id:
                    user.cart.remove_product(product)
                    print(f'Product {product._name} removed from cart')
                    return
            print(f'Product with ID {product_id} not found in cart')
        else:
            print('Authentication failed')

    # Метод для просмотра содержимого корзины пользователя
    def view_cart(self):
        user = self.authenticate_user()
        if user:
            print('Cart:')
            for item in user.cart.items:
                print(f'Product ID: {item._id}')
                print(f'Product Name: {item._name}')
                print(f'Product Price: ${item._price}')
                print(f'Product Rating: {item._rating}')
                print()
            print('Total price:', user.cart.calculate_total_price())
        else:
            print('Authentication failed')

    def get_product_by_id(self, product_id):
        for product in self.products:
            if product._id == product_id:
                return product
        return None

    def generate_products(self, num_products):
        products = []
        for _ in range(num_products):
            name = self.fake.word()
            price = round(random.uniform(1, 100), 2)
            rating = round(random.uniform(1, 5), 2)
            products.append(Product(name, price, rating))
        return products


store = Store()
store._users.append(User('user1', 'password123'))

while True:
    print('\nMenu:')
    print('1. Add product to cart')
    print('2. Remove product from cart')
    print('3. View cart')
    print('4. Exit')

    choice = input('Enter your choice: ')
    if choice == '1':
        store.add_product_to_cart()
    elif choice == '2':
        store.remove_product_from_cart()
    elif choice == '3':
        store.view_cart()
    elif choice == '4':
        break
    else:
        print('Invalid choice. Try again.')

# Принцип работы программы:
# - Магазин имеет класс Store и позволяет пользователям аутентифицироваться, добавлять товары в корзину и просматривать ее содержимое.
# - Каждый пользователь имеет свой уникальный идентификатор, имя пользователя и хэш-значение пароля, создается корзина для пользователя.
# - Класс Product представляет товары в магазине и содерит информацию о продукте, такую как цена, рейтинг и уникальный идентификатор.
# - Класс Cart представляет корзину пользователя и позволяет добавлять и удалять товары, а также вычислять общую цену товаров в корзине.
# - Класс Password отвечает за создание хэш-значения пароля и его проверку.
# - Программа использует библиотеку Faker для генерации фэйковых данных, таких как названия продуктов, а также библиотеку random для генерации случайных цен и рейтингов для товаров.