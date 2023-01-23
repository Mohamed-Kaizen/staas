"""Supertoken initialization."""

from typing import Any

from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.framework.fastapi.fastapi_request import FastApiRequest
from supertokens_python.recipe import (
    emailverification,
    passwordless,
    session,
    thirdpartyemailpassword,
)
from supertokens_python.recipe.passwordless import ContactEmailOrPhoneConfig
from supertokens_python.recipe.session.interfaces import (
    RecipeInterface,
    SessionContainer,
)
from supertokens_python.recipe.thirdparty import (
    Apple,
    Discord,
    Facebook,
    Github,
    Google,
)

from staas.settings import settings

oauth_providers = []

if settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET:
    oauth_providers.append(
        Github(
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET,
        )
    )


if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
    oauth_providers.append(
        Google(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
        )
    )


if (
    settings.APPLE_CLIENT_ID
    and settings.APPLE_CLIENT_KEY_ID
    and settings.APPLE_CLIENT_TEAM_ID
    and settings.APPLE_CLIENT_PRIVATE_KEY
):
    oauth_providers.extend(
        (
            Apple(
                is_default=True,
                client_id=settings.APPLE_CLIENT_ID,
                client_key_id=settings.APPLE_CLIENT_KEY_ID,
                client_team_id=settings.APPLE_CLIENT_TEAM_ID,
                client_private_key=settings.APPLE_CLIENT_PRIVATE_KEY,
            ),
            # Used by IOS login.
            Apple(
                client_id=settings.APPLE_CLIENT_ID,
                client_key_id=settings.APPLE_CLIENT_KEY_ID,
                client_team_id=settings.APPLE_CLIENT_TEAM_ID,
                client_private_key=settings.APPLE_CLIENT_PRIVATE_KEY,
            ),
        )
    )
if settings.FACEBOOK_CLIENT_ID and settings.FACEBOOK_CLIENT_SECRET:
    oauth_providers.append(
        Facebook(
            client_id=settings.FACEBOOK_CLIENT_ID,
            client_secret=settings.FACEBOOK_CLIENT_SECRET,
        )
    )

if settings.DISCORD_CLIENT_ID and settings.DISCORD_CLIENT_SECRET:
    oauth_providers.append(
        Discord(
            client_id=settings.DISCORD_CLIENT_ID,
            client_secret=settings.DISCORD_CLIENT_SECRET,
        )
    )


def override_functions(original_implementation: RecipeInterface) -> RecipeInterface:
    """Override jwt functions."""
    original_implementation_create_new_session = (
        original_implementation.create_new_session
    )

    async def create_new_session(
        request: FastApiRequest,
        user_id: str,
        access_token_payload: dict[str, Any] | None,
        session_data: dict[str, Any] | None,
        user_context: dict[str, Any],
    ) -> SessionContainer:
        """Create new session."""
        if access_token_payload is None:
            access_token_payload = {}

        roles = settings.HASURA_ALLOWED_ROLES

        role = settings.HASURA_DEFAULT_ROLE

        # Your custom logic to determine the role

        access_token_payload["https://hasura.io/jwt/claims"] = {
            "x-hasura-allowed-roles": roles,
            "x-hasura-default-role": role,
            "x-hasura-user-id": user_id,
        }

        return await original_implementation_create_new_session(
            request, user_id, access_token_payload, session_data, user_context
        )

    original_implementation.create_new_session = create_new_session
    return original_implementation


def supertokens() -> None:
    """Initialize supertokens."""
    init(
        app_info=InputAppInfo(
            app_name=settings.PROJECT_NAME,
            api_domain=settings.BACKEND_URL,
            website_domain=settings.FRONTEND_URL,
            api_base_path=settings.BACKEND_BASE_PATH,
            website_base_path=settings.FRONTEND_BASE_PATH,
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.SUPER_TOKENS_URI,
        ),
        framework="fastapi",
        recipe_list=[
            emailverification.init(mode=settings.EMAIL_VERIFICATION),
            session.init(
                cookie_same_site="lax",
                jwt=session.JWTConfig(enable=True),
                override=session.InputOverrideConfig(functions=override_functions),
            ),
            passwordless.init(
                flow_type="USER_INPUT_CODE_AND_MAGIC_LINK",
                contact_config=ContactEmailOrPhoneConfig(),
            ),
            thirdpartyemailpassword.init(providers=oauth_providers),
        ],
        mode="wsgi",
    )
