import datetime
import sqlalchemy
from db.db_session import SqlAlchemyBase
from pydantic import BaseModel, ConfigDict


class FeedbackModel(BaseModel):
    text : str


class FeedbackAnswer(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str
    model_config = ConfigDict(from_attributes=True)


class Feedback(SqlAlchemyBase):
    __tablename__ = 'feedbacks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sentiment = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.String, nullable=False, default=datetime.datetime.utcnow().isoformat())


    def set_the_sentiment(self) -> None:
        positive = 0
        negative = 0
        for word in self.text.split():
            if any([x in word.lower() for x in ["хорош", "неплох", "спасиб", "люб"]]):
                positive += 1
            if any([x in word.lower() for x in ["плох", "проблем", "ужас", "ненавид", "неудовлетвор"]]):
                negative += 1
        if negative > positive:
            sentiment = "negative"
        elif positive > negative:
            sentiment = "positive"
        else:
            sentiment = "neutral"
        self.sentiment = sentiment

    def to_return(self):
        return FeedbackAnswer(id=self.id, text=self.text, sentiment=self.sentiment, created_at=self.created_at)






''' 
Я б вообще предложил сделать так, это не особо затратно, но работает неплохо, ну и хранить отзывы в elasticsearch или
в faiss, чтобы потом можно было быстро искать по отзывам


@broker.subscriber("requests")
async def answer_to_request(data: str):
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    llm = ChatOllama(model=LLM_MODEL)
    retriever = vectorstore.as_retriever()
    template = """
    Используй приведенный ниже контекст, чтобы определить, негативный отзыв или позитивный. 
    Если затрудняешься с ответом, то ставь нейтральный
    В ответ приведи: negative | positive | natural 
    Контекст: 
    {context}

    Вопрос: {question}

    Ответ:
    """
    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()
    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | output_parser
    )
    question = data
    await broker.publish("Генерация ответа началась...", queue="answers")
    try:
        response = rag_chain.invoke(question)
        await broker.publish(response, queue="answers")
    except Exception as e:
        print(f"Ошибка во время выполнения RAG chain: {e}")
        await broker.publish(f"Произошла ошибка при обработке вашего запроса.", queue="answers")
'''

