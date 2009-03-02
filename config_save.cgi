#!/usr/local/bin/perl
# config_save.cgi
# Save inputs from config.cgi

require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
require './config-lib.pl';
&ReadParse();
$m = $in{'module'};
&error_setup($text{'config_err'});
&foreign_available($m) || &error($text{'config_eaccess'});
%access = &get_module_acl(undef, $m);
$access{'noconfig'} && &error($text{'config_ecannot'});

mkdir("$config_directory/$m", 0700);
&lock_file("$config_directory/$m/config");
&read_file("$config_directory/$m/config", \%config);

$mdir = &module_root_directory($m);
if (-r "$mdir/config_info.pl") {
	# Module has a custom config editor
	&foreign_require($m, "config_info.pl");
	local $fn = "${m}::config_form";
	if (defined(&$fn)) {
		local $pkg = $m;
		$pkg =~ s/[^A-Za-z0-9]/_/g;
		eval "\%${pkg}::in = \%in";
		$func++;
		&foreign_call($m, "config_save", \%config);
		}
	}
if (!$func) {
	# Use config.info to parse config inputs
	&parse_config(\%config, "$mdir/config.info", $m, undef, $in{'section'});
	}
&write_file("$config_directory/$m/config", \%config);
&unlock_file("$config_directory/$m/config");
&webmin_log("_config_", undef, undef, \%in, $m);
if ($in{'save_next'}) {
	&redirect("config.cgi?module=$in{'module'}&section=$in{'section_next'}");
	}
elsif ($m eq "virtual-server") {
	&redirect(&theme_use_iui() ? "/index.cgi" : "/index_templates.cgi");
	}
else {
	&redirect("/$m/");
	}

