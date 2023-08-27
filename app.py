import mysql.connector
import sys

connection = mysql.connector.connect(
    user='root', 
    password='Dabrowa2008', 
    host='127.0.0.1', 
    database='tour-de-dabrowa', 
    auth_plugin='mysql_native_password')

cursor = connection.cursor()

def main():
    print()
    print("Dostępne opcje:")
    print("1. Zawodnicy")
    print("2. Drużyny")
    print("3. Wyjdź")

    try:
        user_choice = int(input("Wybierz opcję, podając jej indeks: "))
    except:
        print("Błąd, spróbuj jeszcze raz")
        print()
        main()

    if user_choice == 1:
        main_menu_athletes()
    elif user_choice == 2:
        main_menu_teams()
    elif user_choice == 3:
        connection.close()
        sys.exit()
    else:
        print('Podano nieistniejącą opcję')
        main()
        print()

def main_menu_athletes():
        print()
        print("1. Pokaż zawodników")
        print("2. Dodaj, zawodnika")
        print("3. Usuń zawodnika")
        print("4. Edytuj zawodnika")
        print("5. Wyjdź do menu")

        try:
            user_choice2 = int(input("Wybierz opcję, podając jej indeks: "))
        except:
            print("Błąd, spróbuj jeszcze raz")
            print()
            main()
        
        if user_choice2 == 1:
            show_athletes()
        elif user_choice2 == 2:
            add_athlete()
        elif user_choice2 == 3:
            delete_athlete()
        elif user_choice2 == 4:
            edit_athlete()
        else:
            main()

def main_menu_teams():
        print()
        print("1. Pokaż drużyny ")
        print("2. Dodaj drużynę")
        print("3. Usuń drużynę")
        print("4. Wyjdź do menu")

        try:
            user_choice2 = int(input("Wybierz opcję, podając jej indeks: "))
        except:
            print("Błąd, spróbuj jeszcze raz")
            print()
            main()
        if user_choice2 == 1:
            show_teams()
        elif user_choice2 == 2:
            add_team()
        elif user_choice2 == 3:
            delete_team()
        else:
            main()


def show_athletes():
    query = "SELECT id, athlete_name, athlete_team, athlete_time FROM athletes"
    cursor.execute(query)

    print()
    for (id, athlete_name, athlete_team, athlete_time) in cursor:
        print(f'Numer zawodnika: {id} - Nazwa: {athlete_name} - Drużyna: {athlete_team} - Czas: {athlete_time}')
    print()

    main_menu_athletes()
    

def add_athlete():
    query2 = "SELECT id, teamname, number_of_athletes FROM teams;"
    cursor.execute(query2)

    print()
    for (id, teamname, number_of_athletes) in cursor:
        print(f'Numer drużyny: {id} - Nazwa drużyny: {teamname} - Liczba zawodników: {number_of_athletes}')
    print()

    insertValues = {
        'athlete_name' : str(input("Podaj nazwę (imię i nazwisko), zawodnika: ")),
        'athlete_team' : str(input("Podaj drużynę zawodnika: "))
    }

    query = "INSERT INTO athletes(athlete_name, athlete_team) VALUES(%(athlete_name)s, %(athlete_team)s);"
    query1 = "INSERT INTO teams(teamname) VALUES(%(athlete_team)s);"

    cursor.execute(query, insertValues)
    connection.commit()

    try:
        cursor.execute(query1, insertValues)
        connection.commit()
    except:
        print("Taka drużna już istnieje, nie dodano nowej")

    query2 = "UPDATE teams SET number_of_athletes = (number_of_athletes + 1) WHERE teamname=%(athlete_team)s;"

    cursor.execute(query2, insertValues)
    connection.commit()

    print("Dodano zawodnika")
    print()

    main_menu_athletes()


