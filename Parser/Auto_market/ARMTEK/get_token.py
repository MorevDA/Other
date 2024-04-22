def get_token(ses, config) -> str:
    """Функция для получения jwgt-токена для работы с API."""
    response_result = ses.post(config.get_token_url, headers=config.headers_auth, json={})
    token_data = response_result.json()['data']['accessToken']
    authorization_token = f'Bearer {token_data}'
    return authorization_token

