from sqlmodel import Session, select
from app.models.lesson import Lesson
from app.models.games import Game
from app.models.rewards import Reward

def seed_data(db: Session):
    # Seed Lessons
    if not db.exec(select(Lesson)).first():
        lessons = [
            Lesson(
                title="Greetings and Introductions",
                level="A1",
                content_md="# Greetings\nLearn how to say hello and introduce yourself.\n\nExamples:\n- Hello!\n- My name is Luna.",
                objectives_json={"goal": "Master basic introductions"},
                quiz_json={"q1": "How do you say hello?"}
            ),
            Lesson(
                title="Present Simple Tense",
                level="A2",
                content_md="# Present Simple\nUse it for habits and facts.\n\nExample: I study English every day.",
                objectives_json={"goal": "Learn how to express routines"},
                quiz_json={"q1": "What is the present simple form of 'to go' for 'he'?"}
            )
        ]
        db.add_all(lessons)

    # Seed Games
    if not db.exec(select(Game)).first():
        games = [
            Game(name="Vocabulary Match", type="vocab_match"),
            Game(name="Sentence Builder", type="sentence_builder"),
            Game(name="Grammar Fix", type="grammar_fix")
        ]
        db.add_all(games)

    # Seed Rewards
    if not db.exec(select(Reward)).first():
        rewards = [
            Reward(
                type="cosmetic", 
                key="luna_school_uniform", 
                name="School Uniform Luna", 
                description="Luna's classic school look.",
                cost_coins=100
            ),
            Reward(
                type="badge", 
                key="streak_master_1", 
                name="7-Day Streak Master", 
                description="Complete tasks for 7 days in a row.",
                cost_coins=0
            )
        ]
        db.add_all(rewards)

    db.commit()
