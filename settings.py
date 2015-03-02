from os import path

# tornado specific
app_settings = dict(
    port = 6488,
    db_name = "",
    db_uri  = "",
    db_user = "",
    db_pass = "",
    login_url="/auth/login",
    static_path = path.join(path.dirname(__file__), "app/static"),
    template_path = path.join(path.dirname(__file__), "app/templates"),
    cookie_secret = "SOMETHING HERE",
    debug = False,
    debug_pdb = False,
)

from local_settings import local_settings
app_settings.update(local_settings)

