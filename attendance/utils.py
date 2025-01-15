from nltk.metrics import edit_distance


def fn_nltk(alisher, marketing):
    """
    Сравнивает строки по метрике редактирования.
    """
    alisher = str(alisher).strip().lower()
    marketing = str(marketing).strip().lower()
    max_length = max(len(alisher), len(marketing))
    if max_length == 0:
        return 0
    distance = edit_distance(alisher, marketing)
    similarity_percentage = ((max_length - distance) / max_length) * 100
    return similarity_percentage


def calculate_similarity(employee, attended_list):
    for attendee in attended_list:
        similarity = fn_nltk(employee, attendee)

        if 70 <= similarity <= 75:
            # print(f"Comparing '{employee}' with '{attendee}' -> Similarity: {similarity}%")
            pass
        if similarity > 75:  # Порог для совпадения имен
            # print(f"Comparing '{employee}' with '{attendee}' -> Similarity: {similarity}%")  # Отладка
            return True
    return False
