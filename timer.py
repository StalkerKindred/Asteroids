def display(sec,mins,hours):
    basic_display = str(sec) + "s"
    if mins >= 1:
        basic_display = str(mins) + ":" + basic_display
    if hours >= 1:
        basic_display = str(hours) + ":" + str(mins) + ":" + basic_display
    return basic_display