"""
AI utilities module
Contains helper functions for AI processing
"""


def extract_content_and_tags(answer: str) -> tuple[str, list]:
    """
    Extract content and tags from AI response
    Expected format:
    article content
    TAGS:[tag1, tag2, tag3]

    Returns:
        tuple: (content, tags_list)
    """
    contents = answer.split("TAGS:")
    if len(contents) < 2:
        return answer, []

    content = contents[0].strip()
    tags = contents[1].strip()
    tags = tags.replace("[", "").replace("]", "").replace(".", "").strip()

    tags_list = []
    if tags:
        for tag in tags.split(","):
            tags_list.append(tag.strip().lower())

    return content, tags_list