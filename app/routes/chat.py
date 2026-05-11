from fastapi import APIRouter

from app.models.schemas import ChatRequest
from app.services.conversation import conversation_manager
from app.services.retriever import retriever
from app.services.llm_service import generate_response

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    session = conversation_manager.update_memory(
        request.session_id,
        request.message
    )

    # END CONVERSATION
    if conversation_manager.should_end_conversation(
        request.message
    ):

        return {
            "response": "Glad I could help.",
            "recommendations": None,
            "end_of_conversation": True
        }

    clarification = conversation_manager.needs_clarification(
        session
    )

    # ASK CLARIFICATION
    if clarification:

        response = generate_response(
            user_message=request.message,
            session_memory=session,
            recommendations=[],
            clarification=clarification
        )

        session["history"].append({
            "role": "assistant",
            "content": response
        })

        return {
            "response": response,
            "recommendations": None,
            "end_of_conversation": False
        }

    # SEARCH
    search_query = conversation_manager.build_search_query(
        session
    )

    recommendations = retriever.search(search_query)

    response = generate_response(
        user_message=request.message,
        session_memory=session,
        recommendations=recommendations
    )

    session["history"].append({
        "role": "assistant",
        "content": response
    })

    session["recommendations_given"] = True

    return {
        "response": response,
        "recommendations": recommendations,
        "end_of_conversation": False
    }