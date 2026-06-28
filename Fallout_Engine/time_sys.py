import time

class TimeManager:
    def __init__(self):
        self.year = 2161
        self.month = 12
        self.day = 5
        self.hour = 8
        self.minute = 0
        self.second = 0

        self.last_real_time = time.time()
    
    def advance_time(self, seconds_to_add):
        self.second += seconds_to_add

        if self.second >= 60:
            self.minute += self.second // 60
            self.second %= 60
        
        if self.minute >= 60:
            self.hour += self.minute // 60
            self.minute %= 60
        
        if self.hour >= 24:
            self.day += self.hour // 24
            self.hour %= 24

        if self.day > 30:
            self.month += self.day // 30
            self.day = (self.day % 30) or 1
        
        if self.month > 12:
            self.year += self.month // 12
            self.month = (self.month % 12) or 1

    def update_real_time(self):
        current_real_time = time.time()
        passed_seconds = int(current_real_time - self.last_real_time)

        if passed_seconds > 0:
            self.advance_time(passed_seconds)
            self.last_real_time = current_real_time
    
    def get_time_string(self):
        months_names = {1: "Янв", 2: "Фев", 3: "Мар", 4: "Апр", 5: "Май", 6: "Июн", 7: "Июл", 8: "Авг", 9: "Сен", 10: "Окт", 11: "Ноя", 12: "Дек"}
        return f"{self.day:02d} {months_names[self.month]} {self.year} | {self.hour:02d}:{self.minute:02d}:{self.second:02d}"