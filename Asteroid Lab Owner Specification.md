
# Asteroid Lab Owner Specification

## Contents

i. Introduction

ii. Key Design Decisions

iii. Rules Specification

iv. Default Owner Configuration File

## I. Introduction

In volunteering to support Asteroid Lab, Node Owners (where a Node is a single physical machine) will host one or more Docker containers upon their Node.  This specification exists to define the API through which Node Owners restrict resource access to said containers.

## II. Key Design Decisions

### Usability

- Owners will describe restrictions by populating the Owner Config File (OCF)--a YAML file describing configuration rules.  Owner interaction ends here.
- Owners will be provided with a default OCF, in the event that they do not wish to customize resource access.
- Except for the `bandwidth-limit` rule, rules outlined in the OCF apply individually to each container rather than to all containers on the machine in aggregate. For example, setting `memory: 4g` in this file means that any one Docker container can use up to 4 gigabytes of memory, but gives no guarantees to the memory used by all Docker containers running on this machine. This is primarily due to the limitations of Docker settings and the difficulty of predicting what processes will be run on the host machine.
- The specific format and structure of the OCF are detailed later in this document.

### Semantics

- As implied in the introduction, there exists exactly one OCF per physical machine (i.e. Node).
- If two conflicting rules exist (e.g. exposing and blocking the same port), they are applied in order of appearance.  That is, a later rule will override the portions of earlier rules it conflicts with. **TODO** Add an example.
- Attempts to parse a document with the following will at some point throw an error:
    - Missing required fields.
    - Missing subfields which are required if the parent field exists (example: the `protocol` specification in a `hostname` rule).
- The following will be ignored:
    - Misspelled/unrecognized fields.

## III. Rules Specification

### Metadata

---

**`version: <version number>`**

*The version of Asteroid Lab this file is meant for.*

- **Required**
- Default: the latest version we have.
- Example: `version: 0.0.0`

### Hardware Resources

---

**`cpus: <cpu count>`**

_The maximum number of CPU cores' resources available to each container._

- **Optional**
- `<cpu count>`:  decimal number. The number of CPU cores.
- Default: allow containers to use all available CPUs (Docker default).
- Example:  `cpus: 2.5`
    - Allows a container to use up to 2.5 cores' worth of resources.

---

**`cpuset-cpus: <cpu indices>`**

_Which CPU cores are available to a container._

- **Optional**
- `<cpu indices>`:  comma- or hyphen-separated list of integers; space-separated lists. The zero-indexed indices of CPU cores.
- Default: Allow containers to see and use all CPU cores (Docker default).
- Example:  `cpuset-cpus: 0,5 1-3`
    - Allows a container to use up to cores #0, #1, #2, #3, and #5.

---

**`memory: <allocation limit>`**

_The maximum amount of memory a container can use._

- **Optional**
- `<allocation limit>`: Amount of memory allowed, represented as an integer followed by `b`, `k`, `m`, or `g`. Limit must be more than `4m` (4 megabytes) if specified.
- Default: Any container can use all available memory (Docker default).
- Example: `memory: 4g`
    - Allows any one container to use up to 4 gigabytes of memory on the host machine.

### Networking Resources

---

```
bandwidth-limits:
    upload: <upload limit>
    download: <download limit>
```

_The target bandwidth for all containers combined._

- **Optional** 
- `<upload limit>`, `<download limit>`: bandwidth in kbps.
- Default if not present: containers can use all available bandwidth. If `bandwidth-limits` is specified, **both** `upload` and `download` must be specified.
- Limits must be greater than 0 if specified.
- Example:
```yaml
bandwidth-limits:
    upload: 1000
    download: 1000
```

---

**`ip-rules: <rules>`**

_Packet-handling behavior for packets destined for certain IP addresses._

- **Optional**
- `<rules>`: YAML-formatted list of rules for packets going to/from IP addresses.
- Default if not present: No rules.
- Rule formatting:
    - `ip` (required): IP address.
    - `protocol` (required): `tcp`, `udp`, `icmp`, `ip`.
    - `port` (optional, default: `any`): can be ports, static port definitions, ranges, and can have negation.
    - `behavior` (required): `alert`, `log`, `pass`, `activate`, `dynamic`, `drop`, `reject`, `sdrop`. See Snort manual for descriptions of each type.
    - `direction` (required): `to` (applies only to packets going to the specified IP address), `from` (applies only to packets coming from the specified IP address), `both`.
    - `log` (optional, default: `false`): `true`, `false` (false if not present).
    - `logfile` (optional, default: none): file to log to, relative to working directory of machine (no effect if `log` is false).
    - `snort-options` (optional, default: none): Snort options, in parens and surrounded by single quotes. These will be pasted directly into the `local.rules`.
- Example:
```yaml
ip-rules:
    - ip: 216.58.192.14
      protocol: tcp
      port: !1:1024 (applies to all ports except those between 1 and 1024)
      behavior: drop
      direction: to
      log: true
      logfile: log.txt (will be stored on host filesystem)
```

---

**`hostname-rules: <rules>`**

_Packet-handling behavior for packets destined for certain hostnames._

- **Optional**
- `<rules>`: YAML-formatted list of rules.
- Default if not present: No rules.
- Rule formatting:
    - `host` (required): hostname.
    - `protocol` (required): `tcp`, `udp`, `icmp`, `ip`.
    - `behavior` (required): `alert`, `log`, `pass`, `activate`, `dynamic`, `drop`, `reject`, `sdrop`. See Snort manual for descriptions of each type.
    - `port` (optional, default: `any`): can be ports, static port definitions, ranges, and can have negation.
    - `direction` (required): `to` (applies only to packets going to the specified IP address), `from` (applies only to packets coming from the specified IP address), `both`.
    - `log` (optional, default: `false`): `true`, `false` (false if not present).
    - `logfile` (optional, default: none): file to log to, relative to working directory of machine (no effect if `log` is false).
    - `snort-options` (optional, default: none): Snort options, in parentheses and surrounded by single quotes. These will be pasted directly into the `local.rules`, so it's important that they be formatted correctly. It is recommended that you set the `gid` on your rules, starting from 200000 (100000 - 199999 are reserved for Asteroid-lab generated options).
- Example:
```yaml
hostname-rules:
    - host: google.com
      protocol: tcp
      port: !1:1024 (applies to all ports except those between 1 and 1024)
      behavior: drop
      direction: to
      log: true
      logfile: log.txt (will be stored on host filesystem)
      snort-options: '(msg:"test google.com"; pcre:"(/.*\google.com/i"; sid: 100003; rev:1;)'
    - host: qq.com
      protocol: udp
      behavior: drop
      direction: from
```

## IV. Default Owner Configuration File

```yaml
version: 0.0.0
```
