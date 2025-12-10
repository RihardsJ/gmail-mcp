import google.oauth2.credentials
import google_auth_oauthlib.flow
from starlette.responses import PlainTextResponse

from ...configs import configs


async def oauth_callback_controller(request):
    """Handle OAuth callback requests."""

    print("[callback] oauth_state:", request.session.get("oauth_state"))

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        configs.SECRET_FILE,
        scopes=configs.scopes,
        state=request.session.get("oauth_state"),
    )

    flow.redirect_uri = request.url_for("oauth_callback_controller")

    return PlainTextResponse("OAuth completed successfully!")
