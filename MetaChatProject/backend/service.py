import asyncio
import random

async def stream_chat_response(user_message: str, language: str = "en", voice: str = "female"):
    """
    Simulates a streaming response from an LLM.
    Replace this logic with an actual API call (e.g., OpenAI, Gemini) later.
    """
    
    # Mock responses to make it feel like an AI
    greetings = ["Hello!", "Hi there!", "Greetings!"]
    intros = ["I am MetaChat AI.", "I'm your assistant.", "How can I help you?"]
    
    # Tamil Support
    if language == "ta":
        greetings = ["வணக்கம்!", "ஹலோ!", "நல்வரவு!"]
        intros = ["நான் உங்கள் மெட்டா சாட் AI.", "நான் உங்களுக்கு உதவ தயாராக உள்ளேன்."]
    
    response_text = ""
    # Simple logic
    if "hello" in user_message.lower() or "vanakkam" in user_message.lower():
        response_text = f"{random.choice(greetings)} {random.choice(intros)} "
        if language == "ta":
            response_text += "நான் உங்களுக்கு குறியீட்டு முறை அல்லது எழுதுவதில் உதவ முடியும்."
        else:
            response_text += "I can help you with coding, writing, or just chatting."
    elif "time" in user_message.lower():
        if language == "ta":
             response_text = "என்னிடம் கடிகாரம் இல்லை, ஆனால் இது குறியீட்டு நேரம் என்று நான் நம்புகிறேன்!"
        else:
            response_text = "I don't have a watch, but I believe it's time to code!"
    else:
        if language == "ta":
            response_text = f"உங்கள் செய்தியைப் பெற்றேன்: '{user_message}'. ஒரு AI ஆக, நான் இதைச் செயலாக்கி விரிவான பதிலை அளிக்க முடியும்."
        else:
            response_text = f"I received your message: '{user_message}'. As an AI, I can process this and generate a detailed response. Voice mode: {voice}."

    # Simulate token generation delay
    tokens = response_text.split(" ")
    for token in tokens:
        yield token + " "
        await asyncio.sleep(0.05 + random.random() * 0.1)  # Random delay between 50ms and 150ms
