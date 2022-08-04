import json


def add_infor():
    with open("main.json") as json_file:
        data = json.load(json_file)
        temp = data
        ["student"]
        y = {"name": input("Name: "), "crs": input("Course: "), "year": input("Year: "), "major": input("Major: "),
             "contact": input("Contact: "), "email": input("Email: ")}
        with open("main.json", "w") as f:
            json.dump(data, f)
        print("\nAdding successfully!")
        menu()


def json_create():
    record = {"student": {}}
    with open("main.json", "w") as f:
        json.dump(record, f)
    menu()


def List():
    print("List(s)")
    print("\n--------------------------------")
    with open("main.json") as note:
        data = json.load(note)
        for i in range(len(data["student"])):
            print(i + 1, ".", data["student"][i]["name"])


def delete():
    with open("main.json") as a:
        data = json.load(a)
        List()
        index = int(input("Enter the number you want to delete: "))
        if index <= len(data["student"]):
            del (data["student"][index - 1])
            with open("main.json", "w") as f:
                json.dump(data, f)
            print("Delete successfully!")
            menu()
        else:
            print("Enter the number")
            delete()


print("-------------------------------")
print("Welcome to student record system")
print("-------------------------------")


def edit():
    with open("main.json") as update:
        data = json.load(update)
        List()
        inp = int(input("Enter the number you want to update: "))
        info = {"name": input("Name: "), "crs": input("Course: "), "year": input("Year: "), "major": input("Major: "),
                "contact": input("Contact: "), "email": input("Email: ")}
        data["student"][inp - 1] = info
    with open("main.json", "w") as save:
        json.dump(data, save)
        print("Update successfully!")


def menu():
    print("\n1. Add data")
    print("\n2. Data lists")
    print("\n3. Update data")
    print("\n4. Delete data")
    enter = input("Enter number you want to proceed: ")
    if enter == '1':
        add_infor()
    elif enter == '2':
        List()
    elif enter == '3':
        edit()
    elif enter == '4':
        delete()


from pathlib import Path

if Path("main.json").is_file():
    menu()
else:
    json_create()
json_create()
