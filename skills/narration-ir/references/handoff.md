# From explanation plan to renderer

Give the animator the generated scene packet and its referenced source files.
The packet carries literal source excerpts in the beat, but source paths remain
relative to the original plan directory. Transfer that directory with the packet
when the worker needs to reopen the evidence. Supply the recording separately
when it is authorized and available; the packet contains no media.

Ask the animator to read the selected renderer's own guidance and reuse an
appropriate working scene or component. The global capability list records
what was inspected and tried. A name or clone path alone does not establish
that a component works. Record the chosen implementation and version in the
production project, along with each obligation it implements.

Example handoff:

> Animate beat b04 using this packet and the existing timeline component. Keep
> both tracks' words identical and preserve the qualification. Use the resolved
> event times on the same audio clock. Choose layout and motion that make only
> the silence removal visible. Return the implementation, preview and review
> evidence, and retain the packet's unresolved issues.

## Renderer adapters

- **Remotion:** convert seconds to frames using the composition's actual frame
  rate; bind local scene frames to the same output clock. Inspect frame rounding
  near the selected anchor. Use the renderer's current skill/docs for APIs.
- **Manim:** schedule the transition start and duration separately. A wait to a
  word followed by an animation implements onset timing, not settled timing.
- **Motion Canvas or an editor:** create named markers from the stable event
  IDs, preserving which word occurrence and transcript revision generated them.

These are handoff conventions, not bundled renderer integrations. Do not claim
that the example has been rendered by any of these tools.

If a new recording changes word occurrences, keep the meaning records for
review but invalidate the old schedule. Rebind the anchors, regenerate packets,
then review transitions and the whole audiovisual result. Moving a timestamp
alone cannot establish that an edited sentence has the same meaning.
