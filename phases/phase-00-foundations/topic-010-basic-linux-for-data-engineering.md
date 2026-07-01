# Topic 010: Basic Linux For Data Engineering

## Goal

Learn the Linux commands that data engineers use to inspect files, debug jobs, move data, and understand running systems.

## Simple Explanation

Linux is the operating system behind many servers, data platforms, containers, and cloud workloads.

You do not need to be a Linux administrator on day one, but you must be comfortable navigating files, inspecting logs, checking processes, and using command-line tools.

## Core Idea

- Definition: Linux is a Unix-like operating system widely used for servers and data infrastructure.
- Why it matters: Most Big Data tools run on Linux servers or containers.
- Related terms: shell, terminal, file system, process, permissions, environment variables.

## Essential Commands

| Need | Command |
|---|---|
| show current directory | `pwd` |
| list files | `ls -lah` |
| change directory | `cd path` |
| view file | `less file` |
| print file | `cat file` |
| first lines | `head file` |
| last lines | `tail file` |
| follow logs | `tail -f app.log` |
| search text | `grep "error" app.log` |
| better search | `rg "error"` |
| count lines | `wc -l file` |
| disk usage | `du -sh path` |
| free disk | `df -h` |
| running processes | `ps aux` |
| stop process | `kill PID` |
| environment variable | `echo $PATH` |

## How It Is Used

Common data engineering tasks:

- inspect raw files before loading
- check pipeline logs
- verify file sizes
- test shell commands in Airflow tasks
- debug Spark driver or executor logs
- move files between local and cloud tools
- check environment variables and config

## Big Data / System Design Angle

Linux basics help you debug what dashboards hide.

Examples:

- A Spark job fails because the disk filled up.
- A pipeline fails because a file permission changed.
- A Kafka consumer cannot start because a port is already used.
- A scheduled job reads the wrong environment variable.

## Example

Inspect a CSV quickly:

```bash
head -5 orders.csv
wc -l orders.csv
rg "failed" orders.csv
du -sh orders.csv
```

Follow a pipeline log:

```bash
tail -f pipeline.log
```

## Common Mistakes

- Mistake: Opening huge files in a text editor.
- Better way: Use `head`, `tail`, `less`, `wc`, `rg`, and sampling.

- Mistake: Ignoring permissions.
- Better way: Check ownership and permissions with `ls -l`.

- Mistake: Running commands without knowing the working directory.
- Better way: Start with `pwd`.

## Interview Speak

"For data engineering, Linux is practical debugging muscle. I use it to inspect files, logs, disk, processes, permissions, and environment variables. Even when tools are managed, Linux helps diagnose failures at the system level."

## Quick Recall

- One-liner: Linux is where many data jobs actually run.
- Keywords: files, logs, processes.
- Trap: Trying to load or open huge files instead of sampling them.
