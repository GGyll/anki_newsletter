from datetime import datetime


def get_struggle_cards(
    all_cards_info: list[dict],
    min_lapses: int = 1,
    max_factor: float | None = None,
    recent_days: int | None = None,
    prioritize_active_learning: bool = True,
    limit: int = 15,
) -> list[tuple[str, str]]:
    """
    Filters and sorts Anki cards to identify 'struggle cards'.

    Args:
        all_cards_info: A list of dictionaries, each representing Anki card info.
        min_lapses: Minimum number of lapses a card must have.
        max_factor: Maximum ease factor for a card to be considered a struggle.
        recent_days: Only include cards modified within this many days.
        prioritize_active_learning: If True, cards in learning/relearning queue are prioritized.
        limit: The maximum number of struggle cards to return.

    Returns:
        A list of tuples (Front_Value, Back_Value) for the selected struggle cards.
    """
    struggle_candidates = []
    current_timestamp_ms = int(datetime.now().timestamp() * 1000)

    for card in all_cards_info:
        # Exclude suspended/buried cards
        if card["queue"] == -1 or card["queue"] == -2:
            continue

        is_active_learning = (
            card["type"] == 1 or card["type"] == 3
        )  # 1: Learning, 3: Relearning

        # Prioritize cards actively in learning/relearning phases
        if prioritize_active_learning and is_active_learning:
            struggle_candidates.append({**card, "_priority_type": "active_learning"})
            continue

        # Existing checks for older, struggling cards
        if card["lapses"] < min_lapses:
            continue
        if max_factor is not None and card["factor"] > max_factor:
            continue
        if recent_days is not None:
            mod_time_days_ago = (current_timestamp_ms - card["mod"]) / (
                1000 * 60 * 60 * 24
            )
            if mod_time_days_ago > recent_days:
                continue

        # If it reaches here, it's an older card that still meets struggle criteria
        struggle_candidates.append({**card, "_priority_type": "older_struggle"})

    # Sort cards: Active learning first, then by recency of modification (more recent first)
    # The 'type' check in lambda is for the original type field, not _priority_type
    sorted_cards = sorted(
        struggle_candidates,
        key=lambda x: (
            x["_priority_type"] == "active_learning",  # True comes before False
            x["mod"],  # More recent (higher mod timestamp) comes first
        ),
        reverse=True,
    )[0:limit]

    return [
        (card["fields"]["Front"]["value"], card["fields"]["Back"]["value"])
        for card in sorted_cards
    ]
