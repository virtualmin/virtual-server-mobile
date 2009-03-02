#!/usr/local/bin/perl
# config_save.cgi
# Save inputs from config.cgi

require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
require './config-lib.pl';
&ReadParse();
$m = $in{'module'};
&error_setup($text{'config_err'});
&foreign_available($m) || &error($text{'config_eaccess'});
&switch_to_remote_user();
&create_user_config_dirs();

mkdir("$user_config_directory/$m", 0700);
&lock_file("$user_config_directory/$m/config");
&read_file("$user_config_directory/$m/config", \%config);
&read_file("$config_directory/$m/canconfig", \%canconfig);

$mdir = &module_root_directory($m);
if (-r "$mdir/uconfig_info.pl") {
	# Module has a custom config editor
	&foreign_require($m, "uconfig_info.pl");
	local $fn = "${m}::config_form";
	if (defined(&$fn)) {
		local $pkg = $m;
		$pkg =~ s/[^A-Za-z0-9]/_/g;
		eval "\%${pkg}::in = \%in";
		$func++;
		&foreign_call($m, "config_save", \%config, \%canconfig);
		}
	}
if (!$func) {
	# Use config.info to parse config inputs
	&parse_config(\%config, "$mdir/uconfig.info", $m,
		      %canconfig ? \%canconfig : undef, $in{'section'});
	}
&write_file("$user_config_directory/$m/config", \%config);
&unlock_file("$user_config_directory/$m/config");

# Call any post-config save function
local $pfn = "${m}::config_post_save";
if (defined(&$pfn)) {
	&foreign_call($m, "config_post_save", \%config, \%oldconfig,
					      \%canconfig);
	}

if ($in{'save_next'}) {
	&redirect("uconfig.cgi?module=$in{'module'}&section=$in{'section_next'}");
	}
else {
	&redirect("/$m/");
	}

