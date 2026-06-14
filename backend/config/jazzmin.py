# config/jazzmin.py

# =========================
# JAZZMIN SETTINGS
# =========================

JAZZMIN_SETTINGS = {

    # -------------------------
    # BRANDING
    # -------------------------
    "site_title": "HMS Admin",
    "site_header": "Hospital Management",
    "site_brand": "HMS",
    "welcome_sign": "Welcome to Hospital Admin Panel",
    "copyright": "HMS",

    # -------------------------
    # LOGO
    # -------------------------
    "site_logo": None,
    "login_logo": None,
    "site_logo_classes": "img-circle",

    # -------------------------
    # UI BEHAVIOR
    # -------------------------
    "show_sidebar": True,
    "navigation_expanded": True,
    "related_modal_active": True,

    # IMPORTANT (fix user dropdown issues)
    "show_ui_builder": False,

    # -------------------------
    # TOP MENU
    # -------------------------
    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"name": "Website", "url": "/", "new_window": True},
    ],

    # -------------------------
    # USER MENU (IMPORTANT)
    # -------------------------
    # Keep empty → Django/Jazzmin will auto-add:
    # Profile / Change Password / Logout
    "usermenu_links": [],

    # -------------------------
    # SIDEBAR CONTROL
    # -------------------------
    "hide_apps": [],
    "hide_models": [],

    "order_with_respect_to": [
        "auth",
        "auth.user",
        "auth.Group",
    ],

    # -------------------------
    # ICONS
    # -------------------------
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        "doctor.Doctor": "fas fa-user-md",
        "patient.Patient": "fas fa-procedures",
    },

    # -------------------------
    # CHANGEFORM STYLE
    # -------------------------
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {

    # ---------------------------------------------------
    # Theme
    # ---------------------------------------------------
    "theme": "cerulean",

    # Available themes:
    # cerulean
    # cosmo
    # cyborg
    # darkly
    # flatly
    # journal
    # litera
    # lumen
    # lux
    # materia
    # minty
    # pulse
    # sandstone
    # simplex
    # sketchy
    # slate
    # solar
    # spacelab
    # superhero
    # united
    # yeti
 
  # Navbar
    "navbar": "navbar-dark bg-primary",
    "navbar_fixed": True,

    # Sidebar
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_child_indent": True,

    # Layout
    "body_small_text": False,
    "sidebar_nav_small_text": False,

    # Accent
    "accent": "accent-primary",

    # Footer
    "footer_small_text": False,

    # Dark mode
    "default_theme_mode": "auto",
}