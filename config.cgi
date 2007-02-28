#!/usr/local/bin/perl
# Display a form for editing the configuration of a module, one section at
# a time.

require './web-lib.pl';
require './config-lib.pl';
require './ui-lib.pl';
&init_config();
%text = &load_language($current_theme);
&ReadParse();
$m = $in{'module'} || $ARGV[0];
&foreign_available($m) || &error($text{'config_eaccess'});
%access = &get_module_acl(undef, $m);
$access{'noconfig'} &&
	&error($text{'config_ecannot'});
%module_info = &get_module_info($m);
if (-r &help_file($m, "config_intro")) {
	$help = [ "config_intro", $m ];
	}
else {
	$help = undef;
	}
&ui_print_header(&text('config_dir', $module_info{'desc'}),
		 $text{'config_title'}, "", $help, 0, 1,
		 $m eq "virtual-server" ? 1 : 0);
$mdir = &module_root_directory($m);

# Read the config.info file to find sections
&read_file("$mdir/config.info", \%info, \@info_order);
foreach $i (@info_order) {
	@p = split(/,/, $info{$i});
	if ($p[1] == 11) {
		push(@sections, [ $i, $p[0] ]);
		}
	}
if (@sections > 1 && &get_webmin_version() >= 1.295) {
	# We have some .. show a menu to select
	$in{'section'} ||= $sections[0]->[0];
	print &ui_form_start("config.cgi");
	print &ui_hidden("module", $m),"\n";
	print $text{'config_section'},"\n";
	print &ui_select("section", $in{'section'}, \@sections);
	print &ui_submit($text{'config_change'});
	print &ui_form_end(),"<p>\n";
	($s) = grep { $_->[0] eq $in{'section'} } @sections;
	$sname = " ($s->[1])";
	}

print &ui_form_start("config_save.cgi", "post");
print &ui_hidden("module", $m),"\n";
print &ui_hidden("section", $in{'section'}),"\n";
if ($s) {
	# Find next section
	$idx = &indexof($s, @sections);
	if ($idx == @sections-1) {
		print &ui_hidden("section_next", $sections[0]->[0]);
		}
	else {
		print &ui_hidden("section_next", $sections[$idx+1]->[0]);
		}
	}
print &ui_table_start(&text('config_header', $module_info{'desc'}).$sname,
		      "width=100%", 2);
&read_file("$config_directory/$m/config", \%config);

if (-r "$mdir/config_info.pl") {
	# Module has a custom config editor
	&foreign_require($m, "config_info.pl");
	local $fn = "${m}::config_form";
	if (defined(&$fn)) {
		$func++;
		&foreign_call($m, "config_form", \%config);
		}
	}
if (!$func) {
	# Use config.info to create config inputs
	&generate_config(\%config, "$mdir/config.info", $m, undef, undef,
			 $in{'section'});
	}
print &ui_table_end();
print &ui_form_end([ [ "save", $text{'save'} ],
		     $s ? ( [ "save_next", $text{'config_next'} ] ) : ( ) ]);

if ($m eq "virtual-server") {
	&ui_print_footer("/index_templates.cgi", $text{'config_return'});
	}
else {
	&ui_print_footer("/$m", $text{'index'});
	}

