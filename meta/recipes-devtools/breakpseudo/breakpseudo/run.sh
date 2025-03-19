#!/bin/bash

D=$1

function run()
{
	for run in $(seq 10); do
	    ln -sf file ${D}/file2
	    ls -la ${D}/file2
	done
}

run &
run &
run &
run &
