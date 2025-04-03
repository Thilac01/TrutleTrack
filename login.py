import flet as ft
import firebase_admin
from firebase_admin import credentials, auth
from dashboard import show_dashboard  # Import the show_dashboard function from dashbord.py

# Initialize Firebase
cred = credentials.Certificate("service_account.json")
firebase_admin.initialize_app(cred)

def create_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        print("User created:", user.uid)
    except Exception as e:
        print("Error:", e)

def login_user(email, password, page):
    try:
        user = auth.get_user_by_email(email)
        print("User logged in:", user.uid)
        # If login is successful, show the dashboard
        show_dashboard(page)
    except Exception as e:
        print("Login failed:", e)

def main(page: ft.Page):
    page.window_width = 440
    page.window_height = 800
    page.title = "TurtleTrack"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(label="Password", password=True)

    def handle_login(e):
        login_user(email_field.value, password_field.value, page)  # Pass page to login_user

    def handle_signup(e):
        create_user(email_field.value, password_field.value)

    def show_login(e):
        page.clean()
        page.add(ft.Container(content=login_page, alignment=ft.alignment.center))
        page.update()
    
    def show_signup(e):
        page.clean()
        page.add(ft.Container(content=signup_page, alignment=ft.alignment.center))
        page.update()
    
    def show_forgot_password(e):
        page.clean()
        page.add(ft.Container(content=forgot_password_page, alignment=ft.alignment.center))
        page.update()
    
    # Login Page
    login_page = ft.Column(
        [
            ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
            email_field,
            password_field,
            ft.ElevatedButton("Login", on_click=handle_login),
            ft.TextButton("Sign Up", on_click=show_signup),
            ft.TextButton("Forgot Password?", on_click=show_forgot_password),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    # Signup Page
    signup_page = ft.Column(
        [
            ft.Text("Sign Up", size=30, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Name"),
            email_field,
            password_field,
            ft.ElevatedButton("Register", on_click=handle_signup),
            ft.TextButton("Back to Login", on_click=show_login),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    # Forgot Password Page
    forgot_password_page = ft.Column(
        [
            ft.Text("Forgot Password", size=30, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Enter your email"),
            ft.ElevatedButton("Reset Password", on_click=show_login),
            ft.TextButton("Back to Login", on_click=show_login),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    # Show login page initially
    show_login(None)

ft.app(target=main)
