
do '../web-lib.pl';
&init_config();

sub module_install
{
# Setup miniserv to use this theme for mobile mode
local %miniserv;
&get_miniserv_config(\%miniserv);
if (!defined($miniserv{'mobile_preroot'})) {
	$miniserv{'mobile_preroot'} = "virtual-server-mobile";
	#$miniserv{'mobile_nosession'} = 1;
	$miniserv{'mobile_prefixes'} = "m. mobile.";
	&put_miniserv_config(\%miniserv);
	$gconfig{'mobile_theme'} = "virtual-server-mobile";
	&write_file("$config_directory/config", \%gconfig);
	&reload_miniserv();
	}
}


