# distributed system with message queue

goal is to learn the following items,

- docker compose/docker
- python rq

the system composes of 4 nodes, a frontend flask that takes records job to
redis queue, two rq worker that processes job(s) from queue and redis instance
as database.

## backlog

- [ ] separation of client and app
  - i.e. current commit client and app shares same project folder
  - workaround for namespace search
- [ ] remove rq connection hardcoding
- [ ] endpoint for job checking

## setup

with docker compose

```bash
>> pwd
# .../mq_dist
>> docker compose -d up
>> python -m venv venv
>> pip install -r requirements.txt
>> source venv/bin/python helper.py
```

> note CRLF and LF might screw up the setup. its probably first thing to look
> out for when encountering any random bug.