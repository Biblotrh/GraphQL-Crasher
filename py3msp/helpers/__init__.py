from py3msp.entities import AMFResult, LoginResult, LoginStatus
from dataclasses import fields

def return_login_response(result: AMFResult) -> LoginResult:
    extract_login_status = lambda response: LoginStatus(**{key: value for key, value in response.content.get('loginStatus', {}).items() if key in {field.name for field in fields(LoginStatus)}}) if response.status_code == 200 else LoginStatus()
    return LoginResult(loginStatus=extract_login_status(result)) if result.status_code == 200 else LoginResult(loginStatus=LoginStatus())
