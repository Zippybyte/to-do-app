from dataclasses import dataclass
from datetime import datetime

@dataclass
class RepeatDate:
    type: int # Daily, Weekly, Monthly, MonthlyWeek, Yearly
    specifier: set[int] # MonthlyWeek week(Week of the month), Yearly month
    day: set[int] # Set of days in Week/Month/MonthlyWeek week(Days of the week of the month)/Yearly day/Yearly month day
    time: datetime # Reset time

@dataclass
class CompletionType:
    type: int # Checkbox(binary), multistate(Not called, called, responded no, responeded yes)

@dataclass
class ToDoItem:
    id: int
    name: str
    description: str
    repetition: RepeatDate
    categories: list[str] # Refactor later for indexes of strings
    tags: list[str]
    creation_date: datetime
    due_by_date: datetime
    last_completed: datetime # Possibly replace by history system
    completion_state: int
    completion_type: CompletionType

@dataclass
class ToDoTemplate: # All nullable if possible
    id: int
    repetition: RepeatDate
    categories: list[str] # Refactor later for indexes of strings
    tags: list[str]
    completion_state: int
    completion_type: CompletionType

@dataclass
class HistoryItem:
    id: int
    todo_item_id: ToDoItem
    completion_notes: str
    date_completed: datetime