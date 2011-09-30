#!/bin/sh

. /etc/gwctl.conf
. $ROOT/common

subj=$1
chan=$2

gwctl_lock_wait "switch_${subj}" switch_script

###################################
#	SWITCH! =)
###################################
case "$subj" in
	inet)
		case ${chan} in
			isp1)
				# HOW TO SWITCH INET TO ISP1			
			;;
			isp2)
				# HOW TO SWITCH INET TO ISP2
			;;
		esac
	;;
	tunnel)
		case ${chan} in
			isp1)
				# HOW TO SWITCH TUNNEL TO ISP1					
			;;
			isp2)
				# HOW TO SWITCH TUNNEL TO ISP2							
			;;
		esac
	;;
	*)
		echo " [i] Doing nothing for subject other than default, see the switching script $0!"
	;;
esac

post_switching $subj $chan

gwctl_unlock "switch_${subj}" switch_script

exit 0
