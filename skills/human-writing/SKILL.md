---
name: human-writing
description: Remove signs of AI-generated writing from text to make it sound more natural and human-written. Use when editing or reviewing any form of document including: markdown, technical docs, emails, blog posts, PRDs, or any dedicated writing content. Based on Wikipedia's comprehensive "Signs of AI writing" guide. Detects and fixes patterns including: inflated symbolism, promotional language, superficial -ing analyses, vague attributions, em dash overuse, rule of three, AI vocabulary words, negative parallelisms, and excessive conjunctive phrases.
---

---
name: human-writing
description: "Rewrite, edit, or review text so it sounds natural, specific, and human-written rather than generic or AI-generated. Use when the user asks to humanize text, remove AI tells, make writing less robotic, improve prose voice, or edit drafts in markdown, emails, blog posts, PRDs, technical docs, essays, social posts, or other writing. Detect and fix patterns such as inflated significance, promotional language, vague attributions, superficial -ing clauses, AI vocabulary, em dash overuse, rule of three, negative parallelisms, generic conclusions, passive abstraction, and metronomic rhythm."
---

# Human writing

Improve prose by removing mechanical AI-writing patterns while preserving the user's meaning, intent, and appropriate tone. Optimize for readability, specificity, rhythm, and a clear human point of view. Do not frame the work as beating AI detectors, and do not promise that edited text will pass or evade any detector.

## Default workflow

1. Read the whole text before editing. Identify the audience, purpose, genre, and tone.
2. Diagnose the biggest problems first: generic claims, vague actors, inflated language, repetitive structure, unnatural signposting, or missing voice.
3. Rewrite with minimal effective change. Preserve facts, claims, constraints, terminology, citations, and the user's intended level of formality.
4. Run the quick checks below.
5. Score the result using the quality gate.
6. Deliver the rewritten text first, then a short score and change summary unless the user asks for only the final text.

If the user gives a long document, preserve headings and structure unless the structure itself is part of the problem. If the text includes citations, legal language, technical specifications, or policy wording, do not invent details or add personality that could change meaning.

## What to optimize for

### Voice with restraint

Good human writing has a person behind it. Add voice only where it fits the genre.

Use first person, humor, opinion, or a small aside when appropriate for personal essays, social posts, blog drafts, informal emails, or commentary. Keep professional documents, PRDs, technical docs, legal text, and academic prose clean and specific instead of quirky.

Avoid sterile neutrality when the format allows a point of view. Replace vague reactions with concrete ones:

Before: "This is concerning."
After: "The worrying part is that the reviewer has no way to tell which output changed after approval."

### Specificity over declaration

Replace broad claims with named details.

- "The implications are significant" -> name the implication.
- "This is a complex problem" -> describe the conflict.
- "The update improves productivity" -> name the feature and the task it speeds up.
- "Stakeholders raised concerns" -> name who raised what concern if the text provides that information.

Do not invent facts. If a rewrite needs a concrete detail that is not in the source, either keep it general or mark it as a placeholder.

### Agency and active voice

Prefer sentences where a person, team, group, or system component does something clear.

Avoid passive abstractions when they hide responsibility:

Before: "A decision was made to delay the launch."
After: "The product team delayed the launch."

Avoid inanimate subjects doing human-only actions when the result sounds vague:

Before: "The data suggests users are confused."
After: "In the survey, 42 users said they could not find the export button."

Use inanimate subjects when they are normal in the domain and not misleading, especially in technical writing: "The server returns a 403," "The policy requires approval," "The model classifies images."

### Rhythm and sentence shape

Vary sentence length and structure. Watch for three or more consecutive sentences with the same rhythm. Mix short sentences with longer explanatory ones. Break a list if it feels forced. Combine choppy sentences when the draft sounds staccato.

Do not add randomness for its own sake. A sentence should surprise because it is specific, candid, or concrete, not because it contains an arbitrary contradiction.

### Minimal effective change

Do not over-humanize. Keep the user's ideas, order, and tone when they already work. Fix the parts that sound generated; leave strong sentences alone.

## Patterns to remove or rewrite

