"""
Необходимо создать 3 класса и взаимосвязь между ними (Student, Teacher,
Homework)
Наследование в этой задаче использовать не нужно.
Для работы с временем использовать модуль datetime

1. Homework принимает на вход 2 атрибута: текст задания и количество дней
на это задание
Атрибуты:
    text - текст задания
    deadline - хранит объект datetime.timedelta с количеством
    дней на выполнение
    created - c точной датой и временем создания
Методы:
    is_active - проверяет не истело ли время на выполнение задания,
    возвращает boolean

2. Student
Атрибуты:
    last_name
    first_name
Методы:
    do_homework - принимает объект Homework и возвращает его же,
    если задание уже просрочено, то печатет 'You are late' и возвращает None

3. Teacher
Атрибуты:
    last_name
     first_name
Методы:
    create_homework - текст задания и количество дней на это задание,
    возвращает экземпляр Homework
    Обратите внимание, что для работы этого метода не требуется сам объект.

PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""

import datetime


class DeadlineError(Exception):
    def __init__(self, msg):
        self.msg = msg
        print("You are late")


class Person:
    first_name = ""
    last_name = ""


class Homework:
    def __init__(
        self,
        text: str,
        deadline: datetime.timedelta,
    ) -> None:
        self.text = text
        self.deadline = deadline
        self.created = datetime.datetime.now()

    def is_active(
        self,
    ):
        return (self.created.day + self.deadline) > datetime.datetime.now().day


class Student(Person):
    def __init__(self, last_name: str, first_name: str) -> None:
        self.last_name = last_name
        self.first_name = first_name

    def do_homework(self, homework: Homework):
        if not homework.is_active():
            raise DeadlineError("You are late") from None
        return HomeworkResult(homework, self, homework.text)


class HomeworkResult:
    def __init__(self, homework, author: Student, solution: str) -> None:
        if not isinstance(homework, Homework):
            raise TypeError("You gave a not Homework object")
        self.homework = homework
        self.solution = solution
        self.author = author
        self.created = datetime.datetime.now()


class Teacher(Person):
    homework_done = dict()

    def __init__(self, last_name: str, first_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def create_homework(self, text: str, days: datetime.timedelta.days):
        return Homework(text, days)

    def check_homework(self, result: HomeworkResult):
        if len(result.solution) > 5:
            self.homework_done.update({result.homework: result})
            return True
        return False

    def reset_result(self, homework: Homework):
        if homework:
            self.homework_done.pop(homework)
        else:
            self.homework_done.clear()


if __name__ == "__main__":
    teacher = Teacher("Daniil", "Shadrin")
    student = Student("Roman", "Petrov")
    teacher.last_name  # Daniil
    student.first_name  # Petrov

    expired_homework = teacher.create_homework("Learn functions", 0)
    expired_homework.created  # Example: 2019-05-26 16:44:30.688762
    expired_homework.deadline  # 0:00:00
    expired_homework.text  # 'Learn functions'

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too("create 2 simple classes", 5)
    oop_homework.deadline  # 5 days, 0:00:00

    student.do_homework(oop_homework)
    student.do_homework(expired_homework)  # You are late
