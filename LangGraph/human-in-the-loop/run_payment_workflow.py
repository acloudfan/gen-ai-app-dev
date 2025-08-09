# This can 
# https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Command

import argparse
import time
from payment_processing_workflow import create_graph
from langgraph.types import Command

parser = argparse.ArgumentParser(description="Starts new thread (no thread id needed) or resumes an interrupted thread (requires a thread-id)")
parser.add_argument("--thread_id", "-t", type=str, help="pass the thread id for resuming an interrupted thread")

parser.add_argument("--payment_amount", "-p",  type=float, help="pass the payment amount")
parser.add_argument("--vendor_account_number", "-v", type=str, help="vendor's account number")
parser.add_argument("--approved", "-a", type=str, default='no', help="human decision = yes or no")
parser.add_argument("--approved_by", "-b", type=str,  help="identity of the human taking the decision")
parser.add_argument("--snapshot", "-s", action='store_true',  help="prints the state of the specified thread")

args = parser.parse_args()

# Create the graph
payment_workflow = create_graph()

# Check if the thread id was provided
thread_id = args.thread_id
config = {"configurable": {"thread_id": thread_id}}

snapshot = payment_workflow.get_state(config)
if args.snapshot:
    print(snapshot)
    exit(0)

if thread_id:
    # Check if the thread is interrupted
    if len(snapshot.interrupts) == 0:
        print(f"No interrupts found for the thread = {thread_id}")
        print(snapshot)
        exit(0)

    # Found the interrupted thread
    print(f"Found interrupted thread, will attempt to resume existing interrupted graph!!")

    # Read the human input provided via args
    approved = args.approved
    approved_by = args.approved_by

    # Check if the approval is provided
    if not approved or not approved_by:
        print("ABORTED : Must provide values for 'approved' and 'approved_by'")
        exit(1)

    approved = approved == 'yes'
        
    
    # Resume graph execution from the interrupt
    response = payment_workflow.invoke(Command(resume={"approved": approved, "approved_by": approved_by}), config=config)
    print(response)
    
else:
    # Create a thread_id
    thread_id = int(time.time())
    payment_amount = args.payment_amount
    vendor_account_number = args.vendor_account_number

    # New thread requires the payment amount and vendor information
    if not payment_amount or not vendor_account_number:
        print("ABORTED : Must provide 'payment_amount' and 'vendor_account_number' for starting execution of new thread")
        exit(1)
    
    print(f"Starting a new thread with thread_id = {thread_id}")

    config = {"configurable": {"thread_id": thread_id}}
    
    response = payment_workflow.invoke({"payment_amount": payment_amount, "vendor_account_number": vendor_account_number,"approved": False, "messages": []}, config=config)

    print(response)
    




