import flet as ft
import mysql.connector

connection = mysql.connector.connect(
    user='root', 
    password='Dabrowa2008', 
    host='127.0.0.1', 
    database='tour-de-dabrowa', 
    auth_plugin='mysql_native_password')

cursor = connection.cursor()

def main(page: ft.Page):
    def close_banner(e):
            page.banner.open = False
            page.update()


    def print_athletes():        
        query = "SELECT id, athlete_name, athlete_team, athlete_time FROM athletes"
        cursor.execute(query)

        page.add(ft.Text("Zawodnicy"))
        for (id, athlete_name, athlete_team, athlete_time) in cursor:
            page.add(ft.Text(f"Numer zawodnika: {id} - Nazwa: {athlete_name} - Drużyna: {athlete_team} - Czas: {athlete_time}")) 


    def add_team_to_dropdown():  
        global dropdown_team

        dropdown_team = ft.Dropdown(label="Nazwa drużyny",
            hint_text="Podaj drużynę zawodnika, którego chcesz usunąć")
        
        query = "SELECT teamname FROM teams"
        cursor.execute(query)

        for teamname in cursor:
            option = (f'{teamname}')
            teamname_cleaned = str(option).replace(",", "").replace("'", "").replace("(", "").replace(")", "")

            dropdown_team.options.append(ft.dropdown.Option(teamname_cleaned))
        
        dropdown_team.value = "Wybierz drużynę"


    def add_athlete_id_to_dropdown():
        global dropdown_athlete_id

        dropdown_athlete_id = ft.Dropdown(label="Numer zawodnika",
            hint_text="Podaj numer zawodnika, którego chcesz usunąć")

        query = "SELECT id FROM athletes"
        cursor.execute(query)

        for id in cursor:
            option = (f'{id}')
            athlete_id_cleaned = str(option).replace(",", "").replace("'", "").replace("(", "").replace(")", "")

            dropdown_athlete_id.options.append(ft.dropdown.Option(athlete_id_cleaned))
        
        dropdown_athlete_id.value = "Wybierz numer zawodnika"


    def print_teams():
        query = "SELECT id, teamname, number_of_athletes FROM teams"
        cursor.execute(query)

        page.clean()
        page.add(ft.Text("Drużyny:"))
        for (id, teamname, number_of_athletes) in cursor:
            page.add(ft.Text(f'Numer drużyny: {id} - Nazwa drużyny: {teamname} - Liczba zawodników: {number_of_athletes}'))


    def organizer_account_log_in(e):
        def log_in(e):
            global organizer_log_in_status

            if not organizer_id_field.value:
                organizer_id_field.error_text = "Wpisz id organizatora"
                page.update()
            elif not organizer_password_field.value:
                organizer_password_field.error_text = "Wpisz hasło"
                page.update()
            else:
                organizer_password_from_form = organizer_password_field.value
                organizer_id_from_form = organizer_id_field.value

                insertValues = {
                    'organizer_id' : organizer_id_from_form,
                }
                
                query = "SELECT organizer_id, organizer_password FROM organizers WHERE organizer_id=%(organizer_id)s"
                cursor.execute(query, insertValues)

                for organizer_id, organizer_password in cursor:
                    organizer_id_from_mysql = (f'{organizer_id}')
                    organizer_password_from_mysql = (f'{organizer_password}')

                try:
                    if organizer_id_from_form == organizer_id_from_mysql:
                        if organizer_password_from_form == organizer_password_from_mysql:
                            organizer_log_in_status = True
                            page.vertical_alignment = "START"
                            page.clean()
                            main_menu_for_organizer(e)
                        else:
                            organizer_password_field.error_text = "Błędne hasło"
                            page.update()
                except:
                    page.banner = ft.Banner(
                        bgcolor=ft.colors.RED_300,
                        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                        content=ft.Text(
                            "Błąd! Organizator o takim ID nie istnieje! Spróbuj jeszcze raz"
                        ),
                        actions=[
                            ft.TextButton("OK", on_click=close_banner),
                        ],
                    )

                    page.banner.open = True
                    page.vertical_alignment = "START"
                    organizer_account_log_in(e)
        
        global organizer_log_in_status

        if organizer_log_in_status == True:
            main_menu_for_organizer(e)
        else:
            page.vertical_alignment = "CENTER"
            page.horizontal_alignment = "CENTER"

            img = ft.Image(
                src=f"avatar.jpeg",
                width=80,
                height=80,
                border_radius=50,
                fit=ft.ImageFit.CONTAIN,
            )
            organizer_id_field = ft.TextField(label="Unikalny identyfikator organizatora", autofocus=True, width=250)
            organizer_password_field = ft.TextField(label="Hasło", width=250, password=True, can_reveal_password=True)
            
            page.clean()
            page.add(img, organizer_id_field, organizer_password_field, ft.ElevatedButton(text="Zaloguj się", on_click=log_in, width=150))


    def main_menu_for_organizer(e):
        page.clean()
        page.horizontal_alignment = "CENTER"
        page.add(ft.Text("Menu organizatorów", size=30))
        page.add(ft.ElevatedButton(text="Zawodnicy", on_click=main_menu_athletes, icon="DIRECTIONS_BIKE_ROUNDED", bgcolor={ft.MaterialState.HOVERED: ft.colors.LIGHT_BLUE_100}, width=250))
        page.add(ft.ElevatedButton(text="Drużyny", on_click=main_menu_teams, icon="PEOPLE", bgcolor={ft.MaterialState.HOVERED: ft.colors.LIGHT_BLUE_100}, width=250))


    def main_menu_athletes(e):
            page.clean()
            page.add(ft.Text("Wybierz opcję"))
            page.add(ft.ElevatedButton(text="Pokaż zawodników", on_click=show_athletes, icon="REMOVE_RED_EYE_ROUNDED", width=250))
            page.add(ft.ElevatedButton(text="Dodaj zawodnika", on_click=add_athlete, icon="ADD", width=250))
            page.add(ft.ElevatedButton(text="Usuń zawodnika", on_click=delete_athlete, icon="DELETE", width=250))
            page.add(ft.ElevatedButton(text="Edytuj zawodnika", on_click=edit_athlete, icon="EDIT", width=250))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_for_organizer, icon="EXIT_TO_APP", width=250))


    def main_menu_teams(e):
            page.clean()
            page.add(ft.Text("Wybierz opcję"))
            page.add(ft.ElevatedButton(text="Pokaż drużyny", on_click=show_teams, icon="REMOVE_RED_EYE_ROUNDED", width=250))
            page.add(ft.ElevatedButton(text="Dodaj drużynę", on_click=add_team, icon="ADD", width=250))
            page.add(ft.ElevatedButton(text="Usuń drużynę", on_click=delete_team, icon="DELETE", width=250))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_for_organizer, icon="EXIT_TO_APP", width=250))


    def show_athletes(e):
        page.clean()
        print_athletes()
        page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))


    def add_athlete(e):
        def confirm(e):
            if not athlete_name_field.value:
                athlete_name_field.error_text = "Wpisz nazwę zawodnika"
            else:
                if dropdown.value == "Dodaj nową drużynę":
                    page.add(athlete_team_field)
                    if not athlete_team_field.value:
                        athlete_team_field.error_text = "Wpisz nazwę drużyny"
                    else:
                        insertValues = {
                            'athlete_name' : athlete_name_field.value,
                            'athlete_team' : athlete_team_field.value
                        }

                        query1 = "INSERT INTO athletes(athlete_name, athlete_team) VALUES(%(athlete_name)s, %(athlete_team)s);"
                        query2 = "INSERT INTO teams(teamname, number_of_athletes) VALUES(%(athlete_team)s, 0)"

                        cursor.execute(query1, insertValues)
                        connection.commit()

                        try:
                            cursor.execute(query2, insertValues)
                        except:
                            pass

                        query4 = "UPDATE teams SET number_of_athletes = (number_of_athletes + 1) WHERE teamname=%(athlete_team)s;"
                        cursor.execute(query4, insertValues)
                        connection.commit()

                        page.banner = ft.Banner(
                            bgcolor=ft.colors.GREEN_300,
                            leading=ft.Icon(ft.icons.ADD_TASK_ROUNDED, color=ft.colors.GREEN, size=40),
                            content=ft.Text(
                                "Pomyślnie dodano nowego zawodnika"
                            ),
                            actions=[
                                ft.TextButton("OK", on_click=close_banner),
                            ],
                        )

                        page.banner.open = True
                        page.update()
                        page.clean()
                        print_athletes()
                        page.add(ft.ElevatedButton(text="Dodaj nowego zawodnika", on_click=add_athlete))
                        page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))

                else:
                    insertValues = {
                        'athlete_name' : athlete_name_field.value,
                        'athlete_team' : dropdown.value
                    }

                    query1 = "INSERT INTO athletes(athlete_name, athlete_team) VALUES(%(athlete_name)s, %(athlete_team)s);"
                    query2 = "INSERT INTO teams(teamname, number_of_athletes) VALUES(%(athlete_team)s, 0)"

                    cursor.execute(query1, insertValues)
                    connection.commit()

                    try:
                        cursor.execute(query2, insertValues)
                    except:
                        pass

                    query4 = "UPDATE teams SET number_of_athletes = (number_of_athletes + 1) WHERE teamname=%(athlete_team)s;"
                    cursor.execute(query4, insertValues)
                    connection.commit()

                    page.banner = ft.Banner(
                        bgcolor=ft.colors.GREEN_300,
                        leading=ft.Icon(ft.icons.ADD_TASK_ROUNDED, color=ft.colors.GREEN, size=40),
                        content=ft.Text(
                            "Pomyślnie dodano nowego zawodnika"
                        ),
                        actions=[
                            ft.TextButton("OK", on_click=close_banner),
                        ],
                    )

                    page.banner.open = True
                    page.update()
                    page.clean()
                    print_athletes()
                    page.add(ft.ElevatedButton(text="Dodaj nowego zawodnika", on_click=add_athlete))
                    page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))


        athlete_name_field = ft.TextField(label="Podaj nazwę (imię i nazwisko), zawodnika: ", autofocus=True)
        athlete_team_field = ft.TextField(label="Podaj drużynę zawodnika: ")
        dropdown = ft.Dropdown()

        query1 = "SELECT teamname FROM teams"
        cursor.execute(query1)

        for teamname in cursor:
            option = (f'{teamname}')
            teamname_cleaned = str(option).replace(",", "").replace("'", "").replace("(", "").replace(")", "")

            dropdown.options.append(ft.dropdown.Option(teamname_cleaned))
        
        dropdown.options.append(ft.dropdown.Option(f"Dodaj nową drużynę"))
        dropdown.value = "Wybierz drużynę"

        page.horizontal_alignment = "CENTER"
        page.clean()
        print_athletes()
        page.add(athlete_name_field, dropdown)
        page.add(ft.ElevatedButton(text="Dodaj zawodnika", on_click=confirm))
        page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))


    def delete_athlete(e):
        def confirm(e):
            insertValues = {
                'athlete_id' : dropdown_athlete_id.value,
                'athlete_team' : dropdown_team.value
            }

            query = "DELETE FROM athletes WHERE id=%(athlete_id)s"
            cursor.execute(query, insertValues)

            try:
                query2 = "UPDATE teams SET number_of_athletes = (number_of_athletes - 1) WHERE teamname=%(athlete_team)s"
                cursor.execute(query2, insertValues)
                page.banner = ft.Banner(
                        bgcolor=ft.colors.GREEN_300,
                        leading=ft.Icon(ft.icons.DELETE, color=ft.colors.GREEN, size=40),
                        content=ft.Text(
                            "Usunięto zawodnika"
                        ),
                        actions=[
                            ft.TextButton("OK", on_click=close_banner),
                        ],
                    )

                page.banner.open = True
            except:
                page.banner = ft.Banner(
                        bgcolor=ft.colors.RED_300,
                        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                        content=ft.Text(
                            "Błąd! nie usunięto zawodnika"
                        ),
                        actions=[
                            ft.TextButton("OK", on_click=close_banner),
                        ],
                    )

                page.banner.open = True
                delete_athlete()
            finally:
                connection.commit()

            page.clean()
            print_athletes()
            page.add(ft.ElevatedButton(text="Usuń jeszcze jednego zawodnika", on_click=delete_athlete))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))


        add_athlete_id_to_dropdown()
        add_team_to_dropdown()

        global dropdown_athlete_id
        global dropdown_team

        page.clean()
        print_athletes()                  
        page.add(ft.Text("Którego zawodnika chcesz usunąć"))     
        page.add(dropdown_athlete_id, dropdown_team, ft.ElevatedButton(text="Usuń zawodnika", on_click=confirm))
        page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))

    
    def edit_athlete(e):
        def show_edit_athlete():
            insertValues = {
                    'athlete_id' : dropdown_athlete_id.value
            }

            query = "SELECT id, athlete_name, athlete_team, athlete_time FROM athletes WHERE id=%(athlete_id)s"
            cursor.execute(query, insertValues)

            for (id, athlete_name, athlete_team, athlete_time) in cursor:
                page.add(ft.Text(f"Numer zawodnika: {id} - Nazwa: {athlete_name} - Nazwa drużyny: {athlete_team} - Czas: {athlete_time}"))

        def accept(e):
            page.clean()
            show_edit_athlete()
            page.add(ft.Text('Wybierz opcję:'))
            page.add(ft.ElevatedButton(text="Edytuj nazwę", on_click=edit_name))
            page.add(ft.ElevatedButton(text="Edytuj przynależność do drużyny", on_click=edit_team))
            page.add(ft.ElevatedButton(text="Edytuj czas", on_click=edit_time))
            page.add(ft.ElevatedButton(text="Edytuj wszystko", on_click=edit_all))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))
        
        def edit_name(e):
            def confirm(e):
                if not new_athlete_name.value:
                    new_athlete_name.error_text = "Wpisz nową nazwę zawodnika"
                    page.update()
                else:
                    insertValues = {
                        'athlete_id' : dropdown_athlete_id.value,
                        'new_athlete_name' : new_athlete_name.value
                    }
                    query = "UPDATE athletes SET athlete_name=%(new_athlete_name)s WHERE id=%(athlete_id)s"        
                    cursor.execute(query, insertValues)
                    connection.commit()
                    page.add(ft.Text("Pomyślnie zedytowano"))

            new_athlete_name = ft.TextField(label="Podaj nową nazwę zawodnika: ", autofocus=True)

            page.clean()
            show_edit_athlete()
            page.add(ft.Text("Wybrano opcję - Edytuj nazwę"))
            page.add(new_athlete_name)
            page.add(ft.ElevatedButton(text="Edytuj nazwę", on_click=confirm))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=edit_athlete, icon="EXIT_TO_APP"))

        def edit_team(e):
            def confirm(e):
                if not new_athlete_team.value:
                    new_athlete_team.error_text = "Wpisz nazwę drużyny"
                    page.update()
                else:
                    insertValues = {
                        'athlete_id' : dropdown_athlete_id.value,
                        'new_athlete_team_name' : new_athlete_team.value
                    }
                    query = "UPDATE athletes SET athlete_team=%(new_athlete_team_name)s WHERE id=%(athlete_id)s" 
                    cursor.execute(query, insertValues)
                    connection.commit()

            new_athlete_team = ft.TextField(label="Podaj nową nazwę drużny zawodnika: ", autofocus=True)

            page.clean()
            show_edit_athlete()
            page.add(ft.Text("Wybrano opcję - Edytuj drużynę"))
            page.add(new_athlete_team)
            page.add(ft.ElevatedButton(text="Edytuj drużynę", on_click=confirm))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=edit_athlete, icon="EXIT_TO_APP"))

        def edit_time(e):
            def confirm(e):
                if not athlete_time.value:
                    athlete_time.error_text = "Wpisz czas"
                    page.update()
                else:
                    insertValues = {
                        'athlete_id' : dropdown_athlete_id.value,
                        'athlete_time' : athlete_time.value
                    }
                    query = "UPDATE athletes SET athlete_time=%(athlete_time)s WHERE id=%(athlete_id)s"
                    cursor.execute(query, insertValues)
                    connection.commit()
                    page.add(ft.Text("Pomyślnie zedytowano"))

            athlete_time = ft.TextField(label="Podaj czas zawodnika: ", autofocus=True)

            page.clean()
            show_edit_athlete()
            page.add(ft.Text("Wybrano opcję - Edytuj czas"))
            page.add(athlete_time)
            page.add(ft.ElevatedButton(text="Edytuj czas", on_click=confirm))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=edit_athlete, icon="EXIT_TO_APP"))

        def edit_all(e):
            def confirm(e):
                if not new_athlete_name.value:
                    new_athlete_name.error_text = "Wpisz nową nazwę zawodnika"
                    page.update()
                elif not new_athlete_team.value:
                    new_athlete_team.error_text = "Wpisz nową nazwę drużyny zawodnika"
                    page.update()
                elif not athlete_time.value:
                    athlete_time.error_text = "Wpisz czas zawodnika"
                    page.update()
                else:
                    insertValues = {
                        'athlete_id' : dropdown_athlete_id.value,
                        'new_athlete_name' : new_athlete_name.value,
                        'new_team' : new_athlete_team.value,
                        'athlete_time' : athlete_time.value
                    }
                    query = "UPDATE athletes SET athlete_name=%(new_athlete_name)s, athlete_team=%(new_team)s. athlete_time=%(athlete_time)s WHERE id=%(athlete_id)s"
                    cursor.execute(query, insertValues)
                    connection.commit()

            new_athlete_name = ft.TextField(label="Podaj nową nazwę zawodnika: ", autofocus=True)
            new_athlete_team = ft.TextField(label="Podaj nową nazwę drużny zawodnika: ")
            athlete_time = ft.TextField(label="Podaj czas zawodnika: ")
            add_athlete_id_to_dropdown()

            page.clean()
            show_edit_athlete()
            page.add(ft.Text("Wybrano opcję - Edytuj wszystkie wartości"))
            page.add(new_athlete_name, new_athlete_team, athlete_time)
            page.add(ft.ElevatedButton(text="Edytuj wszystkie wartości", on_click=confirm))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=edit_athlete, icon="EXIT_TO_APP"))

        global dropdown_athlete_id
        add_athlete_id_to_dropdown()

        page.clean()
        print_athletes()
        page.add(dropdown_athlete_id, ft.ElevatedButton(text="Dalej", on_click=accept))
        page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))


    def show_teams(e):
        print_teams()
        page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_teams, icon="EXIT_TO_APP"))
    

    def add_team(e):
        def confirm(e):
            if not team_name_field.value:
                team_name_field.error_text = "Wpisz nazwę drużyny"
                page.update()
            else:
                insertValues = {
                    'team_name' : team_name_field.value
                }

                query1 = "INSERT INTO teams(teamname, number_of_athletes) VALUES(%(team_name)s, 0)"

                cursor.execute(query1, insertValues)
                connection.commit()

                page.banner = ft.Banner(
                        bgcolor=ft.colors.GREEN_300,
                        leading=ft.Icon(ft.icons.ADD_TASK_ROUNDED, color=ft.colors.GREEN, size=40),
                        content=ft.Text(
                            "Pomyślnie dodano nową drużynę"
                        ),
                        actions=[
                            ft.TextButton("OK", on_click=close_banner),
                        ],
                    )

                page.banner.open = True
                page.clean()
                print_teams()
                page.add(ft.ElevatedButton(text="Dodaj nową drużynę", on_click=add_team))
                page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))


        team_name_field = ft.TextField(label="Podaj nazwę drużyny: ", autofocus=True)

        page.clean()
        print_teams()
        page.add(ft.Text("Dodaj nową drużynę"))
        page.add(team_name_field) 
        page.add(ft.ElevatedButton(text="Dodaj drużynę", on_click=confirm))
        page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_teams, icon="EXIT_TO_APP"))
    

    def delete_team(e):
        def confirm(e):
            insertValues = {
                'team_id' : dropdown_delete_team_id.value
            }
            query = "DELETE FROM teams WHERE id=%(team_id)s"
            cursor.execute(query, insertValues)
            connection.commit()

            page.banner = ft.Banner(
                        bgcolor=ft.colors.GREEN_300,
                        leading=ft.Icon(ft.icons.DELETE, color=ft.colors.GREEN, size=40),
                        content=ft.Text(
                            "Usunięto drużynę"
                        ),
                        actions=[
                            ft.TextButton("OK", on_click=close_banner),
                        ],
                )

            page.banner.open = True
            page.clean()
            print_teams()
            page.add(ft.ElevatedButton(text="Usuń jeszcze jedną drużynę", on_click=delete_team))
            page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_athletes, icon="EXIT_TO_APP"))
            

        dropdown_delete_team_id = ft.Dropdown(label="Numer drużyny",
            hint_text="Podaj numer drużyny, którą chcesz usunąć")
        
        query = "SELECT id FROM teams"
        cursor.execute(query)

        for id in cursor:
            option = (f'{id}')
            teamname_cleaned = str(option).replace(",", "").replace("'", "").replace("(", "").replace(")", "")

            dropdown_delete_team_id.options.append(ft.dropdown.Option(teamname_cleaned))
        
        dropdown_delete_team_id.value = "Wybierz drużynę"

        page.clean()
        print_teams()         
        page.add(ft.Text("Którą drużynę chcesz usunąć"))   
        page.add(dropdown_delete_team_id, ft.ElevatedButton(text="Usuń drużynę", on_click=confirm))
        page.add(ft.ElevatedButton(text="Wyjdź", on_click=main_menu_teams, icon="EXIT_TO_APP"))

    global organizer_log_in_status

    organizer_log_in_status = False
    
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.DIRECTIONS_BIKE_ROUNDED),
        leading_width=40,
        title=ft.Text("Zawody rowerowe - Tour De Dąbrowa 2023 - strefa dla organizatorów", size=20, weight=ft.FontWeight.W_500),
        center_title=False,
        bgcolor=ft.colors.ORANGE_300,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.PopupMenuButton(
                icon="PERSON_OUTLINED",
                items=[
                    ft.PopupMenuItem(text="Zaloguj się", on_click=organizer_account_log_in),
                ]
            ),
        ],
    )

    page.horizontal_alignment="CENTER"
    page.add(ft.Text("Witaj w strefie dla organizatorów, aby dalej korzystać z aplikacji, musisz się zalogować"))
    page.add(ft.ElevatedButton(text="Zaloguj się", on_click=organizer_account_log_in))
    

ft.app(target=main)  