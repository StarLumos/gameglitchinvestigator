# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game looked like a regular guessing game. However, one thing I noticed was that if the GUI was really for the game, the developer debug info shouldn't have been there since it gives the answer, but for purely debugging purposes, it isn't much of a problem. Toggling the "show hint" button seems to work as well.

- List at least two concrete bugs you noticed at the start.
At first, it didn't look like there were any bugs. However, when the answer to the first round was revealed, I realized that the hints were pointing me in the wrong direction the whole time. Another issue I did find immediately, though, was the small note on the rightside of the answer entry box telling players to hit enter to submit their answer, but upon hitting enter, the answer wasn't submitted. I instead had to click on the "submit guess" button. Furthermore, when I submit my first guess, the "attempts left" read the same as before -- 7 stays as 7 and doesn't become 6 like it should. Afterwards, however, the counter decreases by 1 correctly.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

|    Input    | Expected Behavior |  Actual Behavior | Console Output / Error | Suspected Code Location 
|-------------|-------------------|------------------|------------------------|--------------------------
| guess of 50 |     go lower      |     go higher    |         none           | app.py check_guess()
| guess of 73 | no answer reveal  |  answer reveal   |         none           | app.py update_score()
| guess of 74 |  correct answer   | no attempts left |         none           | app.py check_guess()

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used the Claude AI assistant in VS Code.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I asked Claude to move check_guess() from app.py to logic_utils.py, fix the moved function so that the hints point the player in the correct direction, and add an import to app.py so that check_guess() was still accessible where it was needed. The AI assistant did exactly that and corrected check_guess(). It didn't go outside of its scope or make incorrect changes to check_guess(), which was extremely helpful in terms of its role as an assistant.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
I noticed that on even-numbered attempts (attempt 2, 4, 6, etc), the secret is converted to a string before comparison and being passed through check_guess(), so I asked Claude to fix it. It fixed it correctly. However, while writing the pytests I asked it to create afterwards, it ran 'git stash' on 'app.py' without being asked. Although it did run 'git stash pop' straight away, it was still out of the scope of the request, so I undid the changes that it made to check if the tests fail without the fix.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
The first thing I did to ensure that a bug was really fixed was run all of the pytests after each bug, regardless of whether or not Claude told me if the pytests they had run had passed or not. Afterwards, I'd play another round of the game to ensure that the game was still working and that the bug was indeed fixed.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
One of the first big changes I made to my code was the correction of hints when the player enters an incorrect guess. Like I mentionned before in my previous response, I used both pytest and manual testing to ensure that the bug was fixed. Once I saw that the pytest was successful, I played the game again, this time keeping close attention on the secret as listed in the developer debugging info, and purposefully guessing numbers that were incorrect until the last moment. 
- Did AI help you design or understand any tests? How?
Claude did play an integral part in designing pytests, as well as help me understand why each pytest was designed the way they were. It also allowed me to see how each pytest plays an important part in the debugging verification process.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
During Streamlit "reruns", the entire script is re-executed from top to bottom everytime something triggers it -- in this case, it would be another guess from the player. That said, it's important to save certain variables across reruns, which is where session state comes in. In this project, it includes things like the secret number (which particularly needs to be keep constant).

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I really liked that I kept track of all of the changes that I made just with comments here and there, which ultimately allowed me to look back for commit messages and potential reporting (if this were for a collaborative project, for example).
- What is one thing you would do differently next time you work with AI on a coding task?
One thing I forgot to do as I was coding (partly because the instructions on the CodePath page wasn't very clear) was multiple git commits after each bug fix. This would've also helped me when I looked back on the changes that I made in GitHub, making the transitions very clear.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This is the first time I've seen AI not be used minimally or not be blindly, heavily relied on through the project. Heavy reliance often comes with the ability to use critical thinking when making technical decisions or reading code, but I was pleasantly surprised with how in-control I felt when working with AI on this project.
