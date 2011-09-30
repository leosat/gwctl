#!/bin/sh

ROOT=/gwctl

tar -czvf $ROOT/misc/gwctl_dist.tgz \
	--exclude "*tgz" \
	--exclude "*conf.local" \
	--exclude "*var/*" \
	--exclude "*tmp/*" \
		$ROOT/
