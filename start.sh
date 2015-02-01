#!/bin/bash
echo "Starting port redirection"
socat -d -d pty,link=./.crossbar/pty1,raw,echo=1 pty,link=./.crossbar/pty2,raw,echo=1 &
echo "Use 'cat < ./.crossbar/pty2' to see virtualport output"
crossbar -d start --loglevel debug --logdir .

