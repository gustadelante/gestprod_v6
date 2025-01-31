from flet import Theme

def switch_theme(page):
    page.theme_mode = Theme.DARK if page.theme_mode == Theme.LIGHT else Theme.LIGHT
    # Guardar la preferencia del usuario localmente
    with open("theme_preference.txt", "w") as f:
        f.write(page.theme_mode)
