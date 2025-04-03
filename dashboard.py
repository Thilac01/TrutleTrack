import flet as ft
import flet.map as map
import random  # Import random module
from value import*  # Assuming you have the read_sensor_data function here

def handle_tap(e):
    print(f"Tapped at {e.data}")

def show_dashboard(page: ft.Page):
    page.clean()
    page.window.width = 440
    page.window.height = 800
    page.title = "TurtleTrack"
    
    sidebar_expanded = False  # Track sidebar state
    main_column = ft.Column()

    def toggle_sidebar(e):
        nonlocal sidebar_expanded
        sidebar_expanded = not sidebar_expanded
        sidebar_container.visible = sidebar_expanded
        page.update()
    
    def navigate_to(page_name):
        def handler(e):
            page.clean()
            page.add(ft.Text(f"Welcome to {page_name}", size=24))
            page.update()
        return handler
    
    map_component = map.Map(
        expand=True,
        initial_center=map.MapLatitudeLongitude(9.823495916688582, 80.2350961902894),
        initial_zoom=15,
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
            map.CircleLayer(
                circles=[map.CircleMarker(
                            radius=5,
                            coordinates=map.MapLatitudeLongitude(9.823495916688582, 80.2350961902894),
                            color=ft.Colors.RED,
                            border_color=ft.Colors.BLUE,
                            border_stroke_width=4,
                        )],
            ),
            map.RichAttribution(
                attributions=[map.TextSourceAttribution(
                    text="OpenStreetMap Contributors",
                    on_click=lambda e: e.page.launch_url("https://openstreetmap.org/copyright"),
                ),
                map.TextSourceAttribution(
                    text="Flet",
                    on_click=lambda e: e.page.launch_url("https://flet.dev"),
                )],
            ),
            map.SimpleAttribution(
                text="Flet",
                alignment=ft.alignment.top_right,
                on_click=lambda e: print("Clicked SimpleAttribution"),
            ),
        ],
    )

    sidebar_container = ft.Container(
        content=ft.Column([ 
            ft.Container(content=ft.Row([ft.Icon(ft.icons.PERSON, color=ft.colors.BLACK), ft.Text("Account", weight="bold", size=16, color=ft.colors.BLACK)]), on_click=navigate_to("Account"), padding=5),
            ft.Container(content=ft.Row([ft.Icon(ft.icons.BAR_CHART, color=ft.colors.BLACK), ft.Text("Statistic", weight="bold", size=16, color=ft.colors.BLACK)]), on_click=navigate_to("Statistic"), padding=5),
            ft.Container(content=ft.Row([ft.Icon(ft.icons.SETTINGS, color=ft.colors.BLACK), ft.Text("Settings", weight="bold", size=16, color=ft.colors.BLACK)]), on_click=navigate_to("Settings"), padding=5),
            ft.Container(content=ft.Row([ft.Icon(ft.icons.EXIT_TO_APP, color=ft.colors.BLACK), ft.Text("Logout", weight="bold", size=16, color=ft.colors.BLACK)]), on_click=navigate_to("Logout"), padding=5),
        ], spacing=10),
        width=150,
        height=200,
        border=ft.border.all(1, ft.colors.BLACK),
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        padding=10,
        visible=False,  # Initially hidden
    )

    top_row = ft.Row([ft.IconButton(icon=ft.icons.MENU, tooltip="Menu", icon_color=ft.colors.BLACK, on_click=toggle_sidebar), ft.Container(expand=True), ft.IconButton(icon=ft.icons.MESSAGE_ROUNDED, tooltip="Contact", icon_color=ft.colors.BLACK)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    main_column.controls.extend([top_row])
    main_column.controls.extend([ft.Text("Map", size=20, weight="bold", color=ft.colors.BLACK),
                                ft.Container(content=map_component, margin=10, padding=10, alignment=ft.alignment.center, bgcolor=ft.colors.WHITE60, width=400, height=200, border=ft.border.all(1, ft.colors.BLACK), border_radius=30)])

    # Function to generate random number
    def random_number():
        return random.randint(1, 100)  # Generates a random number between 1 and 100

    # 2x2 grid layout under the map
    grid_row_1 = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text(str(random_number()) + "m/s", weight="bold", size=40, color=ft.colors.BLACK),
                ft.Row([ft.Icon(ft.icons.SPEED_ROUNDED, color=ft.colors.BLACK), ft.Text("Air Speed", weight="bold", size=16, color=ft.colors.BLACK)]),
            ]),
            margin=5,
            padding=10,
            bgcolor=ft.colors.WHITE,
            width=180,
            height=150,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=10
        ),
        ft.Container(
            content=ft.Column([
                ft.Text(str(random_number()) + "s", weight="bold", size=40, color=ft.colors.BLACK),
                ft.Row([ft.Icon(ft.icons.AV_TIMER, color=ft.colors.BLACK), ft.Text("Time of Flight", weight="bold", size=16, color=ft.colors.BLACK)]),
            ]),
            margin=5,
            padding=10,
            bgcolor=ft.colors.WHITE,
            width=180,
            height=150,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=10
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Dynamic data section (Wind Speed) for grid_row_2
    wind_speed_text = ft.Text(str(read_sensor_data()) + "m/s", weight="bold", size=40, color=ft.colors.BLACK)

    def update_wind_speed(e):
        wind_speed_text.value = str(read_sensor_data()) + "m/s"
        wind_speed_text.update()

    grid_row_2 = ft.Row([
        ft.Container(
            content=ft.Column([
                wind_speed_text,
                ft.Row([ft.Icon(ft.icons.WIND_POWER, color=ft.colors.BLACK), ft.Text("Wind Speed", weight="bold", size=16, color=ft.colors.BLACK)]),
            ]),
            margin=5,
            padding=10,
            bgcolor=ft.colors.WHITE,
            width=180,
            height=150,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=10
        ),
        ft.Container(
            content=ft.Column([
                ft.Text(str(random_number()) + "%", weight="bold", size=40, color=ft.colors.BLACK),
                ft.Row([ft.Icon(ft.icons.BATTERY_6_BAR_OUTLINED, color=ft.colors.BLACK), ft.Text("Battery Level", weight="bold", size=16, color=ft.colors.BLACK)]),
            ]),
            margin=5,
            padding=10,
            bgcolor=ft.colors.WHITE,
            width=180,
            height=150,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=10
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    grid_row_3 = ft.Container(content=ft.Row([ft.Text("Yaw", weight="bold", size=16, color=ft.colors.BLACK), ft.Text("40 ", weight="bold", size=16, color=ft.colors.BLACK), ft.Text("Pitch", weight="bold", size=16, color=ft.colors.BLACK), ft.Text("6 ", weight="bold", size=16, color=ft.colors.BLACK), ft.Text("Roll", weight="bold", size=16, color=ft.colors.BLACK), ft.Text("9 ", weight="bold", size=16, color=ft.colors.BLACK), ft.Text("Altitude", weight="bold", size=16, color=ft.colors.BLACK), ft.Text("13000ft ", weight="bold", size=16, color=ft.colors.BLACK)]), margin=1, padding=5, bgcolor=ft.colors.WHITE, width=400, height=70, border=ft.border.all(1, ft.colors.BLACK), border_radius=10)

    # Add the 2x2 grid under the map
    main_column.controls.extend([grid_row_1, grid_row_2, grid_row_3])

    main_container = ft.Container(
        content=ft.Stack([main_column, sidebar_container]),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE,
        width=400,
        height=750,
        border_radius=20,
        on_click=lambda e: toggle_sidebar(e) if sidebar_expanded else None,  # Close sidebar when clicking outside
    )

    # Set a timer to update the wind speed every second (or adjust interval as needed)
    page.add(main_container)
    page.add(ft.Timer(interval=1000, on_tick=update_wind_speed))  # Update every second

    page.update()

# Uncomment to run the app
# ft.app(target=show_dashboard)
