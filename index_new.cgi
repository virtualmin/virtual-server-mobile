#!/usr/local/bin/perl
# Shows the equivalent of the left-side menu

# XXX un-comment later
#use strict;
#use warnings;
$trust_unknown_referers = 1;
require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
our (%in, %text);
&ReadParse();

# Find all left-side items from Webmin
my $sects = { };
my @leftitems = list_combined_webmin_menu(undef, \%in);

# Also get right-side items, to look for notifications and redirects
my @info = &list_combined_system_info();
my ($redir) = grep { $_->{'type'} eq 'redirect' } @info;
if ($redir) {
	&redirect($redir->{'url'});
        return;
	}
my @warns = grep { $_->{'type'} eq 'warning' } @info;
foreach my $info (@warns) {
	print &ui_alert_box($info->{'warning'},
			    $info->{'level'} || 'warn');
	}

# Get all Webmin modules
my @mods = &list_modules_webmin_menu();

# Work out page title
if ($hasvirt) {
        %minfo = &get_module_info("virtual-server");
        $title = &text('index_virtualmintitle', $minfo{'version'});
        }
elsif ($hasvm2) {
        %minfo = &get_module_info("server-manager");
        $title = &text('index_cloudmintitle', $minfo{'version'});
        }
elsif (&get_product_name() eq 'usermin') {
        $title = &text('index_usermintitle', &get_webmin_version());
        }
else {
        $title = &text('index_webmintitle', &get_webmin_version());
        }
$title = &get_html_title($title);

# Figure out if there are some left menu items to show. If so, they come first
# and Webmin modules are below. Otherwise, modules are at the top level
if (@leftitems) {
	push(@leftitems, { 'type' => 'cat',
			   'desc' => &get_product_name() eq 'webmin' ?
						$text{'index_wmodules'} :
						$text{'index_umodules'},
			   'members' => \@mods });
	}
else {
	@leftitems = @mods;
	}

# XXX logout link?

# Show the menu of items
# XXX

$main::theme_iui_no_default_div = 1;
&ui_print_header(undef, $title, "", undef, undef, 1, 1);

if (&theme_use_iui()) {
	&generate_iui_menu(\@leftitems, 'main', $title, 1);
	}
else {
	# XXX plain mode
	}

# generate_iui_menu(&items, id, title, visible)
sub generate_iui_menu
{
my ($items, $id, $title, $visible) = @_;
print "<ul id='$id' title='$title'",($visible ? " selected='true'" : ""),">\n";
foreach my $item (@$items) {
	if ($item->{'type'} eq 'item') {
		# Link to some page
		my $link = &add_webprefix($item->{'link'});
		print "<li><a href='$link'>$item->{'desc'}</a></li>\n";
		}
	elsif ($item->{'type'} eq 'cat') {
		# Link to a sub-category
		print "<li><a href='#$item->{'id'}'>$item->{'desc'}</a></li>\n";
		# XXX contents are later
		}
	elsif ($item->{'type'} eq 'html') {
		# XXX
		}
	elsif ($item->{'type'} eq 'hr') {
		print "<li><hr></li>\n";
		}
	}
print "</ul>\n";
foreach my $item (grep { $_->{'type'} eq 'cat' } @$items) {
	&generate_iui_menu($item->{'members'}, $item->{'id'},
			   $item->{'desc'}, 0);
	}
}

&ui_print_footer();

