conf_get_one_of ( ) {
	local val
	while [ $# > 0 ]
	do
		if [ "$1" ]
		then
			req_var_name=$1
			eval val=\$$req_var_name
			if [ "$val" ]
			then
				echo "$val"
				return 0
			fi
			shift
		fi
	done
	return -1
}


c1=
c2=
c3=z

conf_get_one_of c1 c2 c3

