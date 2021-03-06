#!/bin/bash

shred -uz *.pem

for arg in "$@"; do
	case $arg in 
		-k|--key)
			echo "starting key folder clean"
			shred -uz key/*.pem
			echo "key folder clean finished"
		;;
		-s|--session)
			echo "starting sessions folder clean"
			shred -uz sessions/*.session
			shred -uz sessions/*.session-journal
			echo "sessions folder clean finished"
		;;
		-e|--encode)
			echo "starting encode folder clean"
			shred -uz encode/*.bin
			echo "encode folder clean finished"
			;;
		-d|--decode)
			echo "starting decode folder clean"
			shred -uz decode/*.bin
			echo "decode folder clean finished"
		;;
		-a|--all)
			echo "starting full clean"
			shred -uz key/*.pem
			shred -uz sessions/*.session
			shred -uz sessions/*.session-journal
			shred -uz encode/*.bin
			shred -uz decode/*.bin
			echo "full clean finished"
		;;
	esac
done
