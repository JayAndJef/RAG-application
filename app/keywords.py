from rake_nltk import Rake

rake = Rake()

def find_keywords(prompt: str, limit: int) -> list[str]:
    """Find keywords from a prompt using RAKE"""
    rake.extract_keywords_from_text(prompt)
    return rake.get_ranked_phrases()[:limit]