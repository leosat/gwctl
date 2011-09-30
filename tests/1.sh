#!/bin/sh

. /etc/gwctl.conf
. ${COMMON_SH_LIB}

#
# Locking test =)
#
[ "" ] && {
	{ 
		sleep 25
		pkill -f gwctl
	} &

	for i in 1 2 3 4 5 6 7
	do
		while :
		do
			gwctl_lock_wait TEST ${i} '' 1 || return 2
			echo " [i] "${i} LOCKED IT!
			sleep 0.2
			gwctl_unlock TEST ${i}
			sleep 0.2
		done &
	done
}

[ "" ] && {

#
#	TESTING! 
#
for chan in `conf_get_subject_channels_sorted_by_weight podolsk_tun`
do
	echo " $chan weight is "`subj_get podolsk_tun ${chan} weight`
done

conf_get_subject_channels_sorted_by_weight "inet"

}

