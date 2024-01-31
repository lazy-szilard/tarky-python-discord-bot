from random import choice


tarky_films = ["The Killers (1956)", "There Will Be No Leave Today (1959)", "The Steamroller and the Violin (1960)", "Ivan's Childhood (1962)", "Andrei Rublev (1966)", "Solaris (1972)", "Mirror (1975)", "Stalker (1979)", "Nostalghia (1983)", "Voyage in Time (1983)", "The Sacrifice (1986)"]

def get_response(user_input: str) -> str:
    """Returns a response based on the user input."""
    lowered = user_input.lower()
    
    if lowered == '':
        return 'Say something!'
    elif 'hello' in lowered:
        return 'Hi! Are you ready to dive into the world of Tarkovsky?'
    elif 'bye' in lowered:
        return 'До свидания! If you have more questions, feel free to ask.'
    elif 'howareyou' in lowered:
        return 'Fine, just like a Tarkovsky film.'
    elif 'suggestfilm' in lowered:
        return f'{choice(["You should immerse yourself in the cinematic poetry of ", "You should watch", "I suggest you watch"])} {choice(tarky_films)} by Andrei Tarkovsky.'
    elif 'favoritefilm' in lowered or 'bestfilm' in lowered:
        return 'Choosing a favorite Tarkovsky film is like choosing a favorite child, impossible! Each masterpiece has its own unique beauty.'
    elif 'tarkovskystyle' in lowered or 'tarkovskythemes' in lowered:
        return 'Tarkovsky\'s films are known for their slow pacing, long takes, deep symbolism, and exploration of existential themes. His works often invite contemplation and reflection.'
    elif 'help' in lowered:
        return 'Sure! You can interact with me using commands like %favoritefilm, %tarkovskystyle, %tarkovskythemes. If you want to analyze the color of a frame, use the command %analysecolour.'
    else:
        return choice(['I do not understand.',
                       'What do you mean?',
                       'I am not sure I understand.',
                       'I do not know what you mean.',
                       'Do you mind rephrasing that?',
                       'Do you want to watch a film? (Say "%suggestfilm").'])
