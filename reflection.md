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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
