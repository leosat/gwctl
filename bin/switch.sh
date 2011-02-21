#!/bin/sh

. /etc/gwctl.conf
. $ROOT/common

subj=$1
chan=$2

gwctl_lock_wait "switch_${subj}" switch_script

###################
# SWITCH! =)
#
case "$subj" in
	inet)
		case ${chan} in
			corbina)
				route change default 85.21.118.145
				ovpn_conf_set_local_ip_binding corbina.ariel.ru server.conf
				/etc/ovpn/ctl.sh restart server
			;;
			macomnet)
				route change default 213.247.232.145
				ovpn_conf_set_local_ip_binding macomnet.ariel.ru server.conf
				/etc/ovpn/ctl.sh restart server
			;;
		esac
	;;
	podolsk_tun)
		case ${chan} in
			macomnet)
				ovpn_conf_set_local_ip_binding macomnet.ariel.ru podolsk.conf
				/etc/ovpn/ctl.sh restart podolsk
			;;
			corbina)
				ovpn_conf_set_local_ip_binding corbina.ariel.ru podolsk.conf
				/etc/ovpn/ctl.sh restart podolsk
			;;
		esac
	;;
	kotelniky_tun)
		case ${chan} in
			macomnet)
				ovpn_conf_set_local_ip_binding macomnet.ariel.ru kotelniky.conf
				/etc/ovpn/ctl.sh restart kotelniky
			;;
			corbina)
				ovpn_conf_set_local_ip_binding corbina.ariel.ru kotelniky.conf
				/etc/ovpn/ctl.sh restart kotelniky
			;;
		esac
	;;
	kotelniky_italinox_tun)
		case ${chan} in
			macomnet)
				ovpn_conf_set_local_ip_binding macomnet.ariel.ru italinox.conf
				/etc/ovpn/ctl.sh restart italinox
			;;
			corbina)
				ovpn_conf_set_local_ip_binding corbina.ariel.ru italinox.conf
				/etc/ovpn/ctl.sh restart italinox
			;;
		esac
	;;
	www)
		case ${chan} in
			macomnet)
				route change default $macomnet_gw
			;;
			corbina)
				route change default $corbina_gw
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
