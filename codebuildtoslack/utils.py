from datetime import timedelta


def seconds_to_text(seconds):
    delta_str = str(timedelta(seconds=seconds))[-8:]
    hours_str, minute_str, seconds_str = delta_str.split(":")

    result_buffer = []
    hours_str = hours_str.lstrip("0")
    hours = int(hours_str) if hours_str else 0
    if hours >= 1:
        hour_string = "{} hour{}".format(int(hours), "s" if hours > 1 else "")
        result_buffer.append(hour_string)

    minute_str = minute_str.lstrip("0")
    minutes = int(minute_str) if minute_str else 0
    if minutes >= 1:
        minute_string = "{} minute{}".format(minutes, "s" if minutes > 1 else "")
        result_buffer.append(minute_string)

    seconds_str = seconds_str.lstrip("0")
    seconds = int(seconds_str) if seconds_str else 0
    if seconds >= 1:
        second_string = "{} second{}".format(
            int(seconds), "s" if int(seconds) > 1 else ""
        )
        result_buffer.append(second_string)

    return ", ".join(result_buffer)
