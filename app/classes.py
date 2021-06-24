"""
    This module holds several classes for robust data handling
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
import time as dtime


##------- classes that define runner attributes
class RunnerAttr(ABC):

    def __init__(self, pos: int, attr_list: [str]):
        self.pos = pos
        super().__init__()
        self.value = self.get_attr(attr_list)

    @abstractmethod
    def get_attr(self, attr_list: [str]):
        pass


class StringAttr(RunnerAttr):
    pos: int
    value: str

    def get_attr(self, attr_list: [str]) -> str:
        try:
            return str(attr_list[self.pos])
        except ValueError:
            raise ValueError(f"attr at position {self.pos} cannot be converted to a string")


class IntAttr(RunnerAttr):
    pos: int
    value: int

    def get_attr(self, attr_list: [str]):
        try:
            return int(attr_list[self.pos])
        except ValueError:
            raise ValueError(f"attr at position {self.pos} cannot be converted to an integer")


class TimeAttr(RunnerAttr):
    pos: int
    value: dtime

    def get_attr(self, attr_list: [str]):
        try:
            return dtime.strptime(attr_list[self.pos], "%H:%M.%S,%f")
        except ValueError:
            raise ValueError(f"attr at position {self.pos} cannot be converted to an time")


@dataclass
class Runner:
    runner_attrs: dict = {}

    def __init__(self, attr_names:[str], attr_orders:[int], attr_types:[str], attr_list:[str]):
        for n in enumerate(attr_names):
            if attr_types[n].lower() == "varchar":
                self.runner_attrs[attr_names[n]] = StringAttr(attr_orders[n], attr_list)
            elif attr_types[n].lower() == "integer" or "integer" in attr_types[n].lower().split(" "):
                self.runner_attrs[attr_names[n]] = IntAttr(attr_orders[n], attr_list)
            elif attr_types[n].lower() == "timestamp":
                self.runner_attrs[attr_names[n]] = TimeAttr(attr_orders[n], attr_list)

@dataclass
class Marathon:
    year:int
    runners:[Runners]





if __name__ == "__main__":
    my_list = ["2", "abc", "3:20.5,2", "54"]
    cat = IntAttr(0, my_list)
    # print(type(cat), cat)

    time_test= TimeAttr(2, my_list)
    # time_test.get_attr(my_list)
    # print(type(time_test), time_test)
    #
    str_test=StringAttr(0, my_list)
    #
    print(type(str_test), str_test)
    #
    my_names= ["cat", "name", "time", "rank"]
    my_
    my_pos = [0,1,2,3]

    runner = Runner(my_list)
    # print(runner)