def delete_athlete():
    query = "DELETE FROM athletes WHERE id=%(athlete_id)s"

    insertValues = {
        'athlete_id' : str(input("Podaj numer zawodnika, którego chcesz usunąć: ")),
        'athlete_team' : 'SELECT athlete_team FROM athletes WHERE id=%(athlete_id)s'
    }

    cursor.execute(query, insertValues)
    connection.commit()

    query2 = "UPDATE teams SET number_of_athletes = (number_of_athletes - 1) WHERE teamname=%(athlete_team)s;"

    cursor.execute(query2, insertValues)

    print("Usunięto zawodnika")
    print()

    main_menu_athletes()

def edit_athlete():
    query1 = "SELECT id, athlete_name, athlete_team, athlete_time FROM athletes"
    cursor.execute(query1)

    print("Zawodnicy:")
    for (id, athlete_name, athlete_team, athlete_time) in cursor:
        print(f'Numer zawodnika: {id} - Nazwa: {athlete_name} - Drużyna: {athlete_team} - Czas: {athlete_time}')
    print()

    athlete_id = int(input("Podaj numer zawodnika, którego chcesz edytować: "))
    user_choice = str(input("Które pole chcesz edytować? "))

    if user_choice == "nazwę":
        insertValues = {
            'athlete_id' : athlete_id,
            'new_athlete_name' : str(input("Podaj nową nazwę zawodnika: "))
        }
        query = "UPDATE athletes SET athlete_name=%(new_athlete_name)s WHERE id=%(athlete_id)s"        
    elif user_choice == "nazwę drużyny":
        insertValues = {
            'athlete_id' : athlete_id,
            'new_athlete_team_name' : str(input("Podaj nową nazwę drużyny zawodnika: "))
        }
        query = "UPDATE athletes SET athlete_team=%(new_athlete_team_name)s WHERE id=%(athlete_id)s"  
    elif user_choice == "czas":
        insertValues = {
            'athlete_id' : athlete_id,
            'athlete_time' : int(input("Podaj czas zawodnika: "))
        }
        query = "UPDATE athletes SET athlete_time=%(athlete_time)s WHERE id=%(athlete_id)s"
    elif user_choice == "wszystkie":
        insertValues = {
            'athlete_id' : int(input("Podaj numer zawodnika, którego chcesz edytować: ")),
            'new_athlete_name' : str(input("Podaj nową nazwę tego zawodnika: ")),
            'new_team' : str(input("Podaj nową nazwę drużny tego zawodnika: "))
        }
        query = "UPDATE athletes SET athlete_name=%(new_athlete_name)s, athlete_team=%(new_team)s WHERE id=%(athlete_id)s"
    else:
        print("Błąd, spróbuj jeszcze raz")
        edit_athlete()

    cursor.execute(query, insertValues)
    connection.commit()
    print("Pomyślnie zedytowano")
    main_menu_athletes()

def show_teams():
    query = "SELECT id, teamname, number_of_athletes FROM teams"
    cursor.execute(query)

    print()
    print("Drużyny:")
    for (id, teamname, number_of_athletes) in cursor:
        print(f'Numer drużyny: {id} - Nazwa drużyny: {teamname} - Liczba zawodników: {number_of_athletes}')
    print()

    main_menu_teams()

def add_team():
    query = "INSERT INTO teams(teamname, number_of_athletes) VALUES(%(teamname)s, %(number_of_athletes)s)"

    insertValues = {
    'teamname' : str(input("Podaj nazwę drużyny, którą chcesz dodać: ")),
    'number_of_athletes' : int(input("Podaj nliczbę zawodnikó, należacych do drużyny: "))
    }

    cursor.execute(query, insertValues)
    connection.commit()
    print("Dodano drużynę")
    print()

    main_menu_teams()


def delete_team():
    query = "DELETE FROM teams WHERE id=%(team_id)s"

    insertValues = {
        'team_id' : str(input("Podaj numer drużyny, którą chcesz usunąć: ")),
    }

    cursor.execute(query, insertValues)
    connection.commit()
    print("Usunięto drużynę")
    print()

    main_menu_teams()    

main()