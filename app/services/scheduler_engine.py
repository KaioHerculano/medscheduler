from datetime import datetime, timedelta, timezone
from typing import Optional


class SchedulerEngine:
    @staticmethod
    def _to_utc(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @staticmethod
    def calculate_next_alarm_time(
        last_medication_time: datetime,
        min_interval_hours: int,
        last_group_time: Optional[datetime] = None,
        spacing_hours: int = 2,
    ) -> datetime:
        last_med = SchedulerEngine._to_utc(last_medication_time)
        next_by_medication = last_med + timedelta(hours=min_interval_hours)
        if last_group_time:
            last_group = SchedulerEngine._to_utc(last_group_time)
            next_by_group = last_group + timedelta(hours=spacing_hours)
            return max(next_by_medication, next_by_group)
        return next_by_medication

    @staticmethod
    def is_delayed_confirmation(
        scheduled_at: datetime,
        taken_at: datetime,
        delay_threshold_minutes: int = 30,
    ) -> bool:
        sched = SchedulerEngine._to_utc(scheduled_at)
        taken = SchedulerEngine._to_utc(taken_at)
        return (taken - sched) > timedelta(minutes=delay_threshold_minutes)

    @staticmethod
    def calculate_rescheduled_time(
        taken_at: datetime,
        min_interval_hours: int,
    ) -> datetime:
        taken = SchedulerEngine._to_utc(taken_at)
        return taken + timedelta(hours=min_interval_hours)

    @staticmethod
    def calculate_group_spacing_adjustment(
        reference_time: datetime,
        candidate_time: datetime,
        spacing_hours: int = 2,
    ) -> datetime:
        ref = SchedulerEngine._to_utc(reference_time)
        cand = SchedulerEngine._to_utc(candidate_time)
        required_minimum_time = ref + timedelta(hours=spacing_hours)
        if cand < required_minimum_time:
            return required_minimum_time
        return cand
