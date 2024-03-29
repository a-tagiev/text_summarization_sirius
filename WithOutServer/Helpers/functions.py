from Bots.Summary.WithOutServer.Model.model import summarize_text


def make_summary(text_to_summary):
    out = summarize_text(text_to_summary)
    return out


def check_ai_marker(original_string):
    return "Generate by dataminds" in original_string or "[club225246870|@club225246870" in original_string


def make_perfect_answer(summary_answer, select_messages_count):
    answer = f"""Результат суммаризации {select_messages_count} сообщений:

{summary_answer}

Generate by dataminds 
    """
    return answer
