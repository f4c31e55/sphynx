# sphynx

## what is it
It's the answer to the following questions
- What happens when you throw your entire toolbox at a problem?
- How can a panda also be a lion?
- What if I want all the things?
- An eagle, a lion and a dragon walk into a bar ...
- Why didn't you just use avatar2?


## components
```
            ┌────────┐
     ┌──────┤ hooman ├───────┐
     │      └───┬────┘       │
     │          │            │
     │          │            │
 ┌───┴───┐   ┌──┴───┐   ┌────┴───┐
 │ eagle ├───┤ lion ├───┤ dragon │
 └───────┘   └──────┘   └────────┘
```
### hooman
That's you! Every good sphynx needs a hooman at the head. And because pwntools implements everything, it has all the interaction capabilities the sphynx will need.
### lion
The concrete execution engine. Like a debugger. Here is where the sphynx gets its legs and can run the program under analysis.
### eagle
The symbolic execution engine. It's angr. Giving the sphynx its wings.
### dragon
The static analysis engine. The disassemebler/decompiler. Let's be honest, it's called dragon, which has no place in the sphynx, so it's a poor effort to sledgehammer ghidra into the toolkit.

## intercomponent interactions
### hooman <-> dragon
- Pop an emulator in your script and call functions from your program. No reimplementation required!
### eagle <-> lion
- angr's symbion, confusingly exposed as OwlBear. Raise a symbolic state from a point during concrete execution. 
