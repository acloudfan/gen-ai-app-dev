# https://changelog.langchain.com/announcements/interrupt-simplifying-human-in-the-loop-agents
# https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt
# Requires: langgraph-checkpoint-sqlite
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from langchain_core.tools import tool

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

from langgraph.types import interrupt,Command
from typing import TypedDict

HIGH_RISK_THRESHOLD = 500.00  # Threshold for payments requiring human approval

# Has the messages implicitly
class PaymentState(MessagesState):
    payment_amount: float               # Amount to be paid
    vendor_account_number: str          # Vendor identity
    reason: str = "payment pending"     # Reason for approval/rejection
    approved: bool = False              # This is set to True if approved automatically or by human
    approved_by: str = None             # Identity of the human who approved/rejected
    processed: bool = False             # Set to True once the payment is processed


# Node to check if approval is required
def check_approval_required(state: PaymentState) -> TypedDict:
    """Decision node that routes the workflow based on payment amount"""

    print("BEGINNING : check_approval_required")
    
    if state["payment_amount"] < HIGH_RISK_THRESHOLD:
        return {
                    "approved" : True,
                    "approved_by" : "automatic",
                    "reason" : f"Auto-approved: ${state['payment_amount']:,.2f} under threshold",
        }
    else:
        return {
                    "approved_by" : "None",
                    "reason" : f"Human approval needed : ${state['payment_amount']:,.2f} over threshold",
        }
        


# Tool simulates the payments for services. This may be considered as a high risk tool.
@tool
def vendor_payment_tool(
    payment_amount: float, 
    vendor_account_number: str,
    approved: bool = False, 
    approved_by: str = None
) -> dict:
    """
    Processes vendor payments based on approval status and logs transaction details.
    
    This tool handles both pre-approved payments and real-time payment processing decisions.
    It serves as the execution endpoint after approval checks are complete.

    Args:
        payment_amount: The monetary amount to be processed (must be positive)
        vendor_account_number: Unique identifier for the vendor/recipient
        approved: Flag indicating whether payment has been pre-approved (default: False)
        approved_by: Identifier of the approving entity/person when pre-approved (optional)

    Returns:
        Dictionary containing:
            - processed: Boolean-like status (True if payment attempt was made)
            - reason: Detailed explanation of payment outcome
            - amount: Processed payment amount (for verification)
            - vendor: Vendor account number (for audit trail)
            - approved_by: Entity that authorized the payment (when applicable)

    """

    print("BEGINNING : vendor_payment_tool")

    if approved:
        return {
            "processed": True,
            "reason" : f"Payment processed as it was approved by: {approved_by}"
        }
    else:
        return {
            "processed": False,
            "reason": f"Payment of ${payment_amount:,.2f} declined by human",
        }

# This node represents the human in the loop
def human_approval_node(state: PaymentState)->dict:
    
    print("BEGINNING : human_approval_node")

    if state["approved"]:
        approved = state["approved"]
        approved_by = state["approved_by"]
    else:
        # value = interrupt( {"messages": state["messages"], "approved": state["approved"], "approved_by": state["approved_by"]}) #
        value = interrupt(state) # This can be partial instead of entire state

        # Print the values received from human
        print(f"HUMAN VALUE RECVD. {value}")

        approved = value["approved"]
        approved_by = value["approved_by"]
        
    # Simulate a tool call
    tool_call_message = AIMessage(
        content = "dummy",
        # Add one or more tool calls
        tool_calls = [
           {"name": "vendor_payment_tool", 
            "args": {
                     "payment_amount": state["payment_amount"], 
                     "vendor_account_number": state["vendor_account_number"], 
                     "approved": approved,
                     "approved_by": approved_by,
                     },
                     "id": "dummy"
            }
        ]
    )
    
    return {"messages": [tool_call_message], "approved": approved, "approved_by": approved_by}

# A node that checks if approval is needed 
def  create_graph():
    payment_workflow_builder = StateGraph(PaymentState)
    payment_workflow_builder.add_node("approval_checker", check_approval_required)
    payment_workflow_builder.add_node("human_approval", human_approval_node)

    payment_tool_node = ToolNode(
        name = "tool_node",
        tools = [vendor_payment_tool]
    )
    payment_workflow_builder.add_node("payment_tool", payment_tool_node)

    # edges
    payment_workflow_builder.add_edge(START, "approval_checker")
    payment_workflow_builder.add_edge("approval_checker", "human_approval")
    payment_workflow_builder.add_edge("human_approval", "payment_tool")
    payment_workflow_builder.add_edge("payment_tool", END)

    # Checkpointer
    conn = sqlite3.connect('payment_workflow_checkpointer_store.db', check_same_thread=False)
    sqlite_checkpointer = SqliteSaver(conn)

    payment_workflow = payment_workflow_builder.compile(checkpointer = sqlite_checkpointer)

    return payment_workflow

# generate the graph
def generate_graph(payment_workflow):
    png_graph = payment_workflow.get_graph().draw_mermaid_png()
    with open("payment_workflow.png", "wb") as f:
        f.write(png_graph)
    

## Generate image
if __name__ == "__main__":
    payment_workflow = create_graph()
    generate_graph(payment_workflow)  





    
    
    