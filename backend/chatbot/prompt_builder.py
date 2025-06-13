
def build_prompt(message: str, tone: dict, context_chunks: list) -> str:
    """
    Combines user message, tone profile, and retrieved context chunks into a prompt string.
    """
    # Join all context chunks into one readable block
    context = "\n\n".join(context_chunks)

    # Start with tone opening if available
    opening = tone.get("opening", "")
    closing = tone.get("closing", "")
    style = tone.get("style", "")

    # Final prompt structure
    prompt = f"""
You are a helpful and persuasive AI salesperson. Respond in the following tone/style: {style}

{opening}

Customer asked: "{message}"

Here’s relevant context from the store:
{context}

{closing}
    """
    return prompt.strip()
