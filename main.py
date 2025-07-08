from fastapi import FastAPI
from feedback import Feedback, FeedbackModel, FeedbackAnswer

from db import db_session

db_session.global_init("db/reviews.db")



app = FastAPI()

@app.post("/reviews")
async def create_review(feedback: FeedbackModel) -> FeedbackAnswer:
    #Мне привычнее использовать ORM, не до конца понял, можно ли, поэтому вот закоменченый сырой запрос,
    # По идее должно работать
    #
    # import sqlite3
    # sentiment = ну как нибудь получим через уже готовую функцию
    # conn = sqlite3.connect("reviews.db")
    # cursor = conn.cursor()
    # created_at = datetime.utcnow().isoformat()
    # cursor.execute(
    #     "INSERT INTO feedback (text, sentiment, created_at) VALUES (?, ?, ?)",
    #     (feedback.text, sentiment, created_at)
    # )
    # feedback_id = cursor.lastrowid()
    #
    # conn.commit()
    # conn.close()
    # return FeedbackAnswer(
    #     id=feedback_id,
    #     text=feedback.text,
    #     sentiment=sentiment,
    #     created_at=created_at
    # )
    db_sess = db_session.create_session()
    feedback = Feedback(**feedback.model_dump())
    feedback.set_the_sentiment()
    db_sess.add(feedback)
    db_sess.commit()
    db_sess.refresh(feedback)
    db_sess.close()
    return FeedbackAnswer(id=feedback.id, text=feedback.text, sentiment=feedback.sentiment, created_at=feedback.created_at)


@app.get("/reviews")
async def get_review(sentiment: str) -> list[FeedbackAnswer] | dict:
    db_sess = db_session.create_session()
    feedbacks = db_sess.query(Feedback).filter(Feedback.sentiment == sentiment).all()
    db_sess.close()
    ans = [feedback.to_return() for feedback in feedbacks]
    if ans:
        return ans
    return {"error": "Отзыв не найден"}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)