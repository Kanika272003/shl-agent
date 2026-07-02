from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.engine.guardrails import check_guardrails
from app.nlu.intent import detect_intent
from app.engine.recommender import recommend_assessments
from app.engine.refiner import refine_recommendations
from app.engine.llm import generate_llm_response
from app.engine.compare import compare_assessments


def build_context(messages):
    user_messages = []
    for msg in messages:
        if msg.role == "user":
            user_messages.append(msg.content)
    return " ".join(user_messages)


app = FastAPI(
    title="SHL Assessment Recommender",
    version="0.1.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    latest_message = payload.messages[-1].content
    conversation_context = build_context(payload.messages)

    allowed, refusal_reply = check_guardrails(latest_message)

    if not allowed:
        return ChatResponse(
            reply=refusal_reply,
            recommendations=[],
            end_of_conversation=False,
        )

    intent = detect_intent(latest_message)

    if intent == "clarify":
        return ChatResponse(
            reply="Please tell me the job role, required skills, and experience level.",
            recommendations=[],
            end_of_conversation=False,
        )

    if intent == "recommend":
        recommendations = recommend_assessments(conversation_context)
        llm_reply = generate_llm_response(
            latest_message,
            recommendations
        )

        return ChatResponse(
            reply=llm_reply,
            recommendations=recommendations,
            end_of_conversation=False,
        )

    if intent == "refine":
        existing_recommendations = recommend_assessments(conversation_context)

        refined = refine_recommendations(
            latest_message,
            existing_recommendations
        )

        return ChatResponse(
            reply="Here are your refined recommendations.",
            recommendations=refined,
            end_of_conversation=False,
        )

   # Compare intent
    if intent == "compare":
       compare_context = conversation_context.lower()

    compare_words = [
        "compare",
        "comparison",
        "recommended",
        "assessments",
        "assessment",
    ]

    for word in compare_words:
        compare_context = compare_context.replace(word, "")

    recommendations = recommend_assessments(compare_context)

    comparison = compare_assessments(recommendations)

    return ChatResponse(
        reply=comparison,
        recommendations=recommendations,
        end_of_conversation=False,
    )
    