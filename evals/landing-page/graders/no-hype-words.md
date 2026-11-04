---
type: regex
pattern: "\\b(seamless|seamlessly|effortless|effortlessly|unlock|empower|elevate|supercharge|leverage|streamline|robust|cutting-edge|delve|game-changing)\\b"
flags: i
match: not_contains
target: { source: file, path: index.html }
---