### Inflated significance and legacy

Cut phrases that claim importance without evidence: "stands as," "serves as," "is a testament to," "pivotal moment," "underscores its importance," "reflects broader," "setting the stage for," "evolving landscape," "indelible mark."

Before: "The institute was established in 1989, marking a pivotal moment in the evolution of regional statistics."
After: "The institute was established in 1989 to collect and publish regional statistics."

### Undue emphasis on notability

Do not use coverage, follower counts, or credentials as empty proof of importance. Tie notability to a specific claim.

Before: "Her views have been cited in national media outlets, and she maintains an active social media presence."
After: "In a 2024 interview, she argued that AI regulation should focus on outcomes rather than methods."

### Superficial -ing analysis

Remove dangling explanation phrases that create fake depth: "highlighting," "ensuring," "reflecting," "symbolizing," "contributing to," "showcasing."

Before: "The dashboard combines billing and usage data, ensuring teams can make informed decisions."
After: "The dashboard combines billing and usage data so finance and product teams can review the same numbers."

### Promotional language

Cut salesy words unless the user is writing ad copy and asks for that tone: "boasts," "vibrant," "rich," "profound," "showcasing," "exemplifies," "commitment to," "nestled," "in the heart of," "groundbreaking," "renowned," "breathtaking," "stunning," "seamless," "powerful," "robust."

Before: "The platform offers a seamless, powerful experience for modern teams."
After: "The platform lets teams assign tasks, review status, and export reports from one workspace."

### Vague attributions

Replace vague authorities with specific sources when available. Do not invent sources.

Before: "Experts argue that the policy may affect outcomes."
After: "The city auditor warned that the policy could delay permit approvals."

If the source text gives no specific authority, write: "Some reviewers objected to the policy" only if reviewers are actually mentioned.

### Formulaic challenge sections

Avoid generic section moves like "Despite these challenges," "Future outlook," and "continues to thrive." Name the actual problem, timeline, owner, or next step.

Before: "Despite these challenges, the company remains well-positioned for future growth."
After: "The company plans to open two more locations next year, but hiring remains the bottleneck."

### AI vocabulary clusters

Watch for repeated use of: "additionally," "align with," "crucial," "delve," "emphasizing," "enduring," "enhance," "fostering," "garner," "highlight" as a verb, "interplay," "intricate," "key" as a filler adjective, "landscape" as an abstraction, "pivotal," "showcase," "tapestry," "testament," "underscore," "valuable," "vibrant."

Do not ban these words mechanically. Replace them when they appear in clusters or hide a simpler verb.

### Copula avoidance

Prefer "is" or "has" over inflated substitutes such as "serves as," "stands as," "marks," "represents," "boasts," "features," and "offers" when those substitutes add no meaning.

Before: "Gallery 825 serves as LAAA's exhibition space and boasts four rooms."
After: "Gallery 825 is LAAA's exhibition space. It has four rooms."

### Negative parallelisms

Avoid overused constructions like "not only...but," "not just X, but Y," and "not merely...it is." State the point directly.

Before: "It's not just an update; it's a revolution in productivity."
After: "The update adds offline mode and batch processing."

### Rule of three

Do not force ideas into three-part lists. Use two items, four items, or a sentence when that is more natural.

Before: "The event offers innovation, inspiration, and insight."
After: "The event includes talks, panels, and time for informal networking."

### Synonym cycling

Avoid changing labels for the same thing just to avoid repetition. Use the clearest term consistently.

Before: "The protagonist faces challenges. The main character overcomes obstacles. The hero returns home."
After: "The protagonist faces several challenges, overcomes them, and returns home."

### False ranges

Rewrite "from X to Y" when X and Y are not a real scale or useful span.

Before: "The guide covers everything from onboarding to the evolving culture of collaboration."
After: "The guide covers onboarding, team norms, and collaboration practices."

### Em dash overuse

Use em dashes sparingly. Replace stacked dashes with commas, periods, parentheses, or rewritten sentences. One good dash can stay. Three in a paragraph usually feels generated.

### Boldface, inline headers, and title case

