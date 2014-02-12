#!/bin/bash

NUM_CHRS=5 # 5
NUM_LOCS=21 #21
NUM_STAGES=20 #20
INPUT_FILES="min-eq.coor,1 min-eq.vel,1 min-eq.xsc,1 \
sys.pdb,1 sys.crd,1 sys.parm,1"
PREFIX=$PWD/data

conf_dir="$PREFIX/dyn-conf-files"
mkdir -p $conf_dir
for conf in `seq 0 \`expr $NUM_STAGES - 1\``; do
	dd if=/dev/urandom of=$conf_dir/dyn$conf.conf bs=1k count=1
done

for chr in `seq 0 \`expr $NUM_CHRS - 1\``; do
	for loc in `seq 0 \`expr $NUM_LOCS - 1\``; do
		dir="$PREFIX/$chr/$loc"
		mkdir -p $dir

        for i in $INPUT_FILES; do

            name="${i%,*}"
            size="${i#*,}"

            file=$dir/$name
			if [ $chr -eq 0 -a $loc -eq 0 ]; then
				dd if=/dev/urandom of=$file bs=1m count=$size
			else
				ln -s $PREFIX/0/0/$name $file
			fi
        done;

	done
done
