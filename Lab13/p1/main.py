from functional import seq
from datetime import date

class Person:
    def __init__(self, first_name, last_name, date_of_birth, email_address):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email_address = email_address

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.date_of_birth})"

persons = [
    Person("John",   "Doe",      date(1960, 11,  3),  "jdoe@example.com"),
    Person("Ellen",  "Smith",    date(1992,  5, 13),  "ellensmith@example.com"),
    Person("Jane",   "White",    date(1986,  2,  1),  "janewhite@example.com"),
    Person("Bill",   "Jackson",  date(1999, 11,  6),  "bjackson@example.com"),
    Person("John",   "Smith",    date(1975,  7, 14),  "johnsmith@example.com"),
    Person("Jack",   "Williams", date(2005,  5, 28),  ""),
]

today = date.today()

youngest = seq(persons) \
    .sorted(key=lambda p: p.date_of_birth, reverse=True) \
    .first()
print("Youngest person:", youngest)

oldest = seq(persons) \
    .sorted(key=lambda p: p.date_of_birth) \
    .first()
print("Oldest person:", oldest)

underage = seq(persons) \
    .filter(lambda p: (today - p.date_of_birth).days // 365 < 18) \
    .to_list()
print("Underage:", underage)

emails = seq(persons) \
    .map(lambda p: p.email_address) \
    .to_list()
print("Emails:", emails)

email_map = seq(persons) \
    .map(lambda p: ((p.first_name + " " + p.last_name), p.email_address)) \
    .to_dict()
print("Email map:", email_map)

by_month = seq(persons) \
    .group_by(lambda p: p.date_of_birth.month) \
    .to_dict()
print("Birthdays by month:", by_month)

born_before, born_after = seq(persons) \
    .partition(lambda p: p.date_of_birth.year <= 1980)
print("Born ≤1980:", born_before.to_list())
print("Born >1980:", born_after.to_list())

# 8) Nume distincte
first_names = seq(persons) \
    .map(lambda p: p.first_name) \
    .distinct() \
    .to_list()
print("Distinct first names:", first_names)

ages = seq(persons) \
    .map(lambda p: (today - p.date_of_birth).days // 365)
average_age = ages.average()
print("Average age:", average_age)

smiths_count = seq(persons) \
    .filter(lambda p: p.last_name == "Smith") \
    .count(lambda _: True)
print("Number of Smiths:", smiths_count)

john = seq(persons) \
    .filter(lambda p: p.first_name == "John") \

print(john if john else "No one named John was found")

thomas_last = seq(persons) \
    .filter(lambda p: p.first_name == "Thomas") \
    .map(lambda p: p.last_name) \

print("Thomas search result:", thomas_last)

any_missing = seq(persons).count(lambda p: p.email_address == "")>0
print("Any missing email:", any_missing)