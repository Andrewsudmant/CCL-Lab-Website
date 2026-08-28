# Gate 5G placeholder and public-copy audit

Audit date: 28 August 2026

## Result

PASS for public content. The eight representative examples in `config/research_scope.yml` remain internal test/editorial examples. Every one now carries both `placeholder: true` and `public: false`; the schema requires both values. The generator never reads this field into a public page, and tests assert that none of the eight exact titles appears in rendered HTML.

No supported public section was filled with invented facts. Work source sections are omitted when a record has no external public source. Current Conversations remains intentionally “In development” rather than showing fixtures or invented entries. Opportunities truthfully states that no confirmed calls are open.

The bounded visible-text audit found no public `TBC`, `TBD`, lorem text, sample project or internal representative example. Form-help text uses visible “For example” guidance rather than placeholder attributes. Quarto’s own non-visible JavaScript configuration contains an internal property named `search-text-placeholder`; this is framework implementation, not page copy or unfinished content.
