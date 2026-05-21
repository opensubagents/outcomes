---
title: Types
description: Primitive value types used across the Open Outcome specification.
---

# Types

This document defines the primitive value types referenced by the normative
sections. Each type has both a wire form (the JSON representation used in
schemas) and a recommended in-memory representation in the reference SDKs.

## `string`

A non-empty Unicode string unless otherwise noted. Empty strings **MUST NOT**
be used where a non-empty string is required.

## `URI`

A string conforming to [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986).
In JSON Schemas, this is `{"type": "string", "format": "uri"}`. Reference
SDKs validate URIs with their language-native URL types
(`pydantic.HttpUrl` in Python, `URL` in TypeScript).

## `date`

A calendar date in ISO 8601 / RFC 3339 form (`YYYY-MM-DD`). In JSON Schemas,
this is `{"type": "string", "format": "date"}`. The date represents the
date the value applies to; it does not carry a time or timezone.

## `Confidence`

An enum drawn from the closed set `{"high", "medium", "low"}`. The
calibration meaning of each value is normative and defined in
[section 5](./sections/05-confidence.md).

## `SourceKind`

An enum drawn from the closed set `{"primary", "secondary", "community"}`.
See the [Source kind glossary entry](./glossary.md#source-kind).

## `Score`

An integer in the closed range `[1, 5]` representing a dimension score in
a [verdict](./sections/03-verdict.md). The score scale is normative; the
labels (e.g. "1 = unacceptable, 5 = excellent") are informative and may
vary by [dimension](./glossary.md#dimension).

## `SpecVersion`

A string conforming to [Semantic Versioning](https://semver.org/) (e.g.
`"0.1.0"`). The current spec version is recorded in
[`specification/README.md`](./README.md) and emitted on every
[verdict](./sections/03-verdict.md).