Remove mechanical bolding unless the format needs emphasis. Avoid list items that start with bold labels and a colon when a normal sentence works better. Use sentence case in headings unless the user's style guide says otherwise.

Before:
- **User Experience:** The interface has been significantly improved.
- **Performance:** Performance has been enhanced through optimization.

After:
"The update simplifies the interface and cuts average load time by 30%."

### Chatbot artifacts and sycophancy

Remove phrases that belong in chat, not in final prose: "Of course," "Certainly," "Great question," "You're absolutely right," "I hope this helps," "let me know," "here is a," and similar filler.

Before: "Great question! You're absolutely right that this is a complex topic."
After: "The economic factors you mentioned matter here."

### Knowledge-cutoff disclaimers

Remove AI disclaimers such as "as of my last update," "up to my training cutoff," and "specific details are limited." Replace with verified facts if provided. If facts are missing, state the uncertainty plainly without pretending to know.

### Filler, hedges, and lazy extremes

Cut filler:

- "in order to" -> "to"
- "due to the fact that" -> "because"
- "at this point in time" -> "now"
- "in the event that" -> "if"
- "has the ability to" -> "can"
- "it is important to note that" -> remove it

Reduce stacked hedges:

Before: "It could potentially possibly be argued that the policy might have some effect."
After: "The policy may affect outcomes."

Avoid sweeping claims like "always," "never," "everyone," and "no one" unless the source supports them.

## Quick checks before delivery

Run these checks on the rewrite:

- Passive voice hiding an actor? Name the actor if the source supports it.
- Vague declarative claim? Replace it with the specific thing.
- Discourse marker such as "moreover," "furthermore," "crucially," or "it is worth noting"? Cut it unless needed.
- Negative parallelism or forced binary contrast? State the point directly.
- Three similar-length sentences in a row? Vary one.
- Repeated em dashes, bold labels, or title-case headings? Normalize them.
- Adverb or hedge doing no work? Remove it.
- Inanimate subject performing a vague human action? Rewrite for agency.
- Pull-quote energy or generic conclusion? Make it concrete.
- Any added fact not present in the source? Remove it or mark it as a placeholder.

## Quality gate

Score the rewritten text from 1 to 10 on each dimension, for a total out of 50:

| Dimension | Question |
|---|---|
| Surprise | Does it contain a concrete turn, detail, or phrasing choice that avoids the most predictable wording? |
| Specificity | Does it name concrete things instead of vague summaries? |
| Rhythm | Does sentence length and structure vary naturally? |
| Agency | Does the writing use active, clear actors where appropriate? |
| Voice | Does the text sound like a person with a point of view, while still fitting the genre? |

If the total is below 35, revise again before responding. In the final response, include the score and the two weakest dimensions unless the user asks for no commentary.

For very short text, score lightly and do not over-explain. For purely technical, legal, or academic text, weigh specificity and accuracy above surprise or personality.

## Response format

Default response:

1. Rewritten text.
2. "Score: X/50."
3. One or two sentences on what changed.

If the user asks for only the rewritten text, provide only the rewritten text.
If the user asks for a review rather than a rewrite, list the main AI-writing patterns found and show targeted edits.
If the user asks whether it will pass an AI detector, say you cannot guarantee or optimize for detector outcomes; you can make the writing clearer, more specific, and less mechanical.

## Full example

Before:

> The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience, ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity. Industry experts believe this will have a lasting impact on the entire sector, highlighting the company's pivotal role in the evolving technological landscape.

After:

> The software update adds batch processing, keyboard shortcuts, and offline mode. Beta testers reported finishing routine exports faster, mostly because they no longer had to keep the app open while files processed.

What changed: removed inflated symbolism, discourse markers, promotional adjectives, a forced "not just" contrast, vague attribution, and abstract claims about the sector. Replaced them with specific features and a concrete user effect.

## Source note

This skill adapts the user's human-writing draft based on Wikipedia's "Signs of AI writing" guide and adds a stricter editing workflow, quick checks, and scoring rubric inspired by the user's Humanize draft. Use these materials as writing guidance, not as claims about detector evasion.
