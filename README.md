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

bro! what is thisssssssss! 3.1 martravrtta!!! aaaaaaa!!!<br>
(6/29) I decided to wrap this project because it is beyound my knowledge at the moment and here is why I am wrapping up. <br>
My original thought was that creating a program it generates the summary then I will read and THEN <br>
it will give me multiple chose and short answer questions so that I can have ultimate learning process. However, there are many things<br>
that didn't worked out<br>
First, pdf parsing was nightmare I have attached (link) how the titles looks like you can see weird letters plus some are not appear<br>
Second, Hallucination even though I successfully navigate llama to summarizing the book, it started hallucinate after I connected<br>
into ui.<br>
Third, This was largest project I have done with many different folder, before this mine was alot simpler I only needed engine, app<br>
ui and db but now they are all folders containing many files, and checking and debugging folders, so I had hard time to track all the pipelines<br>
This shows that I am still have many things to learn, which I will get used to it eventually. and That will be my next project. <br>
I am heading to netword folder visualizer in one repo, and for the proto type I am going to let it analogue it will be user typing<br>
Those folder names and files, and it will show the relationships. <br>
Here are things that I wished to improve in ui<br>
one, chapter orders are in A-Z so when I was generating all of those summary to wrapup report, I had to look back concept map to trace the chapter<br>
two, Time, it took too long, for summarizing one section it took longer than 45 sec sometimes minutes <br>
What did I learn from this project<br>
I learned that when project is large you need to keep the structures and tracing files and keep the pipeline is important<br>
I still managed to 91 chapter out of 114 study node summary, but no gurantee for the hallucination free. 
I noticed that architectural decisions, like one thing I thought was make user to upload TOC only then use LLM to create concept map <br>
so that user can confirm. so applying human in loop into the architecture to make it smoother. <br>
I also was responsible, in the middle of the project I have noticed that my agents were off, because they were high weighted the duolingo concept<br>
Because when planning stage I was describe this project Q as Duolingo, so I had to re-direct them my intention is like a duolingo but summary is first<br>
This project has started with because I was trying to study Algorithms and wanted to speed up so I feed that prompt and only chapter 1-3 <br>
and it gave me interesting result, (link). That was how it begins<br>
Also, I made the final decision of wrap this project, because I thought it is not worth to proceed at the moment. Firstable I am new and started coding hard <br>
from this april 2026, I am barely new in computer world and I found that the more I project I can do, and deploy with right feature that will help me to learn coding <br>
and programming fast. Second, it was my first local LLM exprience and I do have fair understanding about platform and web AI's but running a local LLM was first<br>
so I did not know quite things about it yet, and third, still my project is successful in some way. as mathematician I have natural habit of <br>
finding what's wrong, or using a wrong context and the 91 generated summaries I can tell it is right or not, and the final conculusion is <br>
Euclid said There is no royal road to geometry, and it can expand to all study. There is no royal road. lol and I was imagining to make royal road<br>
Still it was fun, I was able to read the book and learned alot.<br>
Here are some interesting hallucinating patterns I noticed with my agents, because of noralizations and level of project I have noticed interesting patterns<br>
First, They avoid the answer and closing session early. it is famous fact that AI doesn't good at clocking and my agents was pretending <br>
that it was in middle of the project let's say around 3 pm and it pretend it is either weekends or end of the night<br>
Second, They won't say that they cannot do the work, they still give me something or directing to the other directions<br>
Third, They fix the code but same code similar (unsolved) structure but with diffrent variale name. Especially Gemini<br>
However, this can fixed easily by prompting hard: do not change the variable name. <br>
One thing I need to more care about as human is that:<br>
Keep every agent in right track, and aware of Instant answer. what I meant by instant answer is that they will ask me to <br>
few lines of output or parsed data then generalizing the pattern only with two few examples. That was the moment that as human<br>
The wrapupreport is necessary for make conclusion. right this reminds me I was arguring aboug generalization, One thing I was aware <br>
with the pdf viewer is that the book I was trying to parsing had 14-16 pages of prepage before it start to counts page 1. so you can tell<br>
the printing page and actual pdf pages are off, and this matter alot becuase I need to give a boundary to local LLM to where to start the summary<br>
and I worked with one book, however I wanted to create the summarizing pipeline for ANY Book, but with the boundary problem my agents were<br>
oh it's simple we will fix page 14 to where it starts the summary. and I said so many no to them, I am not creating a program that only does<br>
one book. I think that was so far I am remembering. :D 