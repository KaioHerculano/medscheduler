from datetime import datetime, timedelta
from typing import Optional


class SchedulerEngine:
    @staticmethod
    def calculate_next_alarm_time(
        last_medication_time: datetime,
        min_interval_hours: int,
        last_group_time: Optional[datetime] = None,
        spacing_hours: int = 2,
    ) -> datetime:
        next_by_medication = last_medication_time + timedelta(
            hours=min_interval_hours
        )
        if last_group_time:
            next_by_group = last_group_time + timedelta(hours=spacing_hours)
            return max(next_by_medication, next_by_group)
        return next_by_medication

    @staticmethod
    def is_delayed_confirmation(
        scheduled_at: datetime,
        taken_at: datetime,
        delay_threshold_minutes: int = 30,
    ) -> bool:
        return (taken_at - scheduled_at) > timedelta(
            minutes=delay_threshold_minutes
        )

    @staticmethod
    def calculate_rescheduled_time(
        taken_at: datetime,
        min_interval_hours: int,
    ) -> datetime:
        return taken_at + timedelta(hours=min_interval_hours)

    @staticmethod
    def calculate_group_spacing_adjustment(
        reference_time: datetime,
        candidate_time: datetime,
        spacing_hours: int = 2,
    ) -> datetime:
        required_minimum_time = reference_time + timedelta(hours=spacing_hours)
        if candidate_time < required_minimum_time:
            return required_minimum_time
        return candidate_time
