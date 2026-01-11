import flet as ft
import httpx
import json

API_URL = "http://127.0.0.1:8001"

class LuminaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auth_token = None
        self.user_data = None
        self.setup_page()
        self.show_login()

    def setup_page(self):
        self.page.title = "Lumina English"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.window.width = 1200
        self.page.window.height = 900
        self.page.fonts = {
            "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"
        }
        self.page.theme = ft.Theme(font_family="Outfit")

    def show_login(self):
        self.page.clean()
        
        email_field = ft.TextField(
            label="Email", 
            border_radius=15, 
            width=350,
            prefix_icon="email",
            focused_border_color="cyan400"
        )
        password_field = ft.TextField(
            label="Password", 
            password=True, 
            can_reveal_password=True, 
            border_radius=15, 
            width=350,
            prefix_icon="lock",
            focused_border_color="cyan400"
        )
        
        error_text = ft.Text(color="red400", visible=False)

        def login_click(e):
            try:
                # In a real app we'd use true auth, for demo we auto-login if fields aren't empty
                if not email_field.value or not password_field.value:
                    error_text.value = "Please fill in all fields"
                    error_text.visible = True
                    self.page.update()
                    return

                # Perform actual login
                response = httpx.post(
                    f"{API_URL}/auth/login", 
                    data={"username": email_field.value, "password": password_field.value}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.auth_token = data["access_token"]
                    self.fetch_user_and_show_dashboard()
                else:
                    error_text.value = "Invalid credentials"
                    error_text.visible = True
                    self.page.update()
            except Exception as ex:
                error_text.value = f"Connection error: {ex}"
                error_text.visible = True
                self.page.update()

        login_card = ft.Container(
            content=ft.Column([
                ft.Text("Lumina English", size=45, weight="bold", color="cyanaccent"),
                ft.Text("Your AI-Powered Path to English Mastery", size=16, color="grey400"),
                ft.Divider(height=20, color="transparent"),
                email_field,
                password_field,
                error_text,
                ft.Divider(height=10, color="transparent"),
                ft.ElevatedButton(
                    "Sign In", 
                    on_click=login_click,
                    width=350,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        bgcolor="cyan700",
                        color="white"
                    )
                ),
                ft.TextButton("Don't have an account? Create one", on_click=lambda _: None)
            ], horizontal_alignment="center", spacing=15),
            padding=50,
            border_radius=30,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
            border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE)),
            blur=ft.Blur(20, 20),
        )

        self.page.add(
            ft.Stack([
                # Background decoration
                ft.Container(
                    expand=True,
                    bgcolor="black87",
                ),
                ft.Container(
                    width=400, height=400,
                    bgcolor=ft.colors.with_opacity(0.1, "white"),
                    border_radius=200,
                    left=-100, top=-100,
                    blur=ft.Blur(100, 100)
                ),
                ft.Container(
                    width=400, height=400,
                    bgcolor=ft.colors.with_opacity(0.1, "purple"),
                    border_radius=200,
                    right=-100, bottom=-100,
                    blur=ft.Blur(100, 100)
                ),
                # Login Card
                ft.Container(
                    content=login_card,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ])
        )

    def fetch_user_and_show_dashboard(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = httpx.get(f"{API_URL}/dashboard/", headers=headers)
        if response.status_code == 200:
            self.user_data = response.json()
            self.show_main_app()

    def show_main_app(self):
        self.page.clean()
        
        # Navigation Rail
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            bgcolor=ft.colors.with_opacity(0.05, "white"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon="dashboard", label="Home"),
                ft.NavigationRailDestination(icon="menu_book", label="Lessons"),
                ft.NavigationRailDestination(icon="smart_toy", label="Assistant"),
                ft.NavigationRailDestination(icon="games", label="Games"),
                ft.NavigationRailDestination(icon="stars", label="Rewards"),
            ],
            on_change=self.handle_nav_change,
            trailing=ft.IconButton("logout", on_click=lambda _: self.show_login(), tooltip="Sign Out")
        )

        self.content_area = ft.Container(expand=True, padding=30)
        self.render_dashboard()

        self.page.add(
            ft.Row([
                self.rail,
                ft.VerticalDivider(width=1),
                self.content_area
            ], expand=True)
        )

    def handle_nav_change(self, e):
        idx = e.control.selected_index
        if idx == 0: self.render_dashboard()
        elif idx == 1: self.render_lessons()
        elif idx == 2: self.render_assistant()
        elif idx == 3: self.render_games()
        elif idx == 4: self.render_rewards()
        self.page.update()

    def render_games(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = httpx.get(f"{API_URL}/games/", headers=headers)
        games = response.json()

        game_cards = ft.Row(wrap=True, spacing=20)
        for g in games:
            game_cards.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon("videogame_asset", size=40, color="cyan400"),
                        ft.Text(g['name'], size=20, weight="bold"),
                        ft.Text(g['type'].replace('_', ' ').title(), color="grey400"),
                        ft.Divider(height=10, color="transparent"),
                        ft.ElevatedButton("Play Now", on_click=lambda _: None, 
                                         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
                    ], horizontal_alignment="center"),
                    padding=30,
                    width=250,
                    border_radius=20,
                    bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                )
            )

        self.content_area.content = ft.Column([
            ft.Text("Learn through Play", size=32, weight="bold"),
            ft.Text("Master vocabulary and grammar with mini-games", color=ft.colors.GREY_400),
            ft.Divider(height=20, color="transparent"),
            game_cards
        ], scroll=ft.ScrollMode.AUTO)

    def render_rewards(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = httpx.get(f"{API_URL}/rewards/", headers=headers)
        rewards = response.json()

        reward_cards = ft.Row(wrap=True, spacing=20)
        for r in rewards:
            reward_cards.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(r['name'], size=18, weight="bold"),
                        ft.Text(r['description'], color="grey400", size=12),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([
                            ft.Text(f"💰 {r['cost_coins']}"),
                            ft.Container(expand=True),
                            ft.ElevatedButton("Unlock", on_click=lambda _: None, 
                                             style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
                        ])
                    ]),
                    padding=20,
                    width=300,
                    border_radius=20,
                    bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                )
            )

        self.content_area.content = ft.Column([
            ft.Text("Rewards & Shop", size=32, weight="bold"),
            ft.Text("Spend your coins on skins and badges", color="grey400"),
            ft.Divider(height=20, color="transparent"),
            reward_cards
        ], scroll=ft.ScrollMode.AUTO)

    def render_dashboard(self):
        data = self.user_data
        user = data["user"]
        profile = data["profile"]
        tasks = data["tasks"]

        task_list = ft.Column(spacing=10)
        if tasks:
            for key, val in tasks["items_json"].items():
                task_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Checkbox(label=val, value=False),
                        ]),
                        padding=10,
                        border_radius=10,
                        bgcolor=ft.colors.with_opacity(0.05, "white")
                    )
                )

        self.content_area.content = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(f"Welcome back, {user['email'].split('@')[0]}!", size=32, weight="bold"),
                    ft.Text("Here's your progress for today", color="grey400"),
                ]),
                ft.Container(expand=True),
                ft.Row([
                    self.stat_card("🔥", f"{profile['streak']}", "Streak"),
                    self.stat_card("✨", f"{profile['xp']}", "XP"),
                    self.stat_card("💰", f"{profile['coins']}", "Coins"),
                ], spacing=20)
            ]),
            ft.Divider(height=40, color="transparent"),
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Daily Quests", size=24, weight="bold"),
                        ft.Text("Boost your English skills with these tasks", color="grey400"),
                        ft.Divider(height=10, color="transparent"),
                        task_list,
                    ]),
                    padding=30,
                    border_radius=20,
                    bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                    expand=2
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Companion", size=24, weight="bold"),
                        ft.Divider(height=10, color="transparent"),
                        ft.Image(src="https://img.icons8.com/color/512/anime-girl.png", width=200),
                        ft.Text(profile['character'], size=20, weight="bold", color="cyanaccent"),
                        ft.Text("Level 5 Buddy", color="grey400"),
                    ], horizontal_alignment="center"),
                    padding=30,
                    border_radius=20,
                    bgcolor=ft.colors.with_opacity(0.05, "cyan900"),
                    expand=1
                )
            ], vertical_alignment="start", spacing=30)
        ], scroll=ft.ScrollMode.AUTO)

    def stat_card(self, emoji, value, label):
        return ft.Container(
            content=ft.Column([
                ft.Text(f"{emoji} {value}", size=20, weight="bold"),
                ft.Text(label, size=12, color="grey400"),
            ], horizontal_alignment="center"),
            padding=15,
            border_radius=15,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            width=100
        )

    def render_lessons(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = httpx.get(f"{API_URL}/lessons/", headers=headers)
        lessons = response.json()

        lesson_cards = ft.Row(wrap=True, spacing=20)
        for l in lessons:
            def create_click_handler(lesson=l):
                return lambda _: self.open_lesson(lesson)

            lesson_cards.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(l['title'], size=18, weight="bold"),
                        ft.Text(f"Level {l['level']}", color="cyan400"),
                        ft.Divider(height=10, color="transparent"),
                        ft.ElevatedButton("Start Lesson", on_click=create_click_handler(), 
                                         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
                    ]),
                    padding=20,
                    width=300,
                    border_radius=15,
                    bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                )
            )

        self.content_area.content = ft.Column([
            ft.Text("English Lessons", size=32, weight="bold"),
            ft.Text("Explore structured content from A1 to C1", color="grey400"),
            ft.Divider(height=20, color="transparent"),
            lesson_cards
        ], scroll=ft.ScrollMode.AUTO)

    def open_lesson(self, lesson):
        self.content_area.content = ft.Column([
            ft.Row([
                ft.IconButton("arrow_back", on_click=lambda _: self.render_lessons()),
                ft.Text(lesson['title'], size=32, weight="bold"),
            ]),
            ft.Markdown(
                lesson['content_md'],
                selectable=True,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                expand=True
            ),
            ft.Divider(height=20),
            ft.Text("Quiz Time!", size=24, weight="bold"),
            ft.Container(
                content=ft.Column([
                    ft.Text(list(lesson['quiz_json'].values())[0] if lesson['quiz_json'] else "No quiz for this lesson."),
                    ft.TextField(label="Your Answer", border_radius=10),
                    ft.ElevatedButton("Submit Answer", bgcolor="cyan700", color="white")
                ], spacing=20),
                padding=30,
                border_radius=20,
                bgcolor=ft.colors.with_opacity(0.05, "white")
            )
        ], scroll=ft.ScrollMode.AUTO)

    def render_assistant(self):
        self.chat_history = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)
        self.chat_input = ft.TextField(
            hint_text="Ask Lumina anything...",
            expand=True,
            border_radius=15,
            on_submit=lambda e: self.send_assistant_message()
        )
        self.active_session_id = None
        self.assistant_mode = "Explain"

        def set_mode(e):
            self.assistant_mode = list(e.control.selected)[0]
            self.active_session_id = None # Reset session for new mode
            self.chat_history.controls.clear()
            self.chat_history.controls.append(self.chat_bubble(f"Mode switched to {self.assistant_mode}. How can I help?", False))
            self.page.update()

        self.content_area.content = ft.Column([
            ft.Row([
                ft.Text("AI Tutor", size=32, weight="bold"),
                ft.Container(expand=True),
                ft.SegmentedButton(
                    segments=[
                        ft.Segment(value="Explain", label=ft.Text("Explain")),
                        ft.Segment(value="Practice", label=ft.Text("Practice")),
                        ft.Segment(value="Quiz me", label=ft.Text("Quiz")),
                    ],
                    selected={self.assistant_mode},
                    on_change=set_mode
                )
            ]),
            ft.Divider(height=20, color="transparent"),
            ft.Container(
                content=self.chat_history,
                expand=True,
                padding=20,
                border_radius=20,
                bgcolor=ft.colors.with_opacity(0.02, ft.colors.WHITE)
            ),
            ft.Row([
                self.chat_input,
                ft.IconButton("send", on_click=lambda _: self.send_assistant_message(), icon_color="cyanaccent")
            ])
        ])
        
        # Initial greeting
        self.chat_history.controls.append(self.chat_bubble("Hi! I'm Lumina. I can help you with grammar, practice, or just chat in English. What's on your mind?", False))

    def send_assistant_message(self):
        if not self.chat_input.value: return
        user_text = self.chat_input.value
        self.chat_input.value = ""
        self.chat_history.controls.append(self.chat_bubble(user_text, True))
        
        # Add loading indicator
        loading_bubble = self.chat_bubble("Thinking...", False)
        self.chat_history.controls.append(loading_bubble)
        self.page.update()

        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        try:
            # Check if we have a session
            if not self.active_session_id:
                sess_resp = httpx.post(f"{API_URL}/assistant/session?mode={self.assistant_mode}", headers=headers)
                self.active_session_id = sess_resp.json()["id"]

            # Send message
            msg_resp = httpx.post(
                f"{API_URL}/assistant/message?session_id={self.active_session_id}&content={user_text}", 
                headers=headers,
                timeout=30.0
            )
            ai_text = msg_resp.json()["content"]
            
            # Replace loading with real response
            self.chat_history.controls.remove(loading_bubble)
            self.chat_history.controls.append(self.chat_bubble(ai_text, False))
        except Exception as e:
            self.chat_history.controls.remove(loading_bubble)
            self.chat_history.controls.append(self.chat_bubble(f"Error: {e}", False))
        
        self.page.update()

    def chat_bubble(self, text, is_user):
        return ft.Row([
            ft.Container(
                content=ft.Text(text, color="white"),
                padding=15,
                border_radius=15,
                bgcolor="cyan900" if is_user else "grey800",
                max_width=600,
            )
        ], alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START)

def main(page: ft.Page):
    LuminaApp(page)

if __name__ == "__main__":
    ft.app(target=main)
