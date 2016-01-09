"""
Класс расписания
"""

# TODO: проверить, чтобы везде использовались ЦЕЛЫЕ ЧИСЛА

from copy import deepcopy
from classes.exception import BaseException as BException


class UncompatibleSchedulesException(BException):
    pass


class Item:
    """
    Базовый класс элемента расписания
    """
    def __init__(self, time):
        self.time = time  # свойство "занимаемое время"


class Wait(Item):
    """
    Ожидание в расписании. Наследуется от Item
    """
    def __str__(self, *args, **kwargs):
        return 'Wait(time={})'.format(self.time)


class Task(Item):
    """
    Задача в расписании
    """
    def __init__(self, name, time):
        super().__init__(time)
        self.name = name  # имя задачи

    def __str__(self, *args, **kwargs):
        return 'Task(name={}, time={})'.format(self.name, self.time)


class Schedule:
    """
    Класс расписания. В нём хранятся расписания для каждого процессора в виде
    списка Item (либо Task, либо Wait)
    """
    def __init__(self, processors):
        self._data = {p: [] for p in processors}

    def __iter__(self):  # синтаксический сахар для итерации по расписанию
        return iter(self._data.items())

    def add_item(self, processor, item):
        """
        Добавление элемента расписания
        :param processor:
        :param item:
        :return:
        """
        self._data[processor].append(item)

    def add_wait(self, processor, time):
        """
        Добавляет ожидание
        :param processor:
        :param time:
        :return:
        """
        self.add_item(processor, Wait(int(time)))

    def add_task(self, processor, name, time):
        """
        Добавляет таск
        :param processor:
        :param name:
        :param time:
        :return:
        """
        self.add_item(processor, Task(name, int(time)))

    def busy_time(self, processor):
        """
        Вычисляет полное время занятости заданного процессора
        :param processor:
        :return:
        """
        return sum(item.time for item in self._data[processor])

    def max_busy_time(self):
        """
        Вычисляет максимальное время занятости по всем процессорам (время
        занятости по расписанию)
        :return:
        """
        return max(
            sum(item.time for item in items)
            for _, items in self
        )

    def _iterate_task_flow_times(self):
        """
        Генератор для последовательности значений flow time
        для каждой таски
        :return:
        """
        for _, items in self:
            time_passed = 0
            for item in items:
                time_passed += item.time
                if isinstance(item, Task):
                    yield (item, time_passed)

    def task_flow_times(self):
        """
        Возвращает словарь вида {таск: flow time, ...}
        :return:
        """
        return {task.name: flow_time for task, flow_time in self._iterate_task_flow_times()}

    def total_flow_time(self):
        """
        Возвращает total flow time расписания
        :return:
        """
        return sum(map(lambda x: x[1], self._iterate_task_flow_times()))

    def _join_waits(self):
        """
        Склеивает находящиеся рядом Wait в один с суммарным их временем
        :return:
        """
        for _, items in self:
            i = 1
            item_count = len(items)
            while i < item_count:
                if isinstance(items[i - 1], Wait) and isinstance(items[i], Wait):
                    items[i].time = items[i].time + items[i-1].time
                    del items[i-1]
                    item_count -= 1
                else:
                    i += 1

    def _trim_waits(self):
        """
        Удаляет незначащие Wait с конца расписания
        :return:
        """
        for _, items in self:
            while items and isinstance(items[-1], Wait):
                items.pop()

    def normalize(self):
        """
        Нормализация расписания
        :return:
        """
        self._join_waits()
        self._trim_waits()

    def equalize_busy_time(self):
        """
        Adds waits for processors if needed so each processor is busy for the same time
        """
        busy_times = {p: self.busy_time(p) for p in self.get_processors()}
        max_busy_time = max(busy_times.values())
        for processor in self.get_processors():
            if busy_times[processor] < max_busy_time:
                self.add_wait(processor, max_busy_time - busy_times[processor])

    def get_processors(self):
        """
        Аксессор для processors
        :rtype list
        :return:
        """
        return list(self._data.keys())

    def get_task_intervals(self):
        """
        Возвращает интервалы выполнения каждой таски
        :return: Словарь, в котором для каждого процессора определен список,
        в котором каждый элемент - (имя таски, время её начала, время её завершения)
        """
        result = {}
        for processor, items in self:
            result[processor] = []
            item_start = 0
            for item in items:
                if isinstance(item, Task):
                    result[processor].append((item.name, item_start, item_start + item.time))
                item_start += item.time
        return result

    def copy(self):
        """
        Возвращает копию расписания
        :rtype Schedule
        :return:
        """
        return deepcopy(self)

    def concat(self, other):
        """
        Concatenate the given schedule to self

        :param Schedule other:
        """
        if not isinstance(other, Schedule):
            raise TypeError('Schedule can only be concatenated with another Schedule')
        if set(self.get_processors()).symmetric_difference(other.get_processors()):
            raise UncompatibleSchedulesException('operand has different processor data')
        self.equalize_busy_time()
        for processor, items in other:
            for item in items:
                self.add_item(processor, item)
        self.normalize()
        return self

    def __str__(self, *args, **kwargs):
        result = 'Schedule\nTotal flow time = {}'.format(self.total_flow_time())
        for processor, items in self:
            result += '\n{}: {}'.format(processor, ', '.join(str(item) for item in items))
        return result

    def __add__(self, other):
        """
        Перегрузка оператора "+"
        :param other:
        :return:
        """
        result = self.copy()
        result.concat(other)
        return result

if __name__ == '__main__':
    t = Schedule([0, 1])
    t.add_item(0, Task('a', 3))
    t.add_item(0, Task('b', 4))
    t.add_item(0, Task('bb', 6))
    t.add_item(1, Wait(10))
    t.add_item(1, Task('c', 5))
    t.add_item(0, Wait(1))
    t.add_item(0, Wait(1))
    t.add_item(0, Wait(1))
    t.add_item(0, Wait(1))
    t.add_item(0, Task('d', 10))
    t.add_item(0, Task('e', 20))
    t.add_item(0, Wait(5))
    print(t.max_busy_time()); print(t.total_flow_time()); print(t)
    t.equalize_busy_time()
    print(t.max_busy_time()); print(t.total_flow_time()); print(t)
    t.normalize()
    print(t.max_busy_time()); print(t.total_flow_time()); print(t)
    t = t + t
    print(t.max_busy_time()); print(t.total_flow_time()); print(t)