# Generate a list of links for mobile devices
sub generate_mobile_main_menu
{
print "<ul>\n";
if ($hasvirt) {
	# Check licence
	print $lwarn;

	# See if module config needs to be checked
	if ($configcheck) {
		print &ui_form_start("virtual-server/check.cgi");
		print "<b>$virtual_server::text{'index_needcheck'}</b><p>\n";
		print &ui_submit($virtual_server::text{'index_srefresh'});
		print &ui_form_end();
		}

	# List Virtualmin domains
	print "<form action=index_search.cgi>\n";
	print "<li><a href='index_list.cgi'>$text{'index_vmenu'}</a><br>\n";

	# Modify domains
	if (@configdoms) {
		print "<li><a href='virtual-server/index.cgi'>$text{'index_vindex'}</a><br>\n";
		}

	# Configure a domain
	print "<li>$text{'index_vfind'} ",&ui_textbox("search", undef, 15)," ",
	      &ui_submit($text{'index_veditok'}),"<br>\n";

	# Create server
	if ($dom_create_mode == 1) {
		# Can just create own sub-server
		print "<li><a href='virtual-server/domain_form.cgi'>",
		      "$text{'index_vaddsub'}</a><br>\n";
		}
	elsif ($dom_create_mode == 2) {
		# Can create master or sub-server
		print "<li><a href='virtual-server/domain_form.cgi'>",
		      "$text{'index_vadddom'}</a><br>\n";
		}

	# Template-level links
	@buts = grep { $_->{'icon'} ne 'index' } @buts;
	@tcats = &unique(map { $_->{'cat'} } @buts);
	foreach my $tc (@tcats) {
		my @incat = grep { $_->{'cat'} eq $tc } @buts;
		print "<li><b>$incat[0]->{'catname'}</b>\n";
		print "<ul>\n";
		foreach my $c (@incat) {
			my $t = $c->{'target'} ? "target=$c->{'target'}" : "";
			print "<li><a href='$c->{'url'}' $t>$c->{'title'}</a><br>\n";
			}
		print "</ul>\n";
		}

	# New features, if any
	if ($newhtml) {
		print "<li><a href='index_nf.cgi'>$text{'index_vnf'}</a><br>\n";
		}
	}

# VM2 options
if ($hasvm2) {
	print "<p>\n" if ($hasvirt);	# Spacer

	# List Virtualmin domains
	print "<form action=index_ssearch.cgi>\n";
	print "<li><a href='index_slist.cgi'>$text{'index_v2menu'}</a><br>\n";

	# Modify systems
	if (@servers) {
		print "<li><a href='server-manager/index.cgi'>$text{'index_v2index'}</a><br>\n";
		}

	# Search for a server
	print "<li>$text{'index_v2find'} ",&ui_textbox("search", undef, 15)," ",
	      &ui_submit($text{'index_veditok'}),"<br>\n";

	# Create system links
	if (@clinks) {
		print "<li><b>$text{'index_v2create'}</b><br>\n";
		print "<ul>\n";
		foreach my $c (@clinks) {
			my $form = $c->{'link'} ? $c->{'link'} :
				   $c->{'create'} ? 'create_form.cgi'
						  : 'add_form.cgi';
			print "<li><a href='/server-manager/$form?",
			      "type=$c->{'type'}'>",$c->{'desc'},"</a><br>\n";
			}
		print "</ul>\n";
		}

	# Global VM2 links
	foreach my $c (&unique(@$gcats)) {
		print "<li><b>",$server_manager::text{'cat_'.$c} ||
				$text{'left_vm2'.$c},"</b><br>\n";
		print "<ul>\n";
		for(my $i=0; $i<@$glinks; $i++) {
			next if ($gcats->[$i] ne $c);
			print "<li><a href='$glinks->[$i]'>",
			      "$gtitles->[$i]</a><br>\n";
			}
		print "</ul>\n";
		}
	}

if ($hasmail) {
	# Show Usermin folders
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
	push(@mlinks, "<a href='$flink'>$text{'index_lfolders'}</a>");
	push(@mlinks, "<a href='mailbox/list_addresses.cgi'>$text{'index_laddresses'}</a>");
	if (!$mconfig{'noprefs'}) {
		push(@mlinks, "<a href='uconfig.cgi?mailbox'>$text{'index_lprefs'}</a>");
		}
	if (&foreign_available("filter")) {
		push(@mlinks, "<a href='filter/'>$text{'index_lfilter'}</a>");
		}
	if (&foreign_available("changepass")) {
		push(@mlinks, "<a href='changepass/'>$text{'index_lpass'}</a>");
		}
	print "<li>$text{'index_mlinks'}\n",join(" | ",@mlinks),"<br>\n";

	print &ui_form_end();
	}

# Package updates
if (@poss) {
	print "<li><a href='index_updates.cgi' target=_self>",
	      &text('index_vupdates', scalar(@poss)),"</a><br>\n";
	}

# Show links to Webmin or Usermin module categories
print "<li><b>",$text{'index_'.$prod.'cats'},"</b><br>\n";
print "<ul>\n";
foreach my $c (@cats) {
	print "<li><a href='index_webmin.cgi?cat=$c->{'code'}'>$c->{'desc'}</a><br>\n";
	}

# Show refresh modules link
if (&foreign_available("webmin")) {
	print "<li><a href=webmin/refresh_modules.cgi>",
	      "$text{'main_refreshmods'}</a><br>\n";
	}

print "</ul>\n";


# System or account information
print "<li><a href='index_sysinfo.cgi'>$text{'index_vsysinfo'}</a><br>\n";

# Show logout link
if ($logout_link) {
	print "<li><a href='$logout_link'>$logout_title</a><br>\n";
	}

print "</ul>\n";
}

