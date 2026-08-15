---
name: bookos
description: Turn books, book excerpts, reading notes, or transcripts into reusable knowledge systems instead of generic summaries. Use when the user asks to analyze, deconstruct, digest, study, remember, compare, or apply a book; build book notes, mental models, human-insight cards, action principles, review questions, or social-content ideas from reading; or explicitly asks for BookOS.
---

# BookOS

Transform reading material into a durable system for judgment, action, and retrieval.

## Ground the source

1. Identify the book, edition, source material, desired depth, and intended use from the request.
2. Use text, notes, excerpts, transcripts, or files supplied by the user as the primary source.
3. If the source is unavailable, distinguish clearly between a high-level analysis based on established knowledge and a source-grounded close reading. Do not invent quotations, page numbers, scenes, statistics, or author claims.
4. Ask one focused question only when the missing source, edition, or goal would materially change the result. Otherwise make a reasonable assumption and state it briefly.

## Choose the output depth

- **Quick scan:** thesis, structure, five insights, three actions, and five review questions.
- **Deep decomposition:** full BookOS workflow below.
- **Database entry:** compact, atomic insight cards designed for later retrieval.
- **Content conversion:** create a social post only after the analytical layer is sound.

Use deep decomposition by default when the user asks to “拆书”, “深度拆解”, or build a knowledge system.

## Run the BookOS workflow

1. State the book's one-sentence central claim.
2. Map the argument or narrative logic. Show how the main parts connect rather than listing chapters mechanically.
3. Extract five to ten transferable models. For each, explain the mechanism, boundary conditions, and one concrete example.
4. Separate evidence from interpretation:
   - what the author argues;
   - what evidence or story supports it;
   - what is inferred;
   - what deserves skepticism.
5. Extract human patterns when relevant: incentives, fear, identity, status, self-deception, power, trust, and repeated behavior.
6. Translate insights into the user's stated domains, such as business, management, investing, relationships, learning, or personal decisions. Do not force every domain when the connection is weak.
7. Produce action principles. Make each principle specific enough to change a decision or behavior.
8. Create atomic insight cards and spaced-review questions using the schema in `references/bookos-schema.md`.
9. End with a short “what to remember” section containing only the highest-value ideas.

## Preserve rigor

- Prefer mechanisms over slogans and examples over vague praise.
- Keep quotations short and only quote wording present in the supplied source or verified material.
- Label disagreement and uncertainty plainly.
- Avoid padding the result with generic biography or chapter-by-chapter recap.
- Do not pretend to have read a source that was not supplied or retrieved.
- Match the language and level of the user.

## Use the reference schema

Read `references/bookos-schema.md` when producing a deep decomposition, database entry, reusable Markdown note, comparison, or social-content derivative. Select only the sections that serve the request; do not force the entire template into a quick answer.

## Convert into content

When the user asks for a post, script, newsletter, or Xiaohongshu-style draft:

1. Choose one surprising or high-leverage insight from the completed analysis.
2. Open with a concrete tension, mistake, or changed judgment.
3. Explain the idea with one example.
4. Add the user's reaction or application without fabricating personal experience.
5. Close with one useful action or question.

Treat content as a derivative of the knowledge system, not a replacement for it.
