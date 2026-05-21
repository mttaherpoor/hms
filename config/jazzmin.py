# config/jazzmin.py

JAZZMIN_SETTINGS = {

    # ---------------------------------------------------
    # General
    # ---------------------------------------------------
    "site_title": "HMS Admin",
    "site_header": "HMS",
    "site_brand": "Hospital Management System",
    "site_logo": None,
    "login_logo": None,
    "welcome_sign": "Welcome to HMS Admin Panel",
    "copyright": "HMS",

    # ---------------------------------------------------
    # Top Menu
    # ---------------------------------------------------
    "topmenu_links": [

        # Home
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        # External link
        {
            "name": "GitHub",
            "url": "https://github.com",
            "new_window": True,
        },

        # App dropdown
        {"app": "auth"},
    ],

    # ---------------------------------------------------
    # User Menu
    # ---------------------------------------------------
    "usermenu_links": [
        {
            "name": "Support",
            "url": "https://github.com",
            "new_window": True,
        },
    ],

    # ---------------------------------------------------
    # Side Menu
    # ---------------------------------------------------
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    # ---------------------------------------------------
    # Order Apps / Models
    # ---------------------------------------------------
    "order_with_respect_to": [
        "auth",
        "auth.user",
        "auth.Group",
    ],

    # ---------------------------------------------------
    # Icons
    # ---------------------------------------------------
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        # Example apps
        "doctor.Doctor": "fas fa-user-md",
        "patient.Patient": "fas fa-procedures",
    },

    # ---------------------------------------------------
    # Default Icons
    # ---------------------------------------------------
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",

    # ---------------------------------------------------
    # Related Modal
    # ---------------------------------------------------
    "related_modal_active": True,

    # ---------------------------------------------------
    # Custom CSS / JS
    # ---------------------------------------------------
    "custom_css": None,
    "custom_js": None,

    # ---------------------------------------------------
    # Change Form
    # ---------------------------------------------------
    "changeform_format": "horizontal_tabs",

    # Options:
    # single
    # horizontal_tabs
    # vertical_tabs
    # collapsible
    # carousel

    "changeform_format_overrides": {
        "auth.user": "collapsible",
    },

    # ---------------------------------------------------
    # Language / Theme
    # ---------------------------------------------------
    # "language_chooser": True,
}


# -------------------------------------------------------
# UI Tweaks
# -------------------------------------------------------

JAZZMIN_UI_TWEAKS = {

    # ---------------------------------------------------
    # Theme
    # ---------------------------------------------------
    "theme": "flatly",

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

    # ---------------------------------------------------
    # Navbar
    # ---------------------------------------------------
    "navbar_small_text": False,
    "navbar_fixed": True,
    "navbar": "navbar-dark navbar-primary",

    # ---------------------------------------------------
    # Footer
    # ---------------------------------------------------
    "footer_small_text": False,

    # ---------------------------------------------------
    # Body
    # ---------------------------------------------------
    "body_small_text": False,
    "body_navbar_fixed": True,
    "body_footer_fixed": False,

    # ---------------------------------------------------
    # Sidebar
    # ---------------------------------------------------
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar": "sidebar-dark-primary",

    # ---------------------------------------------------
    # Brand
    # ---------------------------------------------------
    "brand_small_text": False,
    "brand_colour": "navbar-primary",

    # ---------------------------------------------------
    # Accent
    # ---------------------------------------------------
    "accent": "accent-primary",

    # ---------------------------------------------------
    # Buttons
    # ---------------------------------------------------
    "actions_sticky_top": False,

    # ---------------------------------------------------
    # Dark Mode
    # ---------------------------------------------------
    "default_theme_mode": "auto",
}