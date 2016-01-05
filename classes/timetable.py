from copy import deepcopy


class UncompatibleTimetablesException(Exception):
    pass


class Item:
    def __init__(self, time):
        self.time = time


class Wait(Item):
    def __str__(self, *args, **kwargs):
        return 'Wait(time={})'.format(self.time)


class Task(Item):
    def __init__(self, name, time):
        super().__init__(time)
        self.name = name
        self.time = time

    def __str__(self, *args, **kwargs):
        return 'Task(name={}, time={})'.format(self.name, self.time)


class Timetable:
    def __init__(self, processors):
        self._data = {p: [] for p in processors}

    def __iter__(self):
        return iter(self._data.items())

    def add_item(self, processor, item):
        self._data[processor].append(item)

    def add_wait(self, processor, time):
        self.add_item(processor, Wait(time))

    def add_task(self, processor, name, time):
        self.add_item(processor, Task(name, time))

    def busy_time(self, processor):
        return sum(item.time for item in self._data[processor])

    def max_busy_time(self):
        return max(
            sum(item.time for item in items)
            for _, items in self
        )

    def total_flow_time(self):
        result = 0
        for _, items in self:
            time_passed = 0
            for item in items:
                time_passed += item.time
                if isinstance(item, Task):
                    result += time_passed
        return result

    def _join_waits(self):
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
        for _, items in self:
            while items and isinstance(items[-1], Wait):
                items.pop()

    def normalize(self):
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
        return list(self._data.keys())

    def copy(self):
        """
        :rtype Timetable
        :return:
        """
        return deepcopy(self)

    def concat(self, other):
        """
        :param Timetable other:
        :rtype Timetable
        :return: Concatenation result
        """
        if set(self.get_processors()).symmetric_difference(other.get_processors()):
            raise UncompatibleTimetablesException()
        result = self.copy()  # type: Timetable
        result.equalize_busy_time()
        for processor, items in other:
            for item in items:
                result.add_item(processor, item)
        result.normalize()
        return result

    def __str__(self, *args, **kwargs):
        result = 'Timetable'
        for processor, items in self:
            result += '\n{}: {}'.format(processor, ', '.join(str(item) for item in items))
        return result


if __name__ == '__main__':
    t = Timetable([0, 1])
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
    t = t.concat(t)
    print(t.max_busy_time()); print(t.total_flow_time()); print(t)
