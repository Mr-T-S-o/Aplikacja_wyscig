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

    def display_informations_about_race(e):
        page.clean()
        page.add(ft.Text("Sehr gut"))


    def user_account_log_in(e):
        def log_in(e):
            global user_log_in_status

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
                src=f"avatar.jpeg",
                width=80,
                height=80,
                border_radius=50,
                fit=ft.ImageFit.CONTAIN,
            )
            user_name_field = ft.TextField(label="Nazwa użykownika", autofocus=True, width=250)
            user_password_field = ft.TextField(label="Hasło", width=250, password=True, can_reveal_password=True)
            
            page.clean()
            page.add(img, user_name_field, user_password_field, ft.ElevatedButton(text="Zaloguj się", on_click=log_in, width=150))


    def main_menu_for_users(e):
        if user_log_in_status == True:
            page.add(ft.Text('Pomyślnie zalogowano'))
        else:
            page.clean()
            page.add(ft.Text("Narazie, możesz zobaczyć inforamcje, o wyścigu, w sekcji - ,,Informacje, o wyścigu'', aby złożyć wniosek, zaloguj się, lub załóż konto"))
            user_account_log_in(e)
            page.add(ft.ElevatedButton(text="Zarejestruj się"))


    global user_log_in_status

    user_log_in_status = False
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
                    ft.PopupMenuItem(text="Zarejestruj się"),
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

    page.horizontal_alignment="CENTER"

    c = ft.Container( 
        content=ft.Text("The 2023 Tour de Pologne is the 80th edition of the Tour de Pologne road cycling stage race, which is part of the 2023 UCI World Tour. It will start on 29 July in Poznań and will finish on 4 August in Kraków. The 2023 Tour de Pologne is the 80th edition of the Tour de Pologne road cycling stage race, which is part of the 2023 UCI World Tour. It will start on 29 July in Poznań and will finish on 4 August in Kraków."), 
        margin=30,
        width=500,
        height=200,
    )
    
    page.add(ft.Text("Opis wyścigu", size=30, font_family=""))
    page.add(c)

ft.app(target=main)  