---
tags: [skill-creator]
max_turns: 200
timeout_seconds: 3600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I put the Beijing multi-site air quality dataset from UCI (https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data) into data/raw/beijing-air/, I just unzipped what I downloaded. Make a new dataset pack `beijing-air` from it so the agent can answer questions about pollution and weather per station. I want to show in the thesis that the system works on a different IoT dataset than the bees.
