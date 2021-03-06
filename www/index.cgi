#!/bin/sh

. /etc/gwctl.conf
. $COMMON_SH_LIB

AUTO_RELOAD_SEC=1 AUTO_REFRESH_SEC=25 SUBJ=default 
LINE="<u>-----------------------------------------------------------------------------------</u>"

COMMENT_DIV_DEF_BG=#FFFFE6

parse_uri ${QUERY_STRING} 5

check_gwctld_is_running ( ) {
	[ ! -r $DMNPIDF -o -z "`ps ax | grep gwctld | grep -v grep`" ] && 
		echo "<h1><font color=red>gwctld DAEMON IS NOT RUNNING!!! <br/>EXITING...</font></h1>" && {
		print_footer
		exit 0
	}
}

ch_auto_sw ( ) {
	[ "$GET_VAL" = "DISABLE" ] &&
		val="1"
	setbuf $DMN_IN "SET_VAR_${GET_SUBJ}_void_in_automode=$val"
	read_runtime_conf
}

print_footer ( ) {
	echo "</body></html>"
}

print_info( ) {
	echo "<pre>"
	echo "UPTIME: `uptime`"
	echo "-------------------------------"
	echo
	for subj in $subjects
	do
		C_CHAN=`get_runtime_conf ${subj}_active_channel`
		P_CHAN=`get_runtime_conf ${subj}_pending_channel`
		echo "Current active channel for subject $subj is: <span style=\"background:yellow;font-weight:;padding: 2px\">${C_CHAN}</span>"
		echo "Pending channel is: $P_CHAN"
		echo --------
	done
	echo
	echo LAST RECORDS FROM LOG:
	tail -n 50 $DMNLOGF | sed -E '
		s/\[(i)\]/<span style="background:lightblue">[\1]<\/span>/;
		s/\[(f?e)\]/<span style="background:lightred">[\1]<\/span>/;
		s/\[(e|w)\]/<span style="background:indianred">[\1]<\/span>/;
		s/\[(.?d)\]/<span style="background:lightgreen">[\1]<\/span>/;
		s/(--->)/<span style="background:lightgrey;border: outset 0px; font-size: 0.8em;">\1<\/span>/g;
		s/(----+)/<span style="background:lightgrey">\1<\/span>/;
		s/(>>>.*<<<)/<span style="background:#006699;color:lightyellow">\1<\/span>/;
		s/(locked)/<span style="background:#555555;color:lightyellow">\1<\/span>/;
		s/(I.m in automode)/<span style="background:#CC9966;">\1<\/span>/;
		s/(alive!)/<span style="background:lightgreen;">\1<\/span>/;
	'
	
        printf "\n$LINE\n\n"
	ifconfig
        printf "\n$LINE\n\n"
	netstat -rn
	echo ...
	echo "</pre>"
}

print_bg_color ( ) {
        if [ $P_CHAN = "$1" ]; 
	then
                echo "#FFcc99";
        elif [ $C_CHAN = "$1" ]; 
	then
                echo "lightgreen;"
        else
                echo "$COMMENT_DIV_DEF_BG;"
        fi
}

