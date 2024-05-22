import json


def render_segment_id(
        log_segment_name: str, id_name_comparison: str) -> str | None:
    """
    Get the segment id by segment name

    Args:
        - log_segment_name (str): The segment name
        - id_name_comparison (str): The id_name_comparison json string

    Returns:
        - str: The segment id | None
    """
    
    id_name_comparison_dict: dict = json.loads(id_name_comparison)    # dict

    for id, time_range in id_name_comparison_dict.items():
        if time_range == log_segment_name:
            return id
    return None
