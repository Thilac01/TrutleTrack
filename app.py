import flet as ft
import flet.map as map

def handle_tap(e):
    print(f"Tapped at {e.data}")

def main(page: ft.Page):
    page.window.width = 440
    page.window.height = 800
    page.title = "TurtleTrack"

    main_column = ft.Column()

    def remove_message(container, e):
        """Remove the entire message container from the main column."""
        main_column.controls.remove(container)
        page.update()

    def toggle_reply_box(reply_container, reply_input, e):
        """Show or hide the reply input box."""
        reply_container.visible = not reply_container.visible
        reply_input.value = "" 
        page.update()

    def send_reply(contact_name, reply_input, e):
        """Handle the reply action."""
        reply_text = reply_input.value
        if reply_text.strip():
            # Add the reply to the chat history
            contact_messages[contact_name].append({"sender": "You", "message": reply_text})
            update_chat(contact_name)
            reply_input.value = "" 
            page.update()

    def open_sidebar(e):
        """Opens the sidebar menu."""
        sidebar.visible = not sidebar.visible
        page.update()

    def show_contacts(e):
        """Replaces the main view with a contacts list."""
        main_column.controls.clear()
        main_column.controls.append(contacts_view())
        page.update()

    def show_main_page(e):
        """Restores the original main page view."""
        main_column.controls.clear()
        load_main_content()
        page.update()

    def update_chat(contact_name):
        """Update the chat history for the selected contact."""
        chat_column = ft.Column()

        # Add the updated chat history
        for msg in contact_messages[contact_name]:
            alignment = ft.MainAxisAlignment.START if msg["sender"] != "You" else ft.MainAxisAlignment.END
            chat_column.controls.append(
                ft.Row(
                    [
                        ft.Text(msg["sender"], weight="bold", color=ft.colors.GREY),
                        ft.Text(msg["message"]),
                    ],
                    alignment=alignment,
                )
            )

        # Add the reply input
        reply_input = ft.TextField(label="Type your message...", expand=True)
        reply_container = ft.Container(
            content=ft.Row(
                [
                    reply_input,
                    ft.IconButton(
                        icon=ft.icons.SEND,
                        tooltip="Send",
                        on_click=lambda e: send_reply(contact_name, reply_input, e),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.all(10),
        )

        chat_column.controls.append(reply_container)

        # Update the view
        main_column.controls.clear()
        main_column.controls.append(chat_column)
        page.update()

    def contacts_view():
        """Returns a list of dummy contacts."""
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(icon=ft.icons.ARROW_BACK, tooltip="Back", on_click=show_main_page),
                        ft.Text("Contacts", size=20, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.ListTile(leading=ft.Icon(ft.icons.PERSON), title=ft.Text("Daniel"), subtitle=ft.Text("Online"),
                            on_click=lambda e: show_chat("Daniel")),
                ft.ListTile(leading=ft.Icon(ft.icons.PERSON), title=ft.Text("Rashad"), subtitle=ft.Text("Offline"),
                            on_click=lambda e: show_chat("Rashad")),
                ft.ListTile(leading=ft.Icon(ft.icons.PERSON), title=ft.Text("Immaath"), subtitle=ft.Text("Busy"),
                            on_click=lambda e: show_chat("Immaath")),
                ft.ListTile(leading=ft.Icon(ft.icons.PERSON), title=ft.Text("Bhavinthan"), subtitle=ft.Text("Away"),
                            on_click=lambda e: show_chat("Bhavinthan")),
            ]
        )

    def show_chat(contact_name):
        """Shows the chat view for the selected contact."""
        main_column.controls.clear()

        # Initialize chat history for each contact (you can make this dynamic)
        if contact_name not in contact_messages:
            contact_messages[contact_name] = []

        update_chat(contact_name)

    contact_messages = {
        "Daniel": [{"sender": "Daniel", "message": "Hey, how are you?"}, {"sender": "You", "message": "I'm good, thanks!"}],
        "Rashad": [{"sender": "Rashad", "message": "Did you finish the report?"}, {"sender": "You", "message": "Almost done."}],
        "Immaath": [{"sender": "Immaath", "message": "Let's meet for lunch."}, {"sender": "You", "message": "Sure!"}],
        "Bhavinthan": [{"sender": "Bhavinthan", "message": "Can you help me with the project?"}, {"sender": "You", "message": "Of course!"}],
    }

    map_component = map.Map(
        expand=True,
        initial_center=map.MapLatitudeLongitude(15, 10),
        initial_zoom=4.2,
        interaction_configuration=map.MapInteractionConfiguration(
            flags=map.MapInteractiveFlag.ALL
        ),
        on_init=lambda e: print("Initialized Map"),
        on_tap=handle_tap,
        on_secondary_tap=handle_tap,
        on_long_press=handle_tap,
        on_event=lambda e: print(e),
        layers=[
            map.TileLayer(
                url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                on_image_error=lambda e: print("TileLayer Error"),
            ),
            map.RichAttribution(
                attributions=[
                    map.TextSourceAttribution(
                        text="OpenStreetMap Contributors",
                        on_click=lambda e: e.page.launch_url(
                            "https://openstreetmap.org/copyright"
                        ),
                    ),
                    map.TextSourceAttribution(
                        text="Flet",
                        on_click=lambda e: e.page.launch_url("https://flet.dev"),
                    ),
                ]
            ),
            map.SimpleAttribution(
                text="Flet",
                alignment=ft.alignment.top_right,
                on_click=lambda e: print("Clicked SimpleAttribution"),
            ),
        ],
    )

    def create_message_card(name, message, timestamp):
        reply_input = ft.TextField(label="Reply...", expand=True)
        reply_container = ft.Container(
            content=ft.Row(
                [
                    reply_input,
                    ft.IconButton(
                        icon=ft.icons.SEND,
                        tooltip="Send",
                        on_click=lambda e: send_reply(name, reply_input, e),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            visible=False, 
            padding=ft.padding.all(10),
        )

        message_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.MESSAGE_OUTLINED),
                            title=ft.Text(name),
                            subtitle=ft.Text(message),
                        ),
                        ft.Row(
                            [
                                ft.Text(timestamp),
                                ft.Container(width=30),
                                ft.TextButton("Reply", on_click=lambda e: toggle_reply_box(reply_container, reply_input, e)),
                                ft.TextButton("Cancel", on_click=lambda e: remove_message(message_card, e)),  # Remove message on cancel
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        reply_container,  # Hidden reply box
                    ]
                ),
                width=400,
                padding=10,
            )
        )

        return message_card

    def load_main_content():
        """Loads the main content into main_column."""
        top_row = ft.Row(
            [
                ft.IconButton(icon=ft.icons.MENU, tooltip="Menu", on_click=open_sidebar),  
                ft.Container(expand=True), 
                ft.IconButton(icon=ft.Icons.MESSAGE_ROUNDED, tooltip="Contact", on_click=show_contacts), 
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        main_column.controls.extend([
            top_row,
            ft.Text("Map", size=20, weight="bold"),
            ft.Container(
                content=map_component,
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE24,
                width=400,
                height=400,
                border_radius=10,
                on_click=lambda e: print("Map Container clicked!"),
            ),
            create_message_card("Rashad", "The coral restoration is looking great.", "5 minutes ago"),
            create_message_card("Daniel", "Excited to see more turtles this season!", "2 minutes ago"),
        ])

    # Sidebar
    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.IconButton(icon=ft.icons.CLOSE, tooltip="Close Sidebar", on_click=open_sidebar),
                ft.ListTile(leading=ft.Icon(ft.icons.PERSON), title=ft.Text("Profile"), on_click=lambda e: print("Profile clicked")),
                ft.ListTile(leading=ft.Icon(ft.icons.SETTINGS), title=ft.Text("Settings"), on_click=lambda e: print("Settings clicked")),
            ]
        ),
        width=200,
        bgcolor=ft.colors.BLUE_600,
        visible=False,
        padding=10,
    )

    # Main content
    load_main_content()  # Load the initial main content

    main_container = ft.Container(
        content=main_column,
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE24,
        width=400,
        height=800,
        border_radius=10,
        on_click=lambda e: print("Main Container clicked!"),
    )

    page.add(main_container, sidebar)

ft.app(target=main)
