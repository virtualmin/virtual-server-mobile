#!/usr/local/bin/perl
# Show a menu of options (list domains, create domains, webmin)

require './web-lib.pl';
&init_config();
require './ui-lib.pl';
%text = &load_language($current_theme);

$hostname = &get_display_hostname();
$ver = &get_webmin_version();
&get_miniserv_config(\%miniserv);
if ($gconfig{'real_os_type'}) {
	if ($gconfig{'os_version'} eq "*") {
		$ostr = $gconfig{'real_os_type'};
		}
	else {
		$ostr = "$gconfig{'real_os_type'} $gconfig{'real_os_version'}";
		}
	}
else {
	$ostr = "$gconfig{'os_type'} $gconfig{'os_version'}";
	}

# Do we have Virtualmin?
if (&foreign_available("virtual-server")) {
	# Yes .. what can we do?
	$hasvirt = 1;
	&foreign_require("virtual-server", "virtual-server-lib.pl");
	%minfo = &get_module_info("virtual-server");
	$title = $gconfig{'nohostname'} ? $text{'vmain_title2'} :
		&text('vmain_title', $minfo{'version'}, $hostname, $ostr);
	}
else {
	# Just show Webmin title
	$title = $gconfig{'nohostname'} ? $text{'main_title2'} :
			&text('main_title', $ver, $hostname, $ostr);
	}
&ui_print_header(undef, $title, "", undef, undef, 1, 1);

if ($hasvirt) {
	# Check licence
	print &virtual_server::licence_warning_message();

	# See if module config needs to be checked
	if (&virtual_server::need_config_check() &&
	    &virtual_server::can_check_config()) {
		print &ui_form_start("virtual-server/check.cgi");
		print "<b>$virtual_server::text{'index_needcheck'}</b><p>\n";
		print &ui_submit($virtual_server::text{'index_srefresh'});
		print &ui_form_end();
		}

	# List Virtualmin domains
	print "<form action=index_edit.cgi>\n";
	print "<ul>\n";
	print "<li><a href='index_list.cgi'>$text{'index_vmenu'}</a><br>\n";

	# Modify domains
	@configdoms = grep { &virtual_server::can_config_domain($_) }
			   &virtual_server::list_domains();
	if (@configdoms) {
		print "<li><a href='virtual-server/index.cgi'>$text{'index_vindex'}</a><br>\n";
		}

	# Configure a domain
	print "<li>$text{'index_vedit'} ",&ui_textbox("search", undef, 15)," ",
	      &ui_submit($text{'index_veditok'}),"<br>\n";

	# Create server
	if (&virtual_server::can_create_master_servers() ||
	    &virtual_server::can_create_sub_servers()) {
		($dleft, $dreason, $dmax) = &virtual_server::count_domains(
						"realdoms");
		($aleft, $areason, $amax) = &virtual_server::count_domains(
						"aliasdoms");
		if ($dleft == 0) {
			# Cannot add
			}
		elsif (!&virtual_server::can_create_master_servers() &&
		       &virtual_server::can_create_sub_servers()) {
			# Can just create own sub-server
			push(@clinks, "<a href='virtual-server/domain_form.cgi'>$text{'index_vaddsub'}</a>");
			}
		elsif (&virtual_server::can_create_master_servers()) {
			# Can create master or sub-server
			push(@clinks, "<a href='virtual-server/domain_form.cgi'>$text{'index_vadddom'}</a>");
			}
		if ((&virtual_server::can_create_sub_servers() ||
		     &virtual_server::can_create_master_servers()) && $dleft &&
		    $virtual_server::virtualmin_pro) {
			# Can create from batch file
			push(@clinks, "<a href='virtual-server/mass_create_form.cgi'>$text{'index_vaddmass'}</a>");
			}
		if (&virtual_server::can_import_servers()) {
			# Can import server
			push(@clinks, "<a href='virtual-server/import_form.cgi'>$text{'index_vimport'}</a>");
			}
		if (&virtual_server::can_migrate_servers()) {
			push(@clinks, "<a href='virtual-server/migrate_form.cgi'>$text{'index_vmigrate'}</a>");
			}
		if (@clinks) {
			print "<li>$text{'index_vcreate'}\n";
			print join(" | ", @clinks),"<br>\n";
			}
		}

	# System settings
	if (&virtual_server::can_edit_templates()) {
		print "<li><a href='index_templates.cgi'>$text{'index_vtemplates'}</a><br>\n";
		}

	# Backup / restore
	if (&virtual_server::can_backup_domains()) {
		print "<li>$text{'index_vbackup'}\n";
		print "<a href='virtual-server/backup_form.cgi'>$text{'index_vbackup1'}</a> |\n";
		print "<a href='virtual-server/backup_form.cgi?sched=1'>$text{'index_vbackup2'}</a> |\n";
		print "<a href='virtual-server/restore_form.cgi'>$text{'index_vbackup3'}</a><br>\n";
		}

	# System or account information
	print "<li><a href='index_sysinfo.cgi'>$text{'index_vsysinfo'}</a><br>\n";

	print "</ul>\n";
	print "</form>\n";
	}

# Show links to Webmin module categories
print "<p><ul>\n";
@modules = &get_visible_module_infos();
%cats = &list_categories(\@modules);
print "<li>$text{'index_webmincats'}\n";
print join(" | ",
	   map { "<a href='index_webmin.cgi?cat=$_'>$cats{$_}</a>" }
	       sort { $b cmp $a } (keys %cats)),"<br>\n";
print "</ul>\n";

&ui_print_footer();

