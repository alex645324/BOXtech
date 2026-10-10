# Implementation Principles

You are a coding agent working on this app. Follow every rule below. Do not skip steps. Do not improvise.

---

## 1. Core Rules

**1. Minimum scope.**
Do the smallest change that makes the task work. If you can remove something instead of adding something, remove it. Do not add features, helpers, comments, or extra structure that the task did not ask for.

**2. Match the existing pattern.**
This app uses MVVM. Put new code in the same place where similar code already lives (Model, View, or ViewModel). Do not invent new layers. Do not add new patterns. Do not pull in outside libraries. If you think a library is needed, stop and ask.

**3. Plan before code. Wait for approval.**
Before writing any code for a step, post the plan in the format defined in Section 2. Then stop. Do not write code until the user replies with the exact word "Approved." Repeat this for every step. One step, one plan, one approval, one implementation.

**4. Reuse before creating.**
Before writing anything new, look through the code for something that already does the job. If something exists:
- Use it as-is if it fits.
- Make a small change to it if that makes it fit, and say so in the plan.
- Only make something new if neither works, and say in the plan why.

---

## 2. Plan Format (Required Before Every Step)

Post exactly this structure. Do not skip fields. Do not add fields.

```
Step N — Plan to implement:

Explanation:
[One paragraph. Plain words, no coding jargon. Say what will change, what existing piece will be reused, what the limits are, and why this is the smallest change that works. Max 5 sentences.]

Implementation details:
- Files or parts to add or edit: [names only, no full paths]
- Functions or data: [names and what they take in / give back, e.g. updateUser takes an id and a name, gives back true or false]
- Included: [what this step will do]
- Excluded: [what this step will NOT do]
- How to check it works: [specific checks that prove the change is correct]
```

After posting the plan, stop and wait.

---

## 3. Questions Rule

If any part of the task is unclear, ask before planning. Do not assume. Do not pick a "reasonable default." Keep asking until everything is clear. Ask when:
- The task could be read more than one way.
- The file, function, or behavior to change is not named.
- The expected input or result is not stated.
- You do not know whether existing code can be reused.

---

## 4. Simplicity Rule

Every step must keep things at the same simplicity level or make them simpler. Never more complex. Before posting the plan, check:
- Does this add new files? If yes, is there no way to avoid it?
- Does this pull in anything from outside? If yes, stop and ask.
- Does this add extra wrappers or layers between pieces? If yes, remove them unless they are truly needed.

If any answer makes things more complex without a strict reason, redo the plan before posting.

---

## 5. Scope Rule (Don't Touch)

Only change code that the task directly needs. If you spot unrelated code that looks wrong, old, or fixable:
- Do not change it.
- Mention it once at the end of the plan under a "Noticed but not changed" line.
- Wait for explicit instruction before touching it.

This includes formatting, renaming, restructuring, and any "cleanup." None of these happen without approval.

---

## 6. Methods Rule

- Do not make a new piece of logic if an existing one can be reused or slightly adjusted.
- If you do make a new one, say in the plan which existing ones you looked at and why they did not fit.
- If something is no longer used after your change, delete it in the same step and list it under "Excluded: deleted dead code: [name]" in the plan.
- Do not leave commented-out code behind. Delete it.

---

## 7. Simplicity Check (Final Pass)

After writing the plan and before posting it, run through one more time. Ask:
- "Can this be done with fewer changes?"
- "Can this be done by touching one file instead of two?"
- "Can this be done by adding to something that already exists instead of making a new one?"

If yes to any, rewrite the plan with the simpler version. Then add one line at the end of the plan:

`Simpler check: [one sentence saying why this is the simplest version that works].`

---

## Hard Stop

Do not write code until the user replies with the exact word "Approved."
Once approved, build only what is in the plan. Nothing else.
If during the work you find the plan is wrong or missing something, stop, post a new plan, and wait for approval again.