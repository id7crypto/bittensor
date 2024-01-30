#!/bin/sh

printf "Bittensor profiler, simply input the argument you'd give to btcli normally & it will get profiled, and dumped into profile.txt\n"

read -p "btcli " v1

# Run the profiler
pyinstrument -o profile -r text --show-all --from-path  btcli $v1