"""
    This module holds several classes for robust data handling
"""

from dataclasses import dataclass, InitVar, field
from abc import ABC, abstractmethod
import time as dtime


##------- classes that define runner attributes
@dataclass
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
            raise ValueError(f"attr {attr_list[self.pos]} cannot be converted to a string")

    def __repr__(self):
        return f"StringAttr( value: {self.value})"


class IntAttr(RunnerAttr):
    pos: int
    value: int

    def get_attr(self, attr_list: [str]):
        try:
            return int(attr_list[self.pos])
        except ValueError:
            raise ValueError(f"attr {attr_list[self.pos]} cannot be converted to an integer")
    def __repr__(self):
        return f"IntAttr( value: {self.value})"

class TimeAttr(RunnerAttr):
    pos: int
    value: dtime

    def get_attr(self, attr_list: [str]):
        try:
            return dtime.strptime(attr_list[self.pos], "%H:%M.%S,%f")
        except ValueError:
            pass
        try:
            return dtime.strptime(attr_list[self.pos], "%M.%S,%f")
        except ValueError:
            pass
        try:
            return dtime.strptime(attr_list[self.pos][:-4], "%H:%M.%S,%f")
        except ValueError:
            return dtime.strptime("0:00.0,0", "%H:%M.%S,%f")

    def __repr__(self):
        return f"TimeAttr ( value: {self.value})"


@dataclass
class Runner:
    runner_attrs: dict

    def __init__(self, config, attr_list: [str]):
        attr_names = config.field_names
        attr_orders = config.field_orders
        attr_types = config.field_types
        # length check
        if not len(attr_names) == len(attr_orders) == len(attr_types) == len(attr_list):
            print(f"missing some values:")
            print(f"names: {len(attr_names)}")
            print(f"types: {len(attr_types)}")
            print(f"order: {len(attr_orders)}")
            print(f"attrs: {len(attr_list)}")
            raise ValueError

        self.runner_attrs ={}
        for n in range(len(attr_orders)):
            check_list=[attr_names[n], attr_orders[n], attr_types[n], attr_list[n]]
            if all([attr_names[n], attr_orders[n], attr_types[n], attr_list[n]]):
                if attr_types[n].lower() == "varchar":
                    self.runner_attrs[attr_names[n]] = StringAttr(attr_orders[n], attr_list)
                elif attr_types[n].lower() == "integer" or "integer" in attr_types[n].lower().split(" "):
                    self.runner_attrs[attr_names[n]] = IntAttr(attr_orders[n], attr_list)
                elif attr_types[n].lower() == "timestamp":
                    test = attr_list[attr_orders[n]]
                    self.runner_attrs[attr_names[n]] = TimeAttr(attr_orders[n], attr_list)

@dataclass
class Marathon:
    year:int
    runners:[Runner]





if __name__ == "__main__":
    import os
    from config import config
    my_list = ["0", "1", "2", "3", "4", "5", "7:12.25,6", None, None]
    runner = Runner(config.field_names, config.field_orders,config.field_types, my_list )
    print(runner)

