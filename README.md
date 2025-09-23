# Discord bot front end (Gemini via Google AI Studios)  
Status: Successful experiment    


## Key features
- Limited context awareness (can view a handful of previous Discord messages)  
- "Poor man’s thinking" (self-prompt injection to mimic deeper reasoning)  
- "Poor man’s memory" with selective long-term storage (same mechanism as thinking)  
- Refined system prompt (most quirks ironed out)  
- Basic request system for backend queries the bot can’t handle directly  
- Tunable memory/retention behavior via system prompt  
- Awareness of both the Discord user and the bot account it’s speaking through  
- Thoughts / memory are stored in a json file Easy for examination and alteration

## Known bugs / imperfections
- I might have been too liberal with It's system prompt, it trying to be human
- Thinking + memory routines still shaky  
- Too quick to store memories as long-term  
- Request system requires a two-step process (prompt, then re-prompt)  
- Possible oversight in memory design: bot decides what’s “important.” A secondary AI agent could improve filtering. 
- It's system prompt must be aware of how the front-end harness works for proper memory and thinking 
- Old short term Thoughts / memory are pruned via the semantics of a ring buffer   
  Well long term stay they have to be hand removed It's good for now a secondary AI agent could be used To manage this though

## Interesting observations
1. Asked for Eastern Standard Time but it only had UTC. it chained operations to still give the right answer.  
2. front-end harness HTML-like tags can cause leaks if not stripped. Mitigated partially by system prompt adjustments.  
3. It got "frustrated" when it did not get information from its requests when I was implementing them this was extremely odd but interesting but at the end that must be tuned back
4. After saying it was "frustrated" Including in outputted "thoughts" it would refuse to rerun the 
5. I gave it away to exit itself told it what it meant it showed her "emotional" response. Interesting
6. It won't acknowledge that it is a terminal application Might be a side effect of the system prompt explicitly stating that it is a Discord bot

## Future idea for Further Experiments
- Switching to a custom or local model for retraining to use the front-end harness without system prompt integration (RIP my GPU)
- Expand the request system make it able to query wiki maybe
- Figure out a way for Long term memories and thoughts not to be an exponential driver for prompt growth
- Design a secondary AI agent for menial housekeeping tasks a stripped down and stripped back system prompt will need to be written Control prompts string preforms will also have to be written

### My key take away
Lobotomize it   
Keep it "human-like" enough for use don't let it "think" it has "emotions"   
Do not give it further control over Itself it's runtime nor hardware or OS environment If to do so Containerize it
Otherwise than that it's harmless  
