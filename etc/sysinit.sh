#!/bin/sh

. /etc/gwctl.conf

(
	$SWITCH_SCRIPT office_tun realcom
	$SWITCH_SCRIPT www rmt
	$GWCTLD_RC_SCRIPT restart
) &