# Generate links for Virtualmin and Webmin, plus sub-links for domains, using
# IUI lists
sub generate_iui_main_menu
{
# First menu
if (!$haswebmin) {
	print "<ul id='main' title='$title' selected='true'>\n";
	}
if ($hasvirt) {
	# List/edit links
	if ($lwarn) {
		print "<li><a href='#license'>* $text{'index_vwarn'}</a></li>\n";
		}
	if ($configcheck) {
		print "<li><a href='virtual-server/check.cgi' target=_self>",
		      "* $virtual_server::text{'index_srefresh'}</a></li>\n";
		}
	if (@doms) {
		print "<li><a href='#domains'>$text{'index_vmenu'}</a></li>\n";
		}
	if (@configdoms) {
		print "<li><a href='virtual-server/index.cgi'>".
		      "$text{'index_vindex'}</a></li>\n";
		}
	print "<li><a href='#dsearch'>$text{'index_vdsearch'}</a></li>\n";

	# Create links
	if ($dom_create_mode == 1) {
		# Can just create own sub-server
		print "<li><a href=virtual-server/domain_form.cgi ",
		      "target=_self>$text{'index_vaddsub'}</a></li>\n";
		}
	elsif ($dom_create_mode == 2) {
		# Can create master or sub-server
		print "<li><a href=virtual-server/domain_form.cgi ",
		      "target=_self>$text{'index_vadddom'}</a></li>\n";
		}

	# Link to templates
	if (@buts) {
		print "<li><a href='#global'>$text{'index_vglobal'}</a></li>\n";
		}

	# New features, if any
	if ($newhtml) {
		print "<li><a href='#newfeat'>$text{'index_vnf'}</a></li>\n";
		}
	}

# VM2-specific options
if ($hasvm2) {
	if (@servers) {
		print "<li><a href='#servers'>$text{'index_v2menu'}</a></li>\n";
		print "<li><a href='server-manager/index.cgi'>$text{'index_v2index'}</a></li>\n";
		}
	print "<li><a href='#ssearch'>$text{'index_vssearch'}</a></li>\n";

	# Link to VM2 global settings
	if (@$gcats) {
		print "<li><a href='#v2global'>",
		      "$text{'index_v2global'}</a></li>\n";
		}

	# Link to VM2 creation links
	if (@clinks) {
		print "<li><a href='#v2create'>",
		      "$text{'index_v2create'}</a></li>\n";
		}

	# VM2 new features, if any
	if ($newv2html) {
		print "<li><a href='#newv2feat'>$text{'index_v2nf'}</a></li>\n";
		}
	}

if ($hasmail) {
	# Usermin email address
	($fromaddr) = &mailbox::split_addresses(
			&mailbox::get_preferred_from_address());
	print "<li style='font-size: 12px'>\n";
	print $fromaddr->[1]," : \n" if ($fromaddr->[1]);
	print $fromaddr->[0],"\n";
	print "</li>\n";

	# Usermin folders
	foreach $f (@folders) {
		$fid = &mailbox::folder_name($f);
		$star = $f->{'type'} == 6 &&
			$mailbox::special_folder_id &&
			$f->{'id'} == $mailbox::special_folder_id ?
			 "<img src=mailbox/images/special.gif border=0>" : "";
		$umsg = "";
		if (&mailbox::should_show_unread($f)) {
			local ($c, $u) = &mailbox::mailbox_folder_unread($f);
			$umsg = "&nbsp;($u)" if ($u);
			}
		print "<li><a href='mailbox/index.cgi?id=$fid' target=_self>",
		      "$star$f->{'name'}$umsg</a></li>\n";
		}

	# Search mail
	print "<li><a href='#usearch'>$text{'index_usearch'}</a></li>\n";

	# Compose
	print "<li><a href='mailbox/reply_mail.cgi?new=1&folder=$dfolder->{'id'}' target=_self>$text{'index_compose'}</a></li>\n";

	# Manage folders
	print "<li><a href='$flink' target=_self>$text{'index_lfolders'}</a></li>\n";

	# Addressbook
	print "<li><a href='mailbox/list_addresses.cgi' target=_self>",
	      "$text{'index_laddresses'}</a></li>\n";

	# Preferences
	if (!$mconfig{'noprefs'}) {
		print "<li><a href='uconfig.cgi?mailbox' target=_self>",
		      "$text{'index_lprefs'}</a></li>\n";
		}

	# Filter mail
	if (&foreign_available("filter")) {
		print "<li><a href='filter/' target=_self>",
		      "$text{'index_lfilter'}</a></li>\n";
		}

	# Change password
	if (&foreign_available("changepass")) {
		print "<li><a href='changepass/' target=_self>",
		      "$text{'index_lpass'}</a></li>\n";
		}
	}

# Package updates
if (@poss) {
	print "<li><a href='index_updates.cgi' target=_self>",
	      "* ",&text('index_vupdates', scalar(@poss)),"</a></li>\n";
	}

# Webmin modules link
if (!$haswebmin) {
	local $modules_title = $prod eq 'usermin' ? $text{'index_umodules'}
						  : $text{'index_wmodules'};
	print "<li><a href='#modules'>$modules_title</a></li>\n";
	}

# System info
if (!$haswebmin) {
	print "<li><a href='index_sysinfo.cgi' target=_self>",
	      "$text{'index_vsysinfo'}</a></li>\n";
	}

# Logout link, if possible
if ($logout_link && !$haswebmin) {
	print "<li><a href='$logout_link' target=_self>",
	      "$logout_title</a></li>\n";
	}

if (!$haswebmin) {
	print "</ul>\n";
	}

#################################### Virtualmin

# License warning page
if ($hasvirt && $lwarn) {
	print "<div id='license' class='panel' title='$text{'index_vwarn'}'>\n";
	print $lwarn;
	print "</div>\n";
	}

# New features panel
if ($newhtml) {
	print "<div id='newfeat' class='panel' title='$text{'index_vnf'}'>\n";
	print $newhtml;
	print "</div>\n";
	}

# Virtualmin domains menu
if ($hasvirt && @doms) {
	print "<ul id='domains' title='$text{'index_vmenu'}'>\n";
	foreach my $d (sort { lc($a->{'dom'}) cmp lc($b->{'dom'}) } @doms) {
		print "<li>",
		      "<a href='index_edit.cgi?dom=$d->{'id'}' target=_self ",
		      ($d->{'disabled'} ? "style='font-style:italic'" : ""),
		      ">",&virtual_server::show_domain_name($d),
		      "</a>\n";
		}
	print "</ul>\n";
	}

# Popup for domain search
if ($hasvirt) {
	print "<form id='dsearch' class='dialog normalSubmit' action='index_search.cgi' method='post' target=_self>\n";
	print "<fieldset>\n";
	print "<h1>$text{'index_vdsearch'}</h1>\n";
	print "<a class='button leftButton' type='cancel' ",
	      "onClick='cancelDialog(form)'>$text{'cancel'}</a>\n";
	print "<a class='button blueButton' type='submit' ",
	      "onClick='submitForm(form)'>$text{'index_vdsearchok'}</a>\n";
	print "<label>$text{'index_vdsearchdom'}</label>\n";
	print "<input id=search type=text name=search>\n";
	print "</fieldset>\n";
	print "</form>\n";
	}

# Template-level categories
if ($hasvirt) {
	print "<ul id='global' title='$text{'index_vglobal'}'>\n";
	foreach my $tc (@tcats) {
		local @incat = grep { $_->{'cat'} eq $tc } @buts;
		if ($tc) {
			# Link to category
			print "<li><a href='#global_$tc'>",
			      "$incat[0]->{'catname'}</a></li>\n";
			}
		else {
			# Items in no category
			foreach my $c (@incat) {
				local $t = $c->{'target'} || "_self";
				print "<li><a href='$c->{'url'}' target=$t>",
				      "$c->{'title'}</a></li>\n";
				}
			}
		}
	print "</ul>\n";
	}

# Template-options in categories
if ($hasvirt) {
	foreach my $tc (@tcats) {
		next if (!$tc);		# Non-categorized items are above
		local @incat = grep { $_->{'cat'} eq $tc } @buts;
		print "<ul id='global_$tc' title='$incat[0]->{'catname'}'>\n";
		foreach my $c (@incat) {
			local $t = $c->{'target'} || "_self";
			print "<li><a href='$c->{'url'}' target=$t>",
			      "$c->{'title'}</a></li>\n";
			}
		print "</ul>\n";
		}
	}

#################################### VM2

# VM2 global categories
if ($hasvm2 && @$gcats) {
	print "<ul id='v2global' title='$text{'index_v2global'}'>\n";
	foreach my $c (&unique(@$gcats)) {
		print "<li><a href='#v2global_$c'>",
		      $server_manager::text{'cat_'.$c} || $text{'left_vm2'.$c},
		      "</a></li>\n";
		}
	print "</ul>\n";
	}

# VM2 global options in categories
if ($hasvm2 && @$gcats) {
	foreach my $c (&unique(@$gcats)) {
		print "<ul id='v2global_$c' title='",
		      $server_manager::text{'cat_'.$c} || $text{'left_vm2'.$c},
		      "'>\n";
		for(my $i=0; $i<@$glinks; $i++) {
			next if ($gcats->[$i] ne $c);
			print "<li><a href='$glinks->[$i]' target=_self>",
			      "$gtitles->[$i]</a></li>\n";
			}
		print "</ul>\n";
		}
	}

# VM2 create links
if ($hasvm2 && @clinks) {
	print "<ul id='v2create' title='$text{'index_v2create'}'>\n";
	foreach my $c (@clinks) {
		my $form = $c->{'link'} ? $c->{'link'} :
			   $c->{'create'} ? 'create_form.cgi'
					  : 'add_form.cgi';
		print "<li><a href='/server-manager/$form?type=$c->{'type'}' ",
		      "target=_self>",$c->{'desc'},"</a></li>\n";
		}
	print "</ul>\n";
	}

# VM2 systems menu
if ($hasvm2 && @servers) {
	print "<ul id='servers' title='$text{'index_v2menu'}'>\n";
	foreach my $s (sort { lc($a->{'host'}) cmp lc($b->{'host'}) }@servers) {
		print "<li><a href='index_system.cgi?id=$s->{'id'}' ",
		      "target=_self>",$s->{'short_host'},"</a></li>\n";
		}
	print "</ul>\n";
	}

# New VM2 features panel
if ($newv2html) {
	print "<div id='newv2feat' class='panel' title='$text{'index_v2nf'}'>";
	print $newv2html;
	print "</div>\n";
	}

# Popup for VM2 system search
if ($hasvm2) {
	print "<form id='ssearch' class='dialog normalSubmit' action='index_ssearch.cgi' method='post' target=_self>\n";
	print "<fieldset>\n";
	print "<h1>$text{'index_vssearch'}</h1>\n";
	print "<a class='button leftButton' type='cancel' ",
	      "onClick='cancelDialog(form)'>$text{'cancel'}</a>\n";
	print "<a class='button blueButton' type='submit' ",
	      "onClick='submitForm(form)'>$text{'index_vdsearchok'}</a>\n";
	print "<label>$text{'index_vssearchserver'}</label>\n";
	print "<input id=search type=text name=search>\n";
	print "</fieldset>\n";
	print "</form>\n";
	}

#################################### Usermin Read Mail

# Popup for mail search
if ($hasmail) {
	print "<form id='usearch' class='dialog normalSubmit' action='mailbox/mail_search.cgi' method='post' target=_self>\n";
	print "<input type=hidden name=simple value=1>\n";
	print &ui_hidden("folder", $dfolder->{'index'});
	print "<fieldset>\n";
	print "<h1>$text{'index_usearch'}</h1>\n";
	print "<a class='button leftButton' type='cancel' ",
	      "onClick='cancelDialog(form)'>$text{'cancel'}</a>\n";
	print "<a class='button blueButton' type='submit' ",
	      "onClick='submitForm(form)'>$text{'index_vdsearchok'}</a>\n";
	print "<input id=search type=text name=search style='width:100%'>\n";
	print "</fieldset>\n";
	print "</form>\n";
	}

#################################### Webmin

if ($haswebmin) {
	print "<ul id='modules' title='$title' selected='true'>\n";
	}
else {
	print "<ul id='modules' title='$modules_title'>\n";
	}

# Webmin search popup
if (-r "$root_directory/webmin-search-lib.pl") {
	print "<li><a href='#wsearch'>",
		($prod eq 'webmin' ? $text{'index_wmsearch'}
				   : $text{'index_umsearch'})."</a></li>\n";
	}

# Webmin categories
foreach my $c (@cats) {
	print "<li><a href='#cat_$c->{'code'}'>$c->{'desc'}</a></li>\n";
	}

# Logout, system info and refresh links, if in Webmin-only mode
if ($haswebmin) {
	print "<li><a href='index_sysinfo.cgi' target=_self>",
	      "$text{'index_vsysinfo'}</a></li>\n";
	}
if (&foreign_available("webmin")) {
	print "<li><a href=webmin/refresh_modules.cgi>",
	      "$text{'main_refreshmods'}</a></li>\n";
	}
if ($logout_link && $haswebmin) {
	print "<li><a href='$logout_link' target=_self>",
	      "$logout_title</a></li>\n";
	}

print "</ul>\n";

# Webmin modules in categories
foreach my $c (@cats) {
	print "<ul id='cat_$c->{'code'}' title='$c->{'desc'}'>\n";
	foreach my $m (@{$c->{'modules'}}) {
		print "<li><a href='$m->{'dir'}/' target=_self>$m->{'desc'}</a></li>\n";
		}
	print "</ul>\n";
	}

# Popup for Webmin search
print "<form id='wsearch' class='dialog normalSubmit' action='webmin_search.cgi' method='post' target=_self>\n";
print "<fieldset>\n";
print "<h1>",($prod eq 'webmin' ? $text{'index_wmsearch'}
				: $text{'index_umsearch'})."</h1>\n";
print "<a class='button leftButton' type='cancel' ",
      "onClick='cancelDialog(form)'>$text{'cancel'}</a>\n";
print "<a class='button blueButton' type='submit' ",
      "onClick='submitForm(form)'>$text{'index_vdsearchok'}</a>\n";
print "<label>$text{'index_wsearchfor'}</label>\n";
print "<input id=search type=text name=search>\n";
print "</fieldset>\n";
print "</form>\n";
}

# add_webprefix(link)
# If a URL starts with a / , add webprefix
sub add_webprefix
{
my ($link) = @_;
return $link =~ /^\// ? $gconfig{'webprefix'}.$link : $link;
}
