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


    def display_informations_about_account(e):
        global user_name_from_form
        
        insertValue = {
            'user_name' : user_name_from_form
        }
        
        query = "SELECT user_name, user_email, user_password, application_status FROM users WHERE user_name=%(user_name)s"
        cursor.execute(query, insertValue)
        
        img = ft.Image(
                src=f"Aplikacja_wyscig/avatar.jpeg",
                width=80,
                height=80,
                border_radius=50,
                fit=ft.ImageFit.CONTAIN,
            )
        
        page.clean()
        page.add(img)
        for user_name, user_email, user_password, application_status in cursor:
            page.add(ft.Text("Nazwa użytkownika: " + user_name, size=17))
            page.add(ft.Text("Email: " + user_email, size=17))
            page.add(ft.Text("Hasło: " + user_password, size=17))
            try:
                page.add(ft.Text("Status wniosku: " + application_status, size=17))
            except:
                pass
            page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users))


    def display_informations_about_race(e):
        if user_log_in_status == False:
            page.clean()
            page.add(ft.Text("Ogólne informacje", size=17))
            page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users)) 
        else:
            page.clean()
            page.add(ft.Text("Szczegółowe informacje", size=17))
            page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users)) 


    def gallery(e):
        
        img1 = ft.Image(
                src=f"Aplikacja_wyscig/Images/image1.jpg",
                height=200,
            )
        
        img2 = ft.Image(
                src=f"Aplikacja_wyscig/Images/image2.jpg",
                height=200,
            )
        
        img3 = ft.Image(
                src=f"Aplikacja_wyscig/Images/image3.jpg",
                height=200,
            )
        
        img4 = ft.Image(
                src=f"Aplikacja_wyscig/Images\image4.jpg",
                width=200,
                height=200,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
            )
        
        img5 = ft.Image(
                src=f"Aplikacja_wyscig/Images/image5.jpg", 
                width=200,
                height=200,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
            )
        
        page.clean()
        page.add(img1, img2, img3, img4, img5)
        page.update()


    def user_account_log_in(e):
        def log_in(e):
            global user_log_in_status
            global user_name_from_form

            if not user_name_field.value:
                user_name_field.error_text = "Podaj nazwę użytkownika"
                page.update()
            elif not user_password_field.value:
                user_password_field.error_text = "Wpisz hasło"
                page.update()
            else:
                user_password_from_form = user_password_field.value
                user_name_from_form = user_name_field.value

                insertValues = {
                    'user_name' : user_name_from_form,
                }
                
                query = "SELECT user_name, user_password FROM users WHERE user_name=%(user_name)s"
                cursor.execute(query, insertValues)

                for user_name, user_password in cursor:
                    user_name_from_mysql = (f'{user_name}')
                    user_password_from_mysql = (f'{user_password}')
  
                try:
                    if user_name_from_form == user_name_from_mysql:
                        if user_password_from_form == user_password_from_mysql:
                            user_log_in_status = True
                            page.vertical_alignment = "START"
                            page.clean()
                            main_menu_for_users(e)
                        else:
                            user_password_field.error_text = "Błędne hasło"
                            page.update()
                except:
                    page.banner = ft.Banner(
                        bgcolor=ft.colors.RED_300,
                        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED, size=40),
                        content=ft.Text(
                            "Błąd! Użytkownik, o takiej nazwie nie istnieje! Spróbuj jeszcze raz"
                        ),
                        actions=[
                            ft.TextButton("OK", on_click=close_banner),
                        ],
                    )

                    page.banner.open = True
                    page.vertical_alignment = "START"
                    user_account_log_in(e)
        
        global user_log_in_status

        if user_log_in_status == True:
            main_menu_for_users(e)
        else:          
            page.vertical_alignment = "CENTER"
            page.horizontal_alignment = "CENTER"

            img = ft.Image(
                src=f"Aplikacja_wyscig/avatar.jpeg",
                width=80,
                height=80,
                border_radius=50,
                fit=ft.ImageFit.CONTAIN,
            )
            user_name_field = ft.TextField(label="Nazwa użykownika", autofocus=True, width=250)
            user_password_field = ft.TextField(label="Hasło", width=250, password=True, can_reveal_password=True)
            
            page.clean()
            page.add(img, user_name_field, user_password_field, ft.ElevatedButton(text="Zaloguj się", on_click=log_in, width=150), ft.Text("Nie masz konta? w każdej chwili możesz się zarejestrować", size=17), ft.ElevatedButton(text="Zarejstruj się", on_click=register_in, width=150))
    
    
    def log_out(e):
        global user_log_in_status       
        user_log_in_status = False
        
        page.banner = ft.Banner(
                        bgcolor=ft.colors.GREEN_300,
                        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.GREEN, size=40),
                        content=ft.Text(
                            "Pomyślnie wylogowano"
                        ),
                        actions=[
                            ft.TextButton("OK", on_click=close_banner),
                        ],
                    )

        page.banner.open = True
        
        page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.DIRECTIONS_BIKE_ROUNDED),
        leading_width=40,
        title=ft.Text("Zawody rowerowe - Tour De Dąbrowa 2023", size=20, weight=ft.FontWeight.W_500),
        center_title=False,
        bgcolor=ft.colors.ORANGE_300,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.PopupMenuButton(
                icon="PERSON_OUTLINED",
                items=[
                    ft.PopupMenuItem(text="Zaloguj się", on_click=user_account_log_in),
                    ft.PopupMenuItem(text="Zarejestruj się", on_click=register_in),
                ]
            ),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Dla uczestnika", on_click=main_menu_for_users), 
                        ft.PopupMenuItem(text="Informacje o wyścigu", on_click=display_informations_about_race),
                    ]
                ),
            ],
        )
        page.update()
        main_menu_for_users(e)
        
            
    def register_in(e):
        def register_in_confirm(e):
            if not user_name_field.value:
                user_name_field.error_text = "Podaj nazwę użytkownika"
                page.update()
            elif not user_email_field.value:
                user_email_field.error_text = "Podaj adre email"
                page.update()
            elif not user_password_field.value:
                user_password_field.error_text = "Podaj hasło"
                page.update()
            elif not user_password_field_confirm.value:
                user_password_field_confirm.error_text = "Podaj powtórzenie hasła"
                page.update()
            else:
                insertValues = {
                    'user_name' : user_name_field.value,
                    'user_email' : user_email_field.value,
                    'user_password' : user_password_field.value
                }
                
                if user_password_field.value == user_password_field_confirm.value:
                    try:
                        query = "INSERT INTO users(user_name, user_email, user_password)  VALUES(%(user_name)s, %(user_email)s, %(user_password)s)"
                        cursor.execute(query, insertValues)
                        connection.commit()
                        
                        page.banner = ft.Banner(
                            bgcolor=ft.colors.GREEN_300,
                            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.GREEN, size=40),
                            content=ft.Text(
                                "Pomyślnie zarejstrowano"
                            ),
                            actions=[
                                ft.TextButton("OK", on_click=close_banner),
                                ft.TextButton("Zaloguj się teraz", on_click=(user_account_log_in))
                            ],
                        )
                        page.banner.open = True
                        main_menu_for_users(e)
                        
                    except:
                        user_name_field.error_text = "Taki użytkownik istnieje w bazie danych"
                        page.update()
                else:
                    user_password_field_confirm.error_text = "Hasła nie są takie same"
                    page.update()
            
        page.vertical_alignment = "CENTER"
        page.horizontal_alignment = "CENTER"

        img = ft.Image(
            src=f"Aplikacja_wyscig/avatar.jpeg",
            width=80,
            height=80,
            border_radius=50,
            fit=ft.ImageFit.CONTAIN,
        )
        user_name_field = ft.TextField(label="Nazwa użykownika", autofocus=True, width=250)
        user_email_field = ft.TextField(label="Email", width=250)
        user_password_field = ft.TextField(label="Hasło", width=250, password=True, can_reveal_password=True)
        user_password_field_confirm = ft.TextField(label="Powtórz hasło", width=250, password=True, can_reveal_password=True)
            
        page.clean()
        page.add(img, user_name_field, user_email_field, user_password_field, user_password_field_confirm, ft.ElevatedButton(text="Zarejstruj się", on_click=register_in_confirm, width=150), ft.Text("Masz już konto?"), ft.ElevatedButton(text="Zaloguj się", on_click=user_account_log_in, width=150))
        

    def main_menu_for_users(e):
        global user_log_in_status
        
                      
        if user_log_in_status == True:
            page.appbar = ft.AppBar(
                leading=ft.Icon(ft.icons.DIRECTIONS_BIKE_ROUNDED),
                leading_width=40,
                title=ft.Text("Zawody rowerowe - Tour De Dąbrowa 2023", size=20, weight=ft.FontWeight.W_500),
                center_title=False,
                bgcolor=ft.colors.ORANGE_300,
                actions=[
                    ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                    ft.PopupMenuButton(
                        icon="PERSON_OUTLINED",
                        items=[
                            ft.PopupMenuItem(text="Wniosek", on_click=athlete_application),
                            ft.PopupMenuItem(text="Zobacz informacje, o twoim koncie", on_click=display_informations_about_account),
                            ft.PopupMenuItem(text="Wyloguj się", on_click=log_out),
                        ]
                    ),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Dla uczestnika", on_click=main_menu_for_users), 
                            ft.PopupMenuItem(text="Zobacz szczegółowe informacje o wyścigu", on_click=display_informations_about_race),
                        ]
                    ),
                ],
            )
            page.clean()
            page.add(ft.ElevatedButton(text="Złóż wniosek", on_click=athlete_application, width=250))
            page.add(ft.ElevatedButton(text="Zobacz informacje o twoim koncie", on_click=display_informations_about_account, width=400))
            page.add(ft.ElevatedButton(text="Zapytania", on_click=questions, width=250))
            page.add(ft.ElevatedButton(text="Wyloguj się", on_click=log_out, width=250))
        else:
            page.clean()
            page.add(ft.Text("Narazie, możesz zobaczyć ogólne informacje o wyścigu w sekcji - ,,Informacje, o wyścigu'', aby złożyć wniosek i otrzymać ich więcej, zaloguj się, lub załóż konto"))
            page.add(ft.ElevatedButton(text="Zaloguj się", on_click=user_account_log_in, width=250))
            page.add(ft.ElevatedButton(text="Zarejestruj się", on_click=register_in, width=250))

    
    def athlete_application(e):
        def send_application(e):
            global user_name_from_form
             
            if not athlete_name.value:
                athlete_name.error_text = "Podaj imię i nazwisko"
                page.update()
            elif not athlete_adress.value:
                athlete_adress.error_text = "Podaj adres"
                page.update()
            elif not date_of_birth.value:
                date_of_birth.error_text = "Podaj swoją datę urodzenia"
                page.update()
            else:
                try:
                    if dropdown_team.value == "Brak":
                        insertValues = {
                            'athlete_name' : athlete_name.value,
                            'athlete_adress' : athlete_adress.value,
                            'extra_informations' : extra_informations.value,
                            'date_of_birth' : date_of_birth.value,
                            'athlete_sex' : dropdown_athlete_sex.value
                        }
                        
                        query = "INSERT INTO athletes_applications(athlete_name, athlete_adress, extra_informations, age, sex, application_status) VALUES(%(athlete_name)s, %(athlete_adress)s, %(extra_informations)s, %(date_of_birth)s, %(athlete_sex)s, 'Oczekuje na weryfikację')"
                        cursor.execute(query, insertValues)
                    else:
                        insertValues = {
                            'athlete_name' : athlete_name.value,
                            'athlete_team' : dropdown_team.value,
                            'athlete_adress' : athlete_adress.value,
                            'extra_informations' : extra_informations.value,
                            'date_of_birth' : date_of_birth.value,
                            'athlete_sex' : dropdown_athlete_sex.value
                        }
                        print(dropdown_team.value)
                        query = "INSERT INTO athletes_applications(athlete_name, athlete_team, athlete_adress, extra_informations, age, sex, application_status) VALUES(%(athlete_name)s, %(athlete_team)s, %(athlete_adress)s, %(extra_informations)s, %(date_of_birth)s, %(athlete_sex)s, 'Oczekuje na weryfikację')"
                        cursor.execute(query, insertValues)
                    
                    insertValue = {
                        'user_name' : user_name_from_form
                    }
                    
                    query = "UPDATE users SET application_status='Oczekuje na weryfikacje' WHERE user_name=%(user_name)s"
                    cursor.execute(query, insertValue)
                    
                    page.banner = ft.Banner(
                            bgcolor=ft.colors.GREEN_300,
                            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.GREEN, size=40),
                            content=ft.Text(
                                "Wysłano zgłoszenie"
                            ),
                            actions=[
                                ft.TextButton("OK", on_click=close_banner),
                            ],
                        )
                    page.banner.open = True
                    connection.commit()
                    main_menu_for_users(e)                    
                except:
                    page.clean()
                    page.add("Wystąpił błąd, spróbuj jeszcze raz", athlete_application(e))
                finally:
                    connection.commit()
                    
        global user_name_from_form 
        
        insertValue = {
            'user_name' : user_name_from_form
        }
               
        query = "SELECT application_status FROM users WHERE user_name=%(user_name)s"
        cursor.execute(query, insertValue)
        
        for application_status in cursor:
            application_status = (f'{application_status}')
            application_status_cleaned = str(application_status).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
            
            if application_status_cleaned == "Oczekuje na weryfikacje":        
                page.clean()
                page.add(ft.Text("Zgłoszenie zostało już wysłane, oczekuje na weryfikację"))
                page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users))   
            elif application_status_cleaned == "Zweryfikowano":        
                page.clean()
                page.add(ft.Text("Zgłoszenie zostało już wysłane oraz zweryfikowane"))
                page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users))   
            elif application_status_cleaned == "Odrzucono":        
                page.clean()
                page.add(ft.Text("Zgłoszenie zostało już wysłane, ale zostało odrzucone"))
                page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users))   
            else:
                dropdown_athlete_sex = ft.Dropdown(
                    label="Płeć",
                    width=250,
                    options= [
                        ft.dropdown.Option("Mężczyzna"),
                        ft.dropdown.Option("Kobieta")
                    ]
                )
                
                dropdown_team = ft.Dropdown(label="Drużyna", width=250)
                
                query = "SELECT teamname FROM teams"
                cursor.execute(query)
                
                for teamname in cursor:
                    option = (f'{teamname}')
                    teamname_cleaned = str(option).replace(",", "").replace("'", "").replace("(", "").replace(")", "")

                    dropdown_team.options.append(ft.dropdown.Option(teamname_cleaned))
                    
                dropdown_team.options.append(ft.dropdown.Option("Brak"))
                
                athlete_name =  ft.TextField(label="Imię i Nazwisko", autofocus=True, width=250)
                athlete_adress = ft.TextField(label="Adres", width=250)
                date_of_birth = ft.TextField(label="Data urodzenia", width=250)
                extra_informations = ft.TextField(label="Dodatkowe informacje, które chcesz przekazać organizatorowi", width=500)
                
                page.clean()
                page.add(ft.Text("Nie wysłano zgłoszenia, możesz to zrobić teraz internetowo, lub udać się do siedziby zawodów i złożyć wniosek stacjonarnie"))
                page.add(athlete_name, dropdown_athlete_sex, athlete_adress, date_of_birth)
                page.add(ft.Text("Jeżeli twojej drużyny, nie ma na liście, to nie została ona jeszcze zgłoszona"), dropdown_team, extra_informations)
                page.add(ft.ElevatedButton(text="Wyślij zgłoszenie", on_click=send_application))
                page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users))   


    def questions(e):
        global user_name_from_form
        
        insertValue = {
                'user_name' : user_name_from_form,
            }
        
        query = "SELECT question, answer FROM questions WHERE user_name=%(user_name)s"
        cursor.execute(query, insertValue)
        
        page.clean()
        try:
            for question, answer in cursor:
                page.add(ft.Text("Zapytanie: " + question, size=17))
                page.add(ft.Text("Odpowiedź: " +  answer, size=17))
        except:
            pass
                   
        page.add(ft.ElevatedButton(text="Wyślij nowe zapytanie", on_click=send_new_question))
        page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users))  
                     
 
    def send_new_question(e):
        def confirm(e):
            if not question_field.value:
                question_field.error_text = "Wprowadź zapytanie"
            else:
                page.clean()
                page.add(ft.Text("Wyślij zapytanie"))
                
                insertValues = {
                    'user_name' : user_name_from_form,
                    'question' : question_field.value
                }
                
                query = "INSERT INTO questions(user_name, question) VALUES(%(user_name)s, %(question)s)"
                
                cursor.execute(query, insertValues)
                connection.commit()
                
                page.clean()
                questions(e)
                
        question_field = ft.TextField(label="Zapytanie", width=500)
        
        page.clean()
        page.add(ft.Text("O co chcesz zapytać?", size=17), question_field)
        page.add(ft.ElevatedButton(text="Wyślij zapytanie", on_click=confirm))
        page.add(ft.ElevatedButton(text="Powrót do menu", on_click=main_menu_for_users))     
        
                    
    global user_log_in_status
    
    page.horizontal_alignment="CENTER"
    user_log_in_status = False

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.DIRECTIONS_BIKE_ROUNDED),
        leading_width=80,
        toolbar_height=80,
        title=ft.Text("Zawody rowerowe - Tour De Dąbrowa 2023", size=20, weight=ft.FontWeight.W_500),
        center_title=False,
        bgcolor=ft.colors.ORANGE_300,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.PopupMenuButton(
                icon="PERSON_OUTLINED",
                items=[
                    ft.PopupMenuItem(text="Zaloguj się", on_click=user_account_log_in),
                    ft.PopupMenuItem(text="Zarejestruj się", on_click=register_in),
                ]
            ),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Dla uczestnika", on_click=main_menu_for_users), 
                        ft.PopupMenuItem(text="Informacje o wyścigu", on_click=display_informations_about_race),
                        ft.PopupMenuItem(text="Galeria", on_click=gallery),
                    ]
                ),
            ],
        )

    c = ft.Container( 
        content=ft.Text("The 2023 Tour de Pologne is the 80th edition of the Tour de Pologne road cycling stage race, which is part of the 2023 UCI World Tour. It will start on 29 July in Poznań and will finish on 4 August in Kraków. The 2023 Tour de Pologne is the 80th edition of the Tour de Pologne road cycling stage race, which is part of the 2023 UCI World Tour. It will start on 29 July in Poznań and will finish on 4 August in Kraków."), 
        margin=30,
        width=500,
        height=200,
    )
    
    img = ft.Image(
        src=f"Aplikacja_wyscig/Images/image4.jpg",
        height=280,
    )
        
    page.add(ft.Text("Opis wyścigu", size=30))
    page.add(c)
    page.add(ft.ElevatedButton(text="Przejdź do menu głównego", on_click=main_menu_for_users), img)
        

ft.app(target=main)  