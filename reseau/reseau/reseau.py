import reflex as rx

from .common.style import style


HOME_ROUTE = '/'
REGISTER_ROUTE = '/rejoindre'
LOGIN_ROUTE = '/connexion'
PROFILE_ROUTE = '/profil'
MEMBERS_ROUTE = '/membres'

DEFAULT_POSTCATEGORY = 0


google_ads_script1 = rx.script(
    src=(
        'https://www.googletagmanager.com/gtag/js?'
        'id=AW-16676736858'
    ),
)

google_ads_script2 = rx.script(
    '''
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'AW-16676736858');
    ''',
)


app = rx.App(
    head_components=[
        google_ads_script1,
        google_ads_script2
    ],
    theme=rx.theme(
        appearance='light',
        accent_color='amber',
    ),
    style=style,  # Global style configuration
    stylesheets=[  # Specific stylesheets
        '/styles.css',  # This path is relative to assets/
    ],
)
