from datetime import datetime, timedelta, timezone

from app.services.scheduler_engine import SchedulerEngine


def test_calculate_next_alarm_time_without_group() -> None:
    last_med = datetime(2026, 10, 7, 8, 0, tzinfo=timezone.utc)
    next_time = SchedulerEngine.calculate_next_alarm_time(
        last_medication_time=last_med,
        min_interval_hours=6,
    )
    expected = datetime(2026, 10, 7, 14, 0, tzinfo=timezone.utc)
    assert next_time == expected


def test_calculate_next_alarm_time_with_group_spacing() -> None:
    last_med = datetime(2026, 10, 7, 8, 0, tzinfo=timezone.utc)
    last_group = datetime(2026, 10, 7, 13, 0, tzinfo=timezone.utc)

    next_time = SchedulerEngine.calculate_next_alarm_time(
        last_medication_time=last_med,
        min_interval_hours=6,
        last_group_time=last_group,
        spacing_hours=2,
    )
    expected = datetime(2026, 10, 7, 15, 0, tzinfo=timezone.utc)
    assert next_time == expected


def test_is_delayed_confirmation() -> None:
    scheduled_at = datetime(2026, 10, 7, 8, 0, tzinfo=timezone.utc)
    on_time = scheduled_at + timedelta(minutes=25)
    delayed = scheduled_at + timedelta(minutes=35)

    assert not SchedulerEngine.is_delayed_confirmation(scheduled_at, on_time)
    assert SchedulerEngine.is_delayed_confirmation(scheduled_at, delayed)


def test_calculate_rescheduled_time() -> None:
    taken_at = datetime(2026, 10, 7, 9, 0, tzinfo=timezone.utc)
    rescheduled = SchedulerEngine.calculate_rescheduled_time(
        taken_at=taken_at,
        min_interval_hours=6,
    )
    expected = datetime(2026, 10, 7, 15, 0, tzinfo=timezone.utc)
    assert rescheduled == expected


def test_calculate_group_spacing_adjustment() -> None:
    reference_time = datetime(2026, 10, 7, 9, 0, tzinfo=timezone.utc)
    too_close = datetime(2026, 10, 7, 10, 0, tzinfo=timezone.utc)
    safe_distance = datetime(2026, 10, 7, 12, 0, tzinfo=timezone.utc)

    adjusted = SchedulerEngine.calculate_group_spacing_adjustment(
        reference_time=reference_time,
        candidate_time=too_close,
        spacing_hours=2,
    )
    expected_adjusted = datetime(2026, 10, 7, 11, 0, tzinfo=timezone.utc)
    assert adjusted == expected_adjusted

    maintained = SchedulerEngine.calculate_group_spacing_adjustment(
        reference_time=reference_time,
        candidate_time=safe_distance,
        spacing_hours=2,
    )
    assert maintained == safe_distance
