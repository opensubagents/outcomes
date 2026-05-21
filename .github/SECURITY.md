# Security policy

## Supported versions

Open Outcome is at **v0.1.0** and the spec is **Experimental**
(see [MATURITY.md](../MATURITY.md)). Only the most recent minor release is
supported for security fixes; older releases will not receive backports
until the spec reaches **Stable**.

## Reporting a vulnerability

If you believe you have found a security vulnerability in any part of this
project (the specification, the JSON schemas, the reference SDKs, or any
example code), please report it privately.

- **Preferred:** email the founding maintainer at `admin@jadecli.com`.
- Use the subject line prefix `[security] open-outcome:`.
- Include the affected component, a description of the issue, steps to
  reproduce if applicable, and any suggested mitigation.

We will acknowledge receipt within **3 business days** and aim to provide
a substantive response within **14 days**.

## Scope

The reference SDKs are not yet hardened for use against adversarial input;
the v0.1 threat model assumes the report being verified comes from a
cooperative agent runtime. Reports of denial-of-service through crafted
input are in scope but lower priority than correctness bugs in the spec
itself or the schemas.

## Public disclosure

Once a fix is available, we will publish a security advisory via the GitHub
Security Advisories tab on this repository. Credit will be given to the
reporter unless they request otherwise.
