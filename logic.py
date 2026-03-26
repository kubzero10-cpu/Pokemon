from random import randint
import requests
from datetime import datetime,timedelta


class Pokemon:
    pokemons = {}  # Словарь для хранения всех покемонов

    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.type = self.get_type()
        self.hp = randint(200, 400)
        self.power = randint(30, 60)
        self.last_feed_time = datetime.now()
        Pokemon.pokemons[pokemon_trainer] = self

    # Исправленный метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Пробуем разные варианты получения картинки
            try:
                if 'dream_world' in data['sprites']['other']:
                    img_url = data['sprites']['other']['dream_world']['front_default']
                    if img_url:
                        return img_url


            except (KeyError, TypeError):
                pass  # Если что-то пошло не так, используем запасную картинку

        #картинка Пикачу
        return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"

    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    # Метод для получения типа покемона
    def get_type(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['types']:
                return data['types'][0]['type']['name'].capitalize()
        return "Normal"

    # Метод класса для получения информации
    def info(self):
        return f"""Имя твоего покемона: {self.name}
        Тип: {self.type}
        HP: {self.hp}
        Сила: {self.power}
        Тренер: {self.pokemon_trainer}"""

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img


    # Метод атаки
    def attack(self, enemy):
        # Проверка на волшебника
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return f"✨ {enemy.name} применил магический щит! Атака не удалась!"

        # Проверка здоровья
        if self.hp <= 0:
            return f"{self.name} не может атаковать, он проиграл!"
        if enemy.hp <= 0:
            return f"{enemy.name} уже побежден!"

        # Нанесение урона
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"⚔️ Сражение {self.pokemon_trainer} с {enemy.pokemon_trainer}\n{self.name} нанес {self.power} урона!"
        else:
            enemy.hp = 0
            return f"🏆 Победа {self.pokemon_trainer} над {enemy.pokemon_trainer}!"
    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time+delta_time}"

class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)

    def attack(self, enemy):
        return super().attack(enemy)

    def info(self):
        return f"✨ Волшебник\n" + super().info()


    def feed(self, feed_interval = 25, hp_increase = 20 ):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time+delta_time}"



class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)

    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\n💪 Боец применил супер атаку силой: {super_power}"

    def info(self):
        return f"⚡ Боец\n" + super().info()

    def feed(self, feed_interval = 10, hp_increase = 15 ):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time+delta_time}"
