from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import config
from tools import (
    get_order_status,
    calculate_discount,
    calculate_delivery_charge,
    get_estimated_delivery_days,
)

# This connects tool names (as text) to the actual Python functions
# Gemini will send back the name as a string, and we use this map to find the real function
TOOL_MAP = {
    "get_order_status": get_order_status,
    "calculate_discount": calculate_discount,
    "calculate_delivery_charge": calculate_delivery_charge,
    "get_estimated_delivery_days": get_estimated_delivery_days,
}

# Give Gemini access to all four tools, so it can decide when to use them
llm_with_tools = config.llm.bind_tools(list(TOOL_MAP.values()))


def customer_support_assistant(user_query: str, conversation_history: list) -> str:
    """
    Takes the customer's question and the running conversation history.
    Talks to Gemini, runs any tools Gemini asks for, and returns the final answer.
    """
    try:
        # Step 1: add the customer's new message to history
        conversation_history.append(HumanMessage(content=user_query))

        # Step 2: ask Gemini what to do (answer directly, or call a tool)
        ai_response = llm_with_tools.invoke(conversation_history)
        conversation_history.append(ai_response)

        # Step 3: if Gemini asked for tools, run them one by one
        if ai_response.tool_calls:
            for tool_call in ai_response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                selected_tool = TOOL_MAP.get(tool_name)

                if selected_tool is None:
                    tool_result = f"Unknown tool requested: {tool_name}"
                else:
                    try:
                        tool_result = selected_tool.invoke(tool_args)
                    except Exception:
                        tool_result = "Sorry, that tool could not complete the request."

                # Step 4: send the tool's result back, matched to the same tool call ID
                conversation_history.append(
                    ToolMessage(content=tool_result, tool_call_id=tool_id)
                )

            # Step 5: ask Gemini again, now that it has the tool results
            final_response = llm_with_tools.invoke(conversation_history)
            conversation_history.append(final_response)
            return final_response.content

        # No tools were needed, Gemini's first answer is the final answer
        return ai_response.content

    except Exception:
        return "Sorry, I am temporarily unable to complete that request. Please try again."


