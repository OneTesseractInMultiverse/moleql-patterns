# Security Policy

## Supported Versions

This project follows semantic versioning.

Security fixes are provided for:
- The latest released minor version (e.g., `1.x`)
- The current development branch (`main`) until the next release

Older versions may not receive security updates. Upgrade to a supported version to receive fixes.

## Reporting a Vulnerability

If you believe you have found a security vulnerability, please report it responsibly.

### Preferred: Private disclosure (GitHub Security Advisories)
1. Go to the repository’s **Security** tab
2. Click **Report a vulnerability**
3. Provide the details requested below

### If private reporting is not available
Open an issue **only if** the report does not include sensitive details. Otherwise, contact the maintainer privately.

## What to Include

Please include as much of the following as possible:

- A clear description of the vulnerability and potential impact
- Steps to reproduce (proof-of-concept is helpful, but keep it safe)
- Affected versions, branches, and environments
- Any relevant logs, stack traces, or configuration details (remove secrets)
- Suggested mitigations or fixes (if you have them)

## Coordinated Disclosure

After receiving a report, we aim to:

- Acknowledge receipt within **7 days**
- Provide a status update as the issue is triaged
- Work on a fix and publish it in a patch release
- Credit reporters in release notes/advisories when requested

Timelines may vary depending on severity and complexity.

## Security Best Practices for Users

- Keep dependencies up to date (especially `pydantic` and related tooling)
- Pin dependencies for production use and update regularly
- Avoid storing secrets in source code or configuration committed to git
- Use least-privilege credentials and rotate secrets periodically

## Scope

This repository includes reusable patterns and base abstractions. It does not operate a hosted service.

Security reports should focus on:
- Incorrect validation or unsafe defaults in provided abstractions
- Issues that could lead to data exposure, privilege escalation, or remote code execution in applications using this library
- Supply chain risks related to packaging, releases, or CI configuration

Thank you for helping keep the project and its users safe.
