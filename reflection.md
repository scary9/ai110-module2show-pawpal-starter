# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- Core Logic: Three core actions that the software should include would be adding a pet and its profile, adding an owner profile and including preferences and contraints for the owner, and creating a daily plan that accounts for time, action, and contraints for each pet. For the daily plan, a linear calendar-like format would be ideal. 

- BRAINSTORMING:
    - each owner profile should have preferred time and preferences
        ~ add pet
        ~ remove pet
        ~ update avaliability
        ~ update preferences
    - each pet profile should have attributes included (walks, meds, grooms, etc) and assigned owners
        ~ update priority
        ~ feed pet
        ~ walk pet
        ~ groom pet
        ~ feed
        ~ play
    - each daily plan should specify each pet the plan is for and fit the time constraints of the owner and explain reasoning
        ~ add tasks
        ~ remove tasks
        ~ get description (why is the plan effective for the assistant and pets)

- Briefly describe your initial UML design.
My initial UML design was short and consise, but lacked a few features to combat edge case scenarios. 
- What classes did you include, and what responsibilities did you assign to each?
The classes I included for my UML was a class for the owner of each pet featuring functions like add pet. Another class was for the specific pet and featured functions like feed. The last class was a plan class that documented the plans for each pet and featured functions such as add tasks to the plan.

**b. Design changes**

- Did your design change during implementation? 
Yes.
 
- If yes, describe at least one change and why you made it.
When the AI coding assistant generated the UML then subsequently the skeleton, I later noticed the AI added features that were beyond the scope of what I aksed for--the software could be much simpler. I went back through and told the coding assistant to drop the creation of a task doer since that overcomplicated the program. Additionally, I asked the AI to drop the creation of a Scheduler since that was not needed. Moreover, the coding assitant created the UML with the scenario of there being multiple owners. I make things simpler, I adjusted the program to model having only one owner. As a result, I was able to trim the amount of code in the skeleton to be cleaner and more efficent. Lastly, after the changes were implemented, tasks now have an end, same name pets count as seperate types of pets, and removed the pet-counter box. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)? 
One of the constraints my scheduler considers is time using the datetime class. Another constraint my scheduler considers is priority for the task. For example, a task can have a high, medium, or low priority. 
- How did you decide which constraints mattered most?
For my scheduler, the constraint that mattered the most was priority due to the filtering and sorting system of the app.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff my scheduler makes is longer lines of code but lower in nesting which is good for readability. 
- Why is that tradeoff reasonable for this scenario?
This tradeoff is reasonable because before, a list of all pets' tasks would be created for only one pet. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
During the project, I used the AI tools to refactor method implementations for performance and efficiency. Another way I used the AI tools was for debugging the code and for understanding. Using the AI coding assistant as a bridge for implementation and learning was helpful. 
- What kinds of prompts or questions were most helpful?
Asking why the implementation was the most efficient approach for app design allowed me to understand the backend of the assignment. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When drafting my UUML design, the AI suggested features that went beyond the scope of the project.
- How did you evaluate or verify what the AI suggested?
Referring to the assignment instructions and the README to evaluate the suggestions that the AI gave allowd me to determine that some features were beyond the scope, such as the use of an API.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
The behaviors I tested were adding a pet and task for a pet.
- Why were these tests important?
These tests were important because if these features were not implemented correctly, the sorting and filtering logic would not work properly. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am fairly confident that my scheduler works correctly because I thoroughly investigated the AI suggestions for the efficiency of the app.
- What edge cases would you test next if you had more time?
The edge cases I would test next time if I had more time would be testing owner avaliability.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The part of the project that went well was implementing the features such as the filering, sorting, and conflict warnings. The AI coding assignment provided comments that allowed me to assess if something was needed or not and make the design process enjoyable. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would redesign why the task was dropped once removed.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important think I have learning about designing systems is taking one step at a time. By blocking each step, reviewing, accepting, and declining recommendations in chunks allowed for a smoother implementation process. It could also help implement the code faster. 
