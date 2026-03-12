from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def normalize_datetime_payload(payload: dict) -> dict:
    dt = _parse_input_datetime(payload['dateTime'], payload['sourceTimezone'])
    target_tz = payload.get('targetTimezone', 'UTC')
    converted = dt.astimezone(ZoneInfo(target_tz))
    return {
        'originalInput': payload['dateTime'],
        'sourceTimezone': payload['sourceTimezone'],
        'targetTimezone': target_tz,
        'iso8601': converted.isoformat(),
        'unixTimestamp': int(converted.timestamp())
    }


def time_remaining_payload(payload: dict) -> dict:
    now = datetime.now(timezone.utc)
    target = _parse_input_datetime(payload['targetDateTime'], payload['timezone']).astimezone(timezone.utc)
    delta = target - now
    remaining_seconds = max(0, int(delta.total_seconds()))
    status = 'upcoming' if remaining_seconds > 0 else 'passed'
    return {
        'targetDateTime': target.isoformat(),
        'remainingSeconds': remaining_seconds,
        'humanReadable': _humanize_seconds(remaining_seconds),
        'status': status
    }


def _parse_input_datetime(dt_str: str, tz_name: str) -> datetime:
    # Accepts YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD HH:MM:SS
    cleaned = dt_str.replace(' ', 'T')
    dt = datetime.fromisoformat(cleaned)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(tz_name))
    return dt


def _humanize_seconds(seconds: int) -> str:
    if seconds <= 0:
        return '0 seconds remaining'
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    parts = []
    if days:
        parts.append(f'{days} day(s)')
    if hours:
        parts.append(f'{hours} hour(s)')
    if minutes:
        parts.append(f'{minutes} minute(s)')
    if secs or not parts:
        parts.append(f'{secs} second(s)')
    return ' '.join(parts) + ' remaining'
