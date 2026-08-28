# Public voice and plain-language standard

## Voice

Write as identifiable researchers speaking to an interested public. Begin with the city, actor, decision or practical difficulty. Use `we` when it clarifies the lab's judgement, but vary paragraph openings. Prefer active verbs and sentences with one main idea.

## Structure

Put a concrete example before a dense conceptual explanation when it gives readers a reason to continue. Vary sentence length and page structure. Do not force different kinds of research into one template. Use no more than three abstract nouns in a series; split longer taxonomies or introduce them after a plain statement.

## Terms and qualifications

Explain specialist terms inline at first use using `config/plain_language_terms.yml`. The definition must work without a tooltip, glossary or JavaScript. Technical wording may follow where precision helps. State the material boundary near the claim, then keep detailed evidence and provenance lower on the page. Do not repeat the same warning in the paragraph, callout, metadata, badge and footer.

## Uncertainty

Keep `may`, `could` and `can` when they express real uncertainty. Remove ritual hedging, not substantive limits. Never convert a bounded or prospective statement into a finding.

## Patterns to challenge

Repeated contrast constructions—`does not by itself`, `not simply`, `not merely`, `rather than`, `while`, `yet` and `although`—are useful only when the contrast carries the argument. Avoid stock language such as `at the intersection of`, `critical role`, `robust framework`, `holistic`, `multifaceted`, `transformative`, `leverage`, `meaningful impact`, `unlock`, `navigate`, `cutting-edge`, `innovative solutions`, `evidence to action`, `scaling what works`, `this theme examines`, `this work seeks to`, `it is important to note` and `has important implications`.

## Review

Run `python scripts/audit_public_voice.py` after building. Treat its phrase counts, long-sentence list and term-order findings as prompts for editorial review, not automated proof of quality. Never rewrite copy automatically from the report. Pair the diagnostic with browser review and an editorial comprehension audit.
