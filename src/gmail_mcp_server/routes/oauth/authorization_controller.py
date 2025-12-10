import google_auth_oauthlib.flow
from starlette.responses import RedirectResponse

from ...configs import configs


async def oauth_authorization_controller(request):
    """Handle Gmail OAuth authentication"""

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        configs.SECRET_FILE, scopes=configs.scopes
    )
    flow.redirect_uri = "http://localhost:8100/oauth/callback"

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        login_hint="rihards.jukna@gmail.com",
        prompt="consent",
    )

    # Store the state so the callback can verify the auth server response.
    request.session["oauth_state"] = state

    return RedirectResponse(authorization_url)
