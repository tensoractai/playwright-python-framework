from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = "[YOUR_CLIENT_ID]"
CLIENT_SECRET = "[YOUR_CLIENT_SECRET]"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                "http://localhost"
            ]
        }
    },
    SCOPES
)

credentials = flow.run_local_server(
    port=0,
    access_type="offline",
    prompt="consent"
)

print("\nREFRESH TOKEN:")
print(credentials.refresh_token)