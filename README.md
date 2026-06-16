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
