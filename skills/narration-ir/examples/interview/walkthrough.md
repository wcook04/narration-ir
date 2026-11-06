# A shorter interview, the same claim

The opening question is: **How can an interview become shorter without changing
what the speaker meant?** The payoff is a before/after comparison in which the
silence changes but the qualifying words remain.

This is a fictional 64-second planning fixture. Each stage has eight seconds;
word times are synthetic and deliberately convenient for inspection. There is
no source audio, rendered clip, or retention measurement. Do not present these
timestamps as an alignment result. See [source.md](source.md) and [plan.json](plan.json).

| Stage | Narration | What the picture must communicate |
| --- | --- | --- |
| 01 Question | How can I shorten this interview without changing what the speaker meant? | The same speaker's statement persists throughout the comparison. |
| 02 Source | First I keep the original recording, so every proposed cut has a reference. | An unchanged original remains available beside the proposed edit. |
| 03 Meaning | The speaker says they saved time for this interview, not for every interview. | “For this interview” is visibly attached to the claim. |
| 04 Cut | I remove the pause, but keep the qualification. | Only the silence disappears; the qualification remains. |
| 05 Compare | Now the same words take less time because only the gap has closed. | Compare identical words on timelines of different length. |
| 06 Listen | I listen across the cut to hear whether the sentence still sounds natural. | Listening is a review action with an unresolved result, not a green certification. |
| 07 Limits | Word timestamps help me find the edit, but they cannot judge its meaning. | Timing evidence and meaning review remain separate. |
| 08 Payoff | The interview is shorter, and the speaker's original qualification is still there. | Return to the opening comparison and show the retained qualification. |

The global profile suggests a small 01–08 stage indicator. Reuse the same original
and edited tracks across stages instead of introducing eight unrelated pictures.
The example has educational value; surprise or emotion can support it but are not
mandatory fields to manufacture in every sentence.

## One sentence, expanded

Stage 04 has eight spoken words. Its `meaning` field explains the difference
between silence removal and claim alteration, what the source supports, what the
editor can change, and why the qualification must remain. Adjacent fields record
audience knowledge, misconceptions, exclusions, source excerpts, persistent objects
and required visual operations. The elaboration is context for the animator,
not a paragraph to put on screen.

The first obligation closes the gap on the occurrence of “remove.” The event is
marked `settled`: the gap finishes closing on that word's start, so a 0.4-second
transition begins 0.4 seconds earlier. A second obligation holds the qualification
on “keep.” Stable IDs distinguish these occurrences from identical words elsewhere.

Run the packet command from the repo README to see the actual resolved schedule.
Change `sync` from `settled` to `onset` and validate again: now the movement starts
on the word and finishes later. Both may be useful treatments; they are different
timing promises.

## A misleading treatment and its repair

**Rejected proposal:** cross out the silence and “for this interview,” then replace
the source quotation with “AI saves time.” An attractive shorter timeline would
now imply a general claim that the fictional source never made.

**Repair:** cross out only the silence. Preserve the qualification as the same
object in both tracks. At the payoff, compare the two complete word sequences.
The source supports a single speaker's account. Keep that boundary in the
elaboration and `must_not_imply`, even if the animator changes the visual style.

This is a deliberately authored failure example, not a report of a rendered
treatment or a controlled evaluation. The helper can find a missing word binding,
stale source or premature declared prerequisite. A reviewer still has to inspect
whether the actual picture broadens the claim.

## Adapt to your topic

Replace the fictional source, narration and audience question first. Preserve
each source's status: an interviewee's account is not independent proof; a code
read is not observed execution; an illustration is not experimental evidence.
Use the section count your explanation needs. Replace synthetic times with a
reviewed recording clock before claiming synchronization to actual speech.
