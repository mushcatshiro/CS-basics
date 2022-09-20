[TOC]

# tmux

## Sessions

```bash
tmux new -s session-name # default tmux session -s 0
tmux a -t session-name
tmux ls
tmux kill-session -t session-name
<CR> d # detach
```

## Panes

````bash
<CR> % # vertical split
<CR> " # horizontal split

<CR> o # swap panes
<CR> q + pane-number # go to pane-number
<CR> x # kill pane
````