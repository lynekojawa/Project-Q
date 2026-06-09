#PODO Suggested
from ledger_ops import fetch_daily_review_queue

print("----CHECK----")
queue = fetch_daily_review_queue()

if queue == []:
    print("[EMPTY QUEUE]: there is no review")
    print("reason: because we just created node last_reviewed_at is current")
elif len(queue)>0:
    print(f"result: Found {len(queue)} nodes!")
else:
    print("Failed!")