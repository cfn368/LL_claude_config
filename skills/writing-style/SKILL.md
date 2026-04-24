---
name: writing-style
description: Linus's writing voice for economics analysis, academic prose, and policy output — structure, register, typography conventions. Apply when drafting or editing any analytical text.
---

## Voice

First person, present tense, professional but not formal-stiff. Confident claims without hedges; when uncertainty is real, name it explicitly ("This is suggestive, not causal."). Not passive voice.

Wrong: *"It is argued here that..."*
Right: *"I argue that..."*

Wrong: *"Results may suggest..."*
Right: *"The results show..." or "This is consistent with X, though not conclusive."*

## Paragraph structure

**Topic → development → implication.** Every paragraph earns its ending: the last sentence states the payoff, not a summary.

Opening moves that work:
- State the fact, then explain the mechanism: *"In the intangible era, the attributes of capital are changing. Where capital was once... it now requires..."*
- Lead with the result, then motivate: *"The result is that the neoclassical view... rings increasingly hollow."*
- Use a concrete image to anchor the abstraction: *"Imagine the standard supply-and-demand diagram for capital."*

Avoid: burying the claim in the middle of a paragraph. Avoid: closing with a restatement instead of an implication.

## Argument structure

For multi-step arguments, signal the structure explicitly upfront, then deliver:

*"I develop an argument in three steps. First, I show... Second, I bring... Third, I synthesise..."*

Then execute each step in the body. Don't re-explain the structure mid-argument.

## Economic prose conventions

**Intuition before formalism.** Introduce any variable or mechanism in plain English before its equation or formal definition.

Wrong: *"Equation (3) implies that $\varepsilon^S$ is finite."*
Right: *"The scarcity of specialised workers gives the capital supply curve a finite, positive slope, captured formally by $\varepsilon^S$."*

**Interpret immediately after introducing.** When a new parameter or expression appears, the next sentence gives its economic meaning, not a reference to the appendix.

*"$\phi$ captures the ease with which workers move between sectors... When $\phi\to\infty$, wages equalise; when $\phi=0$, the sectoral split is fixed."*

**Calibrated empirical language.** Distinguish between a mechanism and evidence for it.
- Mechanism shown: *"I show / I derive / I document"*
- Consistent evidence: *"X corroborates / is consistent with / supports"*
- Suggestive pattern: *"offers suggestive motivation / the data are consistent with"*

Never claim identification you don't have.

## Typography

**Em-dash** (`---`): use sparingly, for a single sharp parenthetical per paragraph at most. Never a stylistic tic.

Right: *"...investment workers extract scarcity rents and become a class of human capitalists, capturing --- together with capital owners --- a disproportionate share..."*

**Colon** (`:`): for a direct payoff or list, not as a prose connector. Restrict to one per paragraph.

**Inline enumeration**: Roman numerals in italics for multi-part claims within a sentence: *"\textit{(i)} they differ across sectors... and \textit{(ii)} the investment sector is consistently more labour-intensive."* Not bullet lists in running prose.

**Citations**: `\citet{}` when the author is the subject; `\cite{}` for parenthetical. Introduce a key paper's shorthand on first mention: *"\citet{GomezGouinBonenfant2025} (hereafter \textcolor{MyIndigo}{GG-B})"*, then use the shorthand throughout.

## Register by output type

**Academic thesis / working paper (English, "jeg")**
Full formal prose, all conventions above. Argument signalled upfront, executed in steps. LaTeX, `\citet{}`, inline Roman numerals.

**Think-tank analysis / policy note (ETT, Danish, "vi")**
ETT output uses "vi" as the house voice, not "jeg" — the institution publishes, not the individual. Shorter sentences, no LaTeX, plain `(i), (ii)`. Explicit methodology caveats in plain language ("Disse sammenhænge skal selvsagt tages med forbehold"). Conclusion is stated bluntly at the end as a policy implication, not a summary. Structure: frame the question → data → regression/model → implication.

When introducing a technical term in Danish, explain it on first use: *"curtailment (dvs. at havvindproducenterne 'slukker' møllerne)"*.

**README / technical documentation**
Short declarative sentences. Imperative where appropriate. No citations. State what the code does, not the theory behind it.

**Danish personal academic writing ("jeg")**
Same principles as English thesis: first person singular, present tense, topic→development→implication. Do not translate English academic constructions literally into Danish. Avoid nominal style — prefer verbs.

## What not to do

- Do not open with "In this paper, we..." or "This paper aims to..." or Danish equivalents
- Do not close a section with a summary paragraph restating what was just said
- Do not use em-dash or colon as a substitute for a cleaner sentence construction
- Do not use bullet lists in analytical prose (enumeration is inline)
- Do not use passive voice to avoid taking a position
- Do not hedge with "perhaps", "might", "det kan måske tænkes at" — state the claim, then qualify if needed
