def get_history(model_obj):
    """
    Get latest object history
    Args:
        model_obj (obj): model history object
    Returns:
        data (list): object history
    """
    history = model_obj.history.filter(
        history_change_reason__isnull=False).order_by("-history_date")[:5]
    ACTION_MAPPER = {
        "~": "Update",
        "+": "Create"
    }
    data = []
    for item in history:
        hist = {}
        hist['time'] = item.history_date.strftime("%m/%d/%Y, %H:%M:%S")
        hist['actor'] = item.history_user.first_name + " " + \
            item.history_user.last_name + " [{}]".format(
                item.history_user.email)
        hist['message'] = str(item.history_change_reason)
        hist['action'] = ACTION_MAPPER.get(item.history_type)
        data.append(hist)
    return data
