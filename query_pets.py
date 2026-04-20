import sqlite3

connection = sqlite3.connect("pets.db")
cursor = connection.cursor()

while True:
    user_input = input("Enter a person's ID number (-1 to quit): ")

    if user_input == "-1":
        print("Goodbye.")
        break

    if not user_input.isdigit():
        print("Please enter a valid number.")
        continue

    person_id = int(user_input)

    cursor.execute("SELECT * FROM person WHERE id = ?", (person_id,))
    person = cursor.fetchone()

    if person:
        first_name = person[1]
        last_name = person[2]
        age = person[3]

        print(f"{first_name} {last_name}, {age} years old")

        cursor.execute("""
        SELECT pet.name, pet.breed, pet.age, pet.dead
        FROM pet
        JOIN person_pet ON pet.id = person_pet.pet_id
        WHERE person_pet.person_id = ?
        """, (person_id,))

        pets = cursor.fetchall()

        for pet in pets:
            pet_name = pet[0]
            breed = pet[1]
            pet_age = pet[2]
            dead = pet[3]

            if dead == 1:
                status = "deceased"
            else:
                status = "alive"

            print(f"{first_name} {last_name} owned {pet_name}, a {breed}, that was {pet_age} years old and is {status}.")
    else:
        print("Error: person not found.")

connection.close()