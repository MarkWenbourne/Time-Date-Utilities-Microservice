from __future__ import annotations

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def validate_request(endpoint: str, payload):
    if not isinstance(payload, dict):
        return False, error('Request body must be a JSON object.')

    if endpoint == 'normalize-datetime':
        required = ['dateTime', 'sourceTimezone']
        missing = [field for field in required if field not in payload]
        if missing:
            return False, error('Missing required fields.', {'missing': missing})
        if not _valid_tz(payload['sourceTimezone']):
            return False, error('Invalid sourceTimezone.', {'sourceTimezone': payload['sourceTimezone']})
        target = payload.get('targetTimezone', 'UTC')
        if not _valid_tz(target):
            return False, error('Invalid targetTimezone.', {'targetTimezone': target})
        return True, payload

    if endpoint == 'time-remaining':
        required = ['targetDateTime', 'timezone']
        missing = [field for field in required if field not in payload]
        if missing:
            return False, error('Missing required fields.', {'missing': missing})
        if not _valid_tz(payload['timezone']):
            return False, error('Invalid timezone.', {'timezone': payload['timezone']})
        return True, payload

    return False, error('Unknown endpoint validation request.')


def _valid_tz(name: str) -> bool:
    try:
        ZoneInfo(name)
        return True
    except ZoneInfoNotFoundError:
        return False


def error(message: str, details: dict | None = None):
    body = {'errorCode': 'INVALID_REQUEST', 'message': message}
    if details:
        body['details'] = details
    return body
