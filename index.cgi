#!/usr/local/bin/perl
# Show a menu of options (list domains, create domains, webmin), or folders
# if this is Usermin

require './web-lib.pl';
&init_config();
require './ui-lib.pl';
%text = &load_language($current_theme);

# Work out page title
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
$prod = &get_product_name();
if ($prod eq 'webmin' && &foreign_available("virtual-server")) {
	# Yes .. what can we do?
	$hasvirt = 1;
	&foreign_require("virtual-server", "virtual-server-lib.pl");
	%minfo = &get_module_info("virtual-server");
	$title = $gconfig{'nohostname'} ? $text{'vmain_title2'} :
		&text('vmain_title', $minfo{'version'}, $hostname, $ostr);
	}
elsif ($prod eq 'usermin' && &foreign_available("mailbox") &&
       &get_webmin_version() >= 1.313) {
	# We have Usermin mail
	$hasmail = 1;
	}
else {
	# Just show Webmin title
	$title = $gconfig{'nohostname'} ? $text{'main_title2'} :
			&text('main_title', $ver, $hostname, $ostr);
	}
&ui_print_header(undef, $title, "", undef, undef, 1, 1);

print "<ul>\n";
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
		if ($dleft == 0 && $aleft == 0) {
			# Cannot add
			}
		elsif (!&virtual_server::can_create_master_servers() &&
		       &virtual_server::can_create_sub_servers()) {
			# Can just create own sub-server
			print "<li><a href='virtual-server/domain_form.cgi'>$text{'index_vaddsub'}</a><br>\n";
			}
		elsif (&virtual_server::can_create_master_servers()) {
			# Can create master or sub-server
			print "<li><a href='virtual-server/domain_form.cgi'>$text{'index_vadddom'}</a><br>\n";
			}
		}

	# Template-level links
	@buts = &virtual_server::get_all_global_links();
	@buts = grep { $_->{'icon'} ne 'index' } @buts;
	@tcats = &unique(map { $_->{'cat'} } @buts);
	foreach my $tc (@tcats) {
		@incat = grep { $_->{'cat'} eq $tc } @buts;
		print "<li>";
		if ($tc) {
			print "$incat[0]->{'catname'}:\n";
			}
		@clinks = map { my $t = $_->{'target'} ? "target=$_->{'target'}" : ""; "<a href='$_->{'url'}' $target>$_->{'title'}</a>" } @incat;
		print &ui_links_row(\@clinks);
		}

	# System or account information
	print "<li><a href='index_sysinfo.cgi'>$text{'index_vsysinfo'}</a><br>\n";

	# New features, if any
	if (defined(&virtual_server::get_new_features_html) &&
	    ($newhtml = &virtual_server::get_new_features_html())) {
		print "<li><a href='index_nf.cgi'>$text{'index_vnf'}</a><br>\n";
		}

	# Package updates
	if (&foreign_available("security-updates")) {
		&foreign_require("security-updates", "security-updates-lib.pl");
		@poss = &security_updates::list_possible_updates();
		if (@poss) {
			print "<li><a href='index_updates.cgi'>",&text('index_vupdates', scalar(@poss)),"</a><br>\n";
			}
		}
	}
elsif ($hasmail) {
	# Show Usermin folders
	&foreign_require("mailbox", "mailbox-lib.pl");
	@folders = &mailbox::list_folders_sorted();
	$df = $mailbox::userconfig{'default_folder'};
	$dfolder = $df ? &mailbox::find_named_folder($df, \@folders) :
			 $folders[0];
	print &ui_form_start("mailbox/mail_search.cgi");
	print &ui_hidden("simple", 1);
	print &ui_hidden("folder", $dfolder->{'index'});

	foreach $f (@folders) {
		$fid = &mailbox::folder_name($f);
		$star = $f->{'type'} == 6 &&
			$mailbox::special_folder_id &&
			$f->{'id'} == $mailbox::special_folder_id ?
			 "<img src=mailbox/images/special.gif border=0>" : "";
		$umsg = "";
		if (defined(&mailbox::should_show_unread) &&
		    &mailbox::should_show_unread($f)) {
			local ($c, $u) = &mailbox::mailbox_folder_unread($f);
			$umsg = "&nbsp;($u)" if ($u);
			}
		push(@flinks, "<a href='mailbox/index.cgi?id=$fid'>$star$f->{'name'}$umsg</a>");
		}
	print "<li>$text{'index_folders'}\n",join(" | ",@flinks),"<br>\n";

	# Show search box
	print "<li>$text{'index_msearch'}\n",
	      &ui_textbox("search", undef, 10)," ",
	      &ui_submit($text{'index_msearchok'}),"<br>\n";

	# Show various links for mail/folder management
	push(@mlinks, "<a href='mailbox/reply_mail.cgi?new=1&folder=$dfolder->{'id'}'>$text{'index_compose'}</a>");
	%mconfig = &foreign_config("mailbox");
	$flink = $mconfig{'mail_system'} == 4 ? "mailbox/list_ifolders.cgi"
					      : "mailbox/list_folders.cgi";
	push(@mlinks, "<a href='$flink'>$text{'index_lfolders'}</a>");
	push(@mlinks, "<a href='mailbox/list_addresses.cgi'>$text{'index_laddresses'}</a>");
	if (!$mconfig{'noprefs'}) {
		push(@mlinks, "<a href='uconfig.cgi?mailbox'>$text{'index_lprefs'}</a>");
		}
	if (&foreign_available("filter")) {
		push(@mlinks, "<a href='filter/'>$text{'index_lfilter'}</a>");
		}
	push(@mlinks, "<a href='changepass/'>$text{'index_lpass'}</a>");
	print "<li>$text{'index_mlinks'}\n",join(" | ",@mlinks),"<br>\n";

	print &ui_form_end();
	}

# Show links to Webmin or Usermin module categories
@modules = &get_visible_module_infos();
%cats = &list_categories(\@modules);
print "<li>$text{'index_'.$prod.'cats'}\n";
print join(" | ",
	   map { "<a href='index_webmin.cgi?cat=$_'>$cats{$_}</a>" }
	       sort { $b cmp $a } (keys %cats)),"<br>\n";

# Show logout link
if (!$ENV{'SSL_USER'} && !$ENV{'LOCAL_USER'}) {
	if ($main::session_id) {
		print "<li><a href='session_login.cgi?logout=1'>",
		      "$text{'main_logout'}</a><br>";
		}
	else {
		print "<li><a href=switch_user.cgi>$text{'main_switch'}</a><br>";
		}
	}

print "</ul>\n";

&ui_print_footer();