print_main_menu ( ) {

	echo "
		<div style='border:outset 2px; padding: 4px; width:75%; height:px; background:#bababa'>
		<div style='border:dashed 1px; padding:4px; width:99%; height:20px;background:lightblue '>
		<b>ACTION MENU : the gateway control for <i>`hostname`</i></b>
		</div><br/>
	"

	QUERY_STR="<a href='$SCRIPT_NAME?DO=INFO'>������ ����������.</a>"

	echo "&bull; "$QUERY_STR

	echo "<hr/>"

	for subj in $subjects
	do
		C_CHAN=`get_runtime_conf ${subj}_active_channel`
		P_CHAN=`get_runtime_conf ${subj}_pending_channel`
	
		echo "<div style='background:lightgrey;border: outset 1px;padding:2px'>"

		if [ `conf_get "$subj" "" void_in_automode` -o "`get_runtime_conf ${subj}_void_in_automode`" ]
		then
			# echo " +++++++++  `get_runtime_conf ${subj}_void_in_automode` || "
			subj_void_in_automode="1"
			echo "
				<span style='color:darkred;font-weight:bold;font-size:0.8em'>
					( MANUAL SWITCH ONLY )</span>
				`conf_get $subj "" desc`
				(\"<b>$subj</b>\")"
			if [ -z `conf_get "$subj" "" no_www_control` ]
			then
				echo "<br/>&nbsp;&nbsp;<a href='$SCRIPT_NAME?DO=CH_AUTO_SW&SUBJ=$subj&VAL=ENABLE' style=font-size:10pt>Enable switching in automode</a>"
			fi
		else
			subj_void_in_automode=""
			echo "
				`conf_get $subj "" desc`
				(\"<b>$subj</b>\")"
			if [ -z `conf_get "$subj" "" no_www_control` ]
			then
				echo "<br/>&nbsp;&nbsp;<a href='$SCRIPT_NAME?DO=CH_AUTO_SW&SUBJ=$subj&VAL=DISABLE' style=font-size:10pt>Disable switching in automode</a>"
			fi
		fi

		echo "</div>"
		echo "<blockquote>"

		for chan in $channels
		do
			weight=`conf_get "$subj" "$chan" weight`
			if [ "$weight" ]
			then
				echo "<div class=\"comment_div\" style='background:`print_bg_color $chan`'>"
				echo "&nbsp;Ch. "
				if [ `conf_get "$subj" "" no_www_control` ]
				then
					echo "$chan"
				else
					echo "<a href='$SCRIPT_NAME?DO=CH_SUBJ_CHAN&SUBJ=$subj&CHAN=$chan'>$chan</a>"
				fi
				echo "( `conf_get $subj $chan desc` pri=$weight ) "
				echo "</div>"
			fi
		done
		echo "</blockquote>"
	done

	echo "<hr/>"
	echo "</div>"
}

print_html_head ( ) {
	echo "<!DOCTYPE html>
	<html>
	<head>
		<title>Control for $WWW_IFACE_HOSTNAME</title>
		<style>
			.comment_div {
				background: $COMMENT_DIV_DEF_BG;
				border: dashed 1px orange;
			}
			a { color: blue; text-decoration: none}
		</style>
		<script lang=JavaScript>
			function countDown(sec, elid) {
	
				element = document.getElementById(elid)
	
	                        if ( element.textContent ) {
					element.textContent = sec;
				} else {
					element.innerText = sec;
				}
	
				if ( sec > 0 ) {
		                        sec--;
		                        setTimeout(\"countDown(\"+sec+\",'\"+elid+\"')\",1000);
				}
	
	                        return 0;
			}
		</script>
	"

	if [ "$GET_CONFIRM" ] &&
		[ 	"$GET_DO" = "CH_MODE_MANUAL" -o \
			"$GET_DO" = "CH_MODE_AUTO" -o \
			"$GET_DO" = "CH_AUTO_SW" -o \
			"$GET_DO" = "CH_SUBJ_CHAN" \
		]
	then
		echo "
			<meta http-equiv=\"refresh\" content=\"${AUTO_RELOAD_SEC};url=${SCRIPT_NAME}\"/>
		"
	elif in_automode
	then
		echo "
			<meta http-equiv=\"refresh\" content=\"${AUTO_REFRESH_SEC}\"/>
		"
	fi

	echo "
		</head>
		<body style='background:white;font-family: Verdana, sans-serif'
		        onload='countDown(${AUTO_REFRESH_SEC},\"refersh_sec_el\")'>
	"
}

print_reload_page_html ( ) {
	print_html_head $AUTO_RELOAD_SEC
	echo "<a href="${SCRIPT_NAME}">Reload the page</a> (auto reload in $AUTO_RELOAD_SEC seconds)"
	print_footer
	exit 0
}

#################################### GO! ##############################################

#
# Output HTTP header
#
echo "content-type: text/html; charset=koi8-r"
echo ""

#
# Then start doing useful things...
#
read_runtime_conf 
check_gwctld_is_running

#
# If we need to do something, ask for the action confirmation first.
#
case "$GET_DO" in
	CH_*)
		[ -z "$GET_CONFIRM" ] && {
			print_html_head
			echo "<h2><a href='$SCRIPT_NAME?$QUERY_STRING&CONFIRM=OK'> [q] ����������, ������� ��� �������������.</a></h2>"
			print_footer
			exit 0
		}
	;; 
esac

#
# Check if some changes require interface reload
#
[ "$GET_DO" = "CH_MODE_MANUAL" ] && {
	setbuf $DMN_IN "SET_MODE_MANUAL"
	print_reload_page_html
}

[ "$GET_DO" = "CH_MODE_AUTO" ] && {
	setbuf $DMN_IN "SET_MODE_AUTO"
	print_reload_page_html
}

[ "$GET_DO" = "CH_AUTO_SW" ] && {
	ch_auto_sw
	print_reload_page_html
}

[ "$GET_DO" = "CH_SUBJ_CHAN" ] && {
	echo "CH_CHAN_${GET_SUBJ}@${GET_CHAN}" > $DMN_IN
	echo "<p/><h2>$QUERY_STR</h2>"
		{
			echo "Manually switched ${GET_SUBJ} to channel ${GET_CHAN}" |
			mail -s "`hostname`: Manually switching ${GET_SUBJ} to another link." \
				unix-admins@ariel.ru
		} &
	print_reload_page_html
}

#
# Changes that do not require inerface reload
#
if in_automode 
then
	print_html_head
	echo "<h2>OK =). The system is in <font color=red>auto mode</font>. (page autorefresh in
			<span id='refersh_sec_el' name='refersh_sec_el'>${AUTO_REFRESH_SEC}</span>
		 seconds)
		</h2>
		<a href="?DO=CH_MODE_MANUAL">Disable automode globally (...if needed)</a><br/>
		<p/>
		" 
else
	print_html_head
	echo "
		<h2>The system is in <font color=red>manual mode (no autoswithching done!)</font>.
		<br/>
		<a href="?DO=CH_MODE_AUTO">Recommended: enable automode. </a>
		</h2>
		<p/>
	" 
fi

case $GET_DO in
	INFO)
		print_main_menu
		print_info
	;;
	*)
		print_main_menu
		[ $GET_DO ] &&
			echo "<p/>No such action!"
	;; 
esac

print_info 
print_footer 
exit 0
