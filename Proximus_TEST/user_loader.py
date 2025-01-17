import csv
from gophish.models import User

def load_users_from_csv(csv_file):
    users = []
    with open(csv_file, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            users.append(User(
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                position=row["position"]
            ))
    return users
