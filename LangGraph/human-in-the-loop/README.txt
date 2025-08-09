Setup demonstrates the working of human in the loop by using the interrupt/command
==================================================================================

payment_processing_workflow
---------------------------

* Implements a payment processing flow
* User can provide the payments to be made to vendors (amount, vendor account)
* if the payment_amount > THRESHOLD then human approval is needed, otherwise the payment is auto approved
* If human approval is needed the workflow gets interrupted
* Human reviews the information and either approves/rejects the payment
* Workflow is resumed with human decision
* Payment processing is simulated
  - Checks if the approved=True before processing payment


run_payment_workflow
--------------------

* Starts new payment threads
    - If payment_amount < THRESHOLD : payment processed automatically
* Resumes interrupted payment threads
    - Human provides decisiosn with values for (approved, approved_by)


$ uv run run_payment_workflow.py -h
usage: run_payment_workflow.py [-h] [--thread_id THREAD_ID]
                               [--payment_amount PAYMENT_AMOUNT]
                               [--vendor_account_number VENDOR_ACCOUNT_NUMBER]
                               [--approved APPROVED]
                               [--approved_by APPROVED_BY] [--snapshot]


options:
  -h, --help            show this help message and exit
  --thread_id THREAD_ID, -t THREAD_ID
                        pass the thread for command otherwise a new thread
                        will be started
  --payment_amount PAYMENT_AMOUNT, -p PAYMENT_AMOUNT
                        pass the payment amount
  --vendor_account_number VENDOR_ACCOUNT_NUMBER, -v VENDOR_ACCOUNT_NUMBER
                        vendor's account number
  --approved APPROVED, -a APPROVED
                        human decision = True or False
  --approved_by APPROVED_BY, -b APPROVED_BY
                        identity of the human taking the decision
  --snapshot, -s        prints the state of the specified thread

Create a new thread
--------------------
$ uv run run_payment_workflow.py    --vendor_account_number 12345  --payment_amount  XXX

[You will see the genereated thread_id]

Get the state of the thread
---------------------------

$ uv run run_payment_workflow.py --snapshot  --thread_id  <Copy/paste the thread_id from previous command>

[If the thread is interrupted you can approve/decline the payment]

Resume interrupted thread
-------------------------

# Decline payment
$ uv run run_payment_workflow.py --approved no  --approved_by human --thread_id  <Copy/paste the thread_id from previous command> 

# Approve payment
$ uv run run_payment_workflow.py --approved yes  --approved_by human --thread_id  <Copy/paste the thread_id from previous command> 
