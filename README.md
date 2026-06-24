#Project -Q
(6/1-6/5) For sure if I prevent AI to change the variable name that would saved alot more time. <br>
for next prompt gen for code agent I am goint strengthen about this. <br> 
(6/8) Today we are updating parser. so first try with parser it was over creating chapter which was around 139<br>
and now it is over filtering, which is not a good sign. So updating parser to recognizing numberpattern instead of mardowns<br> 
rejected orion's suggestion because I wanted to generalize for other book as well<br>
Generalizing parsar is pain and there are little issues going on for the generalization, it does decent job, and started detecting<br>
more chapters and detailed sub section. But not enough, so for right now, manually fixed the concep_map json to proceed next step.
(6/9) Today we are moving to phase 2, I got comeup with new architecture yesterday but I am going to apply this when I am working on<br>
phase for UI. <br>
Learned different based with PostgredSQL and SQLlitem DB depending on the it can run it light in terminal or not.
(6/10) Today we are continue to phase 2 yesterday I have noticed that there are many files created for phase 2 but there are<br>
some places needs to check up. So today I started with Dante to inspecting the code. <br>
Fixed 
sm2_engine: Implemented quadratic EF decay <br>
evaluation: Unified PASS_Threshold to q>=4 and enforced atomic transactional logging <br>
db_setup: Implemented slugify() for normalized keys and forced DB_PATH.unlink() for state purify<br>
ledger_ops.py: Replaced manual cursor management with with context mangers for autoatic roll back<br>
add test_generation.py and models.py downloaded ollama. <br>
redirected learning style, from right/wrong-> grading and everyproblem hint TO after some number force review. <br>
(6/11) Continue on phase 3
Updated ledger_ops.py, db_setup.py, evaluation py. 
test_logic_integration.py success. Check this with Dante. 
added functions in ledger_ops, table in db_setup, evaluation.py<br>
Updated test_logic_integration.py with real ID from the DB fixed minor things.<br>
Change comments into English, initializing phase 4.<br>
(6/16) Continue on phase 4, catching up and trying to figure out where I left off. Two of my agents(ORION and PODO aren't synced) therefore 
need to find where to continue<br>
Create: skill_tree.py, socratic_mentor.py<br>
So main confusion and error was coming from unmatched table and variabble for example concept_title in evaluation.py and skill_tree.py<br>
and prvious test files so I had to remove concept title and re-aligned the variable names, One good sides of this structured <br>
folder and file is that it is quite easy to catch, one downside is that as an architecture I need to remember which folder has which<br>
and using sqlite means there is no visible table unless checking inside terminal, that's trickier than supabase/postgreSQL<br>
(6/17) Yesterday re-directed the project. there was leaking on inital guide, agents were too excited about Duolingo concept<br>
However that's not exactly I was trying it is also part of it. Today we are jumping into phase 5 which will be summary getting pdf part<br>
(6/18) Started with Dante's commnets separating some functions into ledger_ops.py, the files are containing more functions and easy to get confused. <br>
Before I was losing all of my mind I created the file that tracks the functions only. After all the project is over, will go over again to see if there<br>
is any functions that are not used. Jumping into pdf_prosessor today. pdf_processor and summary pipelines and many movements happend.<br>
(6/19) started with Dante comment. 
1. db/ledger_ops = record_assessment and reset_failure_hisotry and apply_mentoring recovery has no error handling<br>
2. ingestion/sanitizer.py = switching re.sub to str.replace so that this can be faster and cleaner, sanitize markdown and sanitize_pdf_glyphs are not connected<br>
split sanitize markdown into sanitizemarkdown_artifact and sanitize_markdown then combines with danitize all for pipeline.<br>
(6/23) Today we are continue to fix. <br>
On last session AI wasn't able to detect the titles correctly yet, so we are working on it. <br>
hallucinating is bit huge, 1.3 tower of hanoi test has passed however struggling with 3.6 longestincreaing subsequence<br>
For some reason llama thinks ch 2.6 to 2.7 longest increasing subsequence is the chapter it needs to work on. <br>
3. ubmitting to LLM: [np_hardness_12_2_12_2_p_versus_np] -> '12.2 P versus NP'

Summary:
{
  "concept_title": "12.2 P versus NP",<br>
  "core_thesis": "There is no known fast algorithm for CircuitSat.",<br>
  "time_complexity": "O(nc) for some constant c, where n is the size of the input",<br>
  "space_complexity": "N/A",<br>
  "critical_invariants": [<br>
    "P is the set of decision problems that can be solved in polynomial time.",<br>
    "NP is the set of decision problems with the following property: If the answer is Yes, then there is a proof of this fact that can be checked in polynomial time.",<br>
    "co-NP is essentially the opposite of NP. If the answer to a problem in co-NP is No, then there is a proof of this fact that can be checked in polynomial time."
  ],<br>
  "clean_markdown_summary": "The P versus NP problem deals with the relationship between decision problems that can be solved quickly (P) and those that can be verified quickly if we have the solution (NP). The circuit satis\ufb01ability problem is an example of a problem in NP, but it's widely believed to not be in P or co-NP. Researchers have difficulty figuring out exactly which problems can be solved quickly and which cannot."
}<br>

wooohooo! finally! this took so longggg<br>
(6/24) continue on the project, yesterday Ui connection and summary pipeline broken going to working on it. <br>
Moved podo into the different room. currently recalibrating the agents<br> 
Page 118: '3.1. m¯atr¯avr.tta\nf2 f1\nf1 f0f1 f0\nf3\nf2 f1\nf1 f0\nf2\nf1 f0\nf3f4\nf2 f1\nf1 f0\nf3\nf2 f1\nf1 f0\nf2\nf1 f0\n011235813\nf5\nf3f4\nf3\nf1\nf1 f0\nf2\nf4\nf6 f5\nf7\nf2\nfigure 3.2.the recursion tree forf7 trimmed by memo'<br>
bro! what is thisssssssss! 3.1 martravrtta!!! aaaaaaa!!!