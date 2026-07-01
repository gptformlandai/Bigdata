# Topic 007: Encoding

## Goal

Understand how characters and values become bytes that computers can store, transmit, and decode correctly.

## Simple Explanation

Computers store bytes, not letters.

Encoding is the agreement that says which bytes mean which characters. If two systems disagree on encoding, text becomes corrupted.

Example:

```text
letter A -> byte value 65 in ASCII/UTF-8
```

## Core Idea

- Definition: Encoding maps information, especially text, into bytes using a known standard.
- Why it matters: Data pipelines move bytes across files, APIs, queues, databases, and networks.
- Related terms: ASCII, UTF-8, Unicode, Base64, binary, charset.

## Common Encodings

| Encoding | What It Is | Common Use |
|---|---|---|
| ASCII | old 7-bit English character encoding | simple legacy text |
| Unicode | universal character set | global text representation |
| UTF-8 | variable-width Unicode encoding | most modern data systems |
| Base64 | encodes binary as text | sending binary through text-only systems |

## How It Is Used

Encoding appears when:

- reading CSV files
- parsing JSON
- sending HTTP responses
- writing logs
- storing multilingual text
- moving binary files through APIs

Most modern systems should default to UTF-8 unless there is a specific reason not to.

## Big Data / System Design Angle

Encoding bugs are annoying at small scale and expensive at Big Data scale.

Common symptoms:

- broken characters
- failed parsing jobs
- mismatched byte lengths
- corrupt files
- search/indexing problems

Example: customer names, addresses, and product titles may contain non-English characters. A pipeline that assumes ASCII can break or silently corrupt them.

## Example

```python
text = "data"

encoded = text.encode("utf-8")
decoded = encoded.decode("utf-8")

print(encoded)
print(decoded)
```

Output:

```text
b'data'
data
```

## Common Mistakes

- Mistake: Assuming text is always ASCII.
- Better way: Use UTF-8 by default.

- Mistake: Confusing encoding with encryption.
- Better way: Encoding is representation; encryption is security.

- Mistake: Using Base64 to "secure" data.
- Better way: Base64 is reversible formatting, not protection.

## Interview Speak

"Encoding is how text or binary values are represented as bytes. In data systems I would standardize on UTF-8, validate input encoding, and be careful when moving data between files, APIs, and databases because encoding mismatches can corrupt text or break parsing."

## Quick Recall

- One-liner: Encoding is the byte agreement for representing data.
- Keywords: UTF-8, bytes, decode.
- Trap: Treating Base64 as encryption.
