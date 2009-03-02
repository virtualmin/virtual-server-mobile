# Theme-level UI override functions
# XXX Usermin mailbox module support
#	XXX nicer mail / folder lists for iPhone
#	XXX icons next to folders
#	XXX next/prev navigator
#	XXX prefs on every page??

# Disable buttons on edit_domain page
$main::basic_virtualmin_domain = 1;

# Disable other links on virtualmin module main page
$main::basic_virtualmin_menu = 1;
$main::nocreate_virtualmin_menu = 1;

# Tell CGIs that uploads are not possible
$main::no_browser_uploads = 1;

# The theme will provide links for VM2
$main::vm2_no_create_links = 1;
$main::vm2_no_edit_buttons = 1;
$main::vm2_no_global_links = 1;

sub theme_ui_post_header
{
local ($text) = @_;
local $rv;
if ($text) {
	$rv .= "<div type=panel>\n" if ($main::theme_iui_no_default_div);
	print "<div class=linksbar>\n";
	print "<h2>$text</h2>\n";
	print "</div>\n";
	$rv .= "</div>\n" if ($main::theme_iui_no_default_div);
	}
return $rv;
}

sub theme_ui_pre_footer
{
return "";
}

# theme_footer([page, name]+, [noendbody])
# Output a footer for returning to some page
sub theme_footer
{
local $i;
local @links;
for($i=0; $i+1<@_; $i+=2) {
	local $url = $_[$i];
	if ($url ne '/' || !$tconfig{'noindex'}) {
		if ($url eq '/') {
			# Don't change link to /
			$url = "/";
			}
		elsif ($url eq '' && $module_name eq 'virtual-server' ||
		       $url eq '/virtual-server/') {
			# Don't bother with virtualmin menu, unless the current
			# page is view/edit_domain.cgi, in which case link
			# back to index_edit.cgi
			if ($0 =~ /(view|edit)_domain.cgi/ &&
			    $in{'dom'} &&
			    $module_name eq 'virtual-server') {
				$url = "/index_edit.cgi?dom=$in{'dom'}";
				}
			else {
				next;
				}
			}
		elsif ($url eq '' && $module_name eq 'server-manager' ||
		       $url eq '/server-manager/') {
			# Don't bother with VM2 menu, unless the current page
			# is edit_serv.cgi
			if ($0 =~ /edit_serv.cgi/ &&
			    $in{'id'} &&
			    $module_name eq 'server-manager') {
				$url = "/index_system.cgi?id=$in{'id'}";
				}
			else {
				next;
				}
			}
		elsif ($url eq '' && $module_name eq 'mailbox') {
			# Don't bother with link to mail list from
			# pages other than view/reply mail
			if ($0 =~ /list_(folders|ifolders).cgi/ ||
			    $0 =~ /list_addresses.cgi/ ||
			    $0 =~ /edit_sig.cgi/ ||
			    $0 =~ /edit_(folder|ifolder|virt|imap|pop3|comp).cgi/) {
				next;
				}
			}
		elsif ($url =~ /^\/mailbox(|\/|index.cgi)$/) {
			# For links to read mail from other modules, link
			# to the main menu (ie. preferences)
			next;
			}
		elsif ($url eq '' && $module_name) {
			$url = "/$module_name/$module_info{'index_link'}";
			}
		elsif ($url =~ /^\?/ && $module_name) {
			$url = "/$module_name/$url";
			}
		elsif ($url =~ /(edit|view)_domain.cgi\?dom=(\d+)/) {
			# Force links back to edit form to domain options list
			$url = "/index_edit.cgi?dom=$2";
			}
		elsif ($url =~ /edit_serv.cgi\?id=(\d+)/) {
			# Force links back to edit form to system options list
			$url = "/index_system.cgi?id=$1";
			}
		$url = "$gconfig{'webprefix'}$url" if ($url =~ /^\//);
		push(@links, [ $url, &text('main_return', $_[$i+1]) ]);
		}
	}
if (&theme_use_iui()) {
	# Close main body div
	if (!$main::theme_iui_no_default_div) {
		print "</div>\n";
		}

	# Output toolbar, if needed
	if (@links) {
		# Use first link from footer
		$theme_iui_toolbar_index = $links[0]->[0];
		}
	if (!$main::theme_iui_no_default_div && !$theme_iui_toolbar_index &&
	    $remote_user) {
		# For pages other than the main index, always have a backlink
		# (assuming we are logged in)
		$theme_iui_toolbar_index = "/";
		}
	if ($theme_iui_toolbar_title || $theme_iui_toolbar_index ||
	    $theme_iui_toolbar_button || $main::theme_iui_no_default_div) {
		print "<div class='toolbar'>\n";
		if ($theme_iui_toolbar_title) {
			# Title of page, full width if no buttons
			if ($theme_iui_toolbar_index ||
			    $main::theme_iui_no_default_div ||
			    $theme_iui_toolbar_button) {
				print "<h1 id='pageTitle'></h1>\n";
				}
			else {
				print "<h2 id='pageTitle'></h2>\n";
				}
			}
		if ($theme_iui_toolbar_index) {
			print "<a class='button indexButton' href='$theme_iui_toolbar_index' target=_self>Back</a>\n";
			}
		if ($main::theme_iui_no_default_div) {
			print "<a id='backButton' class='button' href='#'></a>\n";
			}
		if ($theme_iui_toolbar_button) {
			local $t = $theme_iui_toolbar_button->[0] =~ /help.cgi/ ? "target=_new" : "target=_self";
			print "<a class='button' href='$theme_iui_toolbar_button->[0]' $t>$theme_iui_toolbar_button->[1]</a>\n";
			}
		print "</div>\n";
		}
	}
else {
	# As bar-separated list
	print join("&nbsp;|&nbsp;",
		   map { "<a href='$_->[0]'>&lt;- $_->[1]</a>" } @links),"\n";
	}
if (!$_[$i]) {
	print "</body></html>\n";
	}
}

# theme_ui_table_start(heading, [tabletags], [cols])
# A table with a heading and table inside
sub theme_ui_table_start
{
local ($heading, $tabletags, $cols) = @_;
local $rv;
if (&theme_use_iui() && $theme_iui_fieldset_table) {
	# Use IUI field set
	$rv .= "<fieldset>\n";
	$rv .= "<div class=rowhead>$heading</div>\n" if (defined($heading));
	}
elsif (&theme_use_iui()) {
	# Start a styled block for the table
	$rv .= "<div class='webminTable'>\n";
	if (defined($heading)) {
		$rv .= "<div class='webminTableHeader'>$heading</div>\n";
		}
	$rv .= "<div class='webminTableBody'>\n";
	}
else {
	# Table is just elements below each other
	$rv .= "<font size=+1>$heading</font><br>\n" if (defined($heading));
	$rv .= "<hr>\n";
	}
$main::ui_table_cols = 2;
$main::ui_table_pos = 0;
return $rv;
}

# theme_ui_table_end()
# The end of a table started by ui_table_start
sub theme_ui_table_end
{
if (&theme_use_iui() && $theme_iui_fieldset_table) {
	return "</fieldset>\n";
	}
elsif (&theme_use_iui()) {
	return "</div></div>\n";
	}
else {
	return "<hr>\n";
	}
}


# theme_ui_table_row(label, value, [cols], [&td-tags])
# Returns HTML for a row in a table started by ui_table_start, with a 1-column
# label and 1+ column value.
sub theme_ui_table_row
{
local ($label, $value, $cols) = @_;
local $rv;
if (&theme_use_iui() && $theme_iui_fieldset_table) {
	# Use IUI field set
	$rv .= "<div class=row>\n";
	$rv .= "<label>$label</label>\n" if ($label =~ /\S/);
	$rv .= "<div class=rowvalue>$value</div>\n";
	$rv .= "</div>\n";
	}
elsif (&theme_use_iui()) {
	# Styles label and value
	if ($label =~ /\S/) {
		$rv .= "<div class='webminTableName'>$label</div>\n";
		}
	$rv .= "<div class='webminTableValue'>$value</div>\n";
	}
else {
	# Label and value are above each other
	$rv .= "<b>$label</b><br>\n" if ($label =~ /\S/);
	#$rv .= "&nbsp;&nbsp;" if (defined($label) &&
	#			  $value !~ /^\s*<table/ &&
	#			  $value !~ /^\s*<!--grid/);
	$rv .= "$value<br>\n";
	}
return $rv;
}

# theme_ui_hidden_table_row_start(label, name, flag)
# On the iPhone, returns a collapsible section start. On other devices, does
# nothing as CSS isn't supported.
sub theme_ui_hidden_table_row_start
{
local ($label, $name, $flag) = @_;
if (&theme_use_iui()) {
	my $rv = &theme_ui_hidden_start($label, $name, $flag);
	return $rv;
	}
else {
	return "";
	}
}

sub theme_ui_hidden_table_row_end
{
local ($name) = @_;
if (&theme_use_iui()) {
	return &theme_ui_hidden_end($name);
	}
else {
	return "";
	}
}

# theme_ui_hidden_table_start
sub theme_ui_hidden_table_start
{
local ($heading, $tabletags, $cols, $name, $status) = @_;
if (&theme_use_iui() && !$theme_iui_fieldset_table) {
	# Start a CSS / javascript collapsible table for the iPhone
	local $rv = "<div class='webminTable'>\n";
	local $openid = "hiddenopener_".$name;
	local $divid = "hiddendiv_".$name;
	local $opencls = $status ? "webminTableHeaderOpen"
				 : "webminTableHeaderClosed";
	local $divcls = $status ? "webminTableBodyOpen"
				: "webminTableBodyClosed";
	$rv .= "<div class=webminTableHeader><a class='$opencls' ".
	       "href='javascript:openCloseTable(\"$openid\", \"$divid\")' ".
	       "id='$openid'>$heading</a></div>\n";
	$rv .= "<div class='$divcls' id='$divid'>\n";
	return $rv;
	}
else {
	# Just output a normal table start, as mobile browsers don't support CSS
	return &theme_ui_table_start($heading, $tabletags, $cols);
	}
}

# theme_ui_hidden_table_end
# Just outputs a normal table end, as mobile browsers don't support CSS
sub theme_ui_hidden_table_end
{
local ($heading, $tabletags, $cols, $name, $status) = @_;
return &theme_ui_table_end($heading, $tabletags, $cols);
}

# theme_ui_columns_start(&headings, [width-percent], [noborder], [&tdtags], [heading])
# Returns HTML for a multi-column table, with the given headings
sub theme_ui_columns_start
{
local ($heads, $width, $noborder, $tdtags, $heading) = @_;
local $rv;
$main::theme_ui_columns_folders = 0;
$main::theme_ui_columns_search = 0;
$main::theme_ui_columns_filter = 0;
if ($module_name eq 'mailbox' && $0 =~ /list_(i?)folders.cgi/) {
	# For folders list, use different format
	$main::theme_ui_columns_folders = 1;
	}
elsif ($module_name eq 'mailbox' && $0 =~ /search_form.cgi/) {
	# For search form
	$main::theme_ui_columns_search = 1;
	}
elsif ($module_name eq 'filter' && $0 =~ /index.cgi/) {
	# For filter list
	$main::theme_ui_columns_filter = 1;
	}
else {
	# Just regular plain table
	$rv .= "<table".($noborder ? "" : " border").
			(defined($width) ? " width=$width%" : "").
			" class='ui_columns'>\n";
	if ($heading) {
		$rv .= "<font size=+1>$heading</font><br>\n";
		}
	$rv .= "<tr class='ui_columns_heads'>\n";
	local $i;
	for($i=0; $i<@$heads; $i++) {
		$rv .= "<th ".$tdtags->[$i].">".
		       (&theme_use_iui() ? "" : "<b>").
	               ($heads->[$i] eq "" ? "<br>" : $heads->[$i]).
		       (&theme_use_iui() ? "" : "</b>")."</th>\n";
		}
	$rv .= "</tr>\n";
	}
return $rv;
}

# theme_ui_columns_row(&columns, &tdtags)
# Returns HTML for a row in a multi-column table
sub theme_ui_columns_row
{
local ($cols, $tdtags) = @_;
local $rv;
if ($main::theme_ui_columns_folders) {
	# Show each row of folders as a block
	local %ttext = &load_language($current_theme);
	local $cb = &ui_checkbox("x", "x", undef, 0, undef, 1);
	local @c = @$cols;
	splice(@c, 2, 0, undef) if ($0 =~ /list_ifolders.cgi/);
	$rv .= ($c[0] || $cb);
	$rv .= $c[1]."<br>\n";
	if ($c[2]) {
		$rv .= "<b>$ttext{'folders_loc'}</b> ".$c[2]."<br>\n";
		}
	$rv .= "<b>$ttext{'folders_ty'}</b> ".$c[3].", ".$c[4]."<br>\n";
	if ($c[5] =~ /\S/) {
		$rv .= "<b>$ttext{'folders_acts'}</b> ".$c[5]."<br>\n";
		}
	}
elsif ($main::theme_ui_columns_search) {
	# Show each search term as a block
	local %ttext = &load_language($current_theme);
	local $neg = $cols->[2];
	if ($neg =~ /(neg_\d+)/) {
		$neg = &ui_checkbox("$1", 1, $ttext{'search_neg'}, 0);
		}
	$rv .= "<b>$ttext{'search_field'}</b> ".$cols->[1]."<br>\n";
	$rv .= "<b>$ttext{'search_text'}</b> ".$cols->[4].$neg."<br>\n";
	}
elsif ($main::theme_ui_columns_filter) {
	# Show each filter as a block
	local %ttext = &load_language($current_theme);
	local $cb = &ui_checkbox("x", "x", undef, 0, undef, 1);
	$rv .= ($cols->[0] || $cb);
	local $cond = $cols->[1];
	if ($cond =~ /^<([^>]*)>(.*)<\/a>$/) {
		local ($href, $txt) = ($1, $2);
		if (length($txt) > 40) {
			$txt = substr($txt, 0, 40);
			if ($txt =~ /<[^>]*$/) {
				$txt .= ">";	# Close HTML
				}
			$txt .= "..";
			}
		$cond = "<$href>$txt</a>";
		}
	$rv .= $cond."<br>\n";
	$rv .= "<b>$ttext{'filter_act'}</b> $cols->[2]<br>\n";
	if ($cols->[3]) {
		$rv .= "<b>$ttext{'filter_move'}</b> $cols->[3]<br>\n";
		}
	}
else {
	# Regular table
	$rv .= "<tr class='ui_columns_row'>\n";
	local $i;
	for($i=0; $i<@$cols; $i++) {
		$rv .= "<td ".$tdtags->[$i]." class='ui_columns_cell'>".
		       ($cols->[$i] eq "" ? "<br>" : $cols->[$i])."</td>\n";
		}
	$rv .= "</tr>\n";
	}
return $rv;
}

# theme_ui_columns_header(&columns, &tdtags)
# Returns HTML for a row in a multi-column table, with a header background
sub theme_ui_columns_header
{
local ($cols, $tdtags) = @_;
local $rv;
$rv .= "<tr class='ui_columns_header'>\n";
local $i;
for($i=0; $i<@$cols; $i++) {
	$rv .= "<th ".$tdtags->[$i].">".
	       (&theme_use_iui() ? "" : "<b>").
	       ($cols->[$i] eq "" ? "<br>" : $heads->[$i]).
	       (&theme_use_iui() ? "" : "</b>")."</th>\n";
	}
$rv .= "</tr>\n";
return $rv;
}

# theme_ui_checked_columns_row(&columns, &tdtags, checkname, checkvalue, [checked?])
# Returns HTML for a row in a multi-column table, in which the first
# column is a checkbox
sub theme_ui_checked_columns_row
{
local ($cols, $tdtags, $checkname, $checkvalue, $checked) = @_;
local $rv;
local $cb = &ui_checkbox($checkname, $checkvalue, undef, $checked);
if ($main::theme_ui_columns_folders || $main::theme_ui_columns_filter) {
	$rv = &theme_ui_columns_row([ $cb, @$cols ], $tdtags);
	}
else {
	$rv .= "<tr class='ui_checked_columns'>\n";
	$rv .= "<td ".$tdtags->[0].">".$cb."</td>\n";
	local $i;
	for($i=0; $i<@$cols; $i++) {
		$rv .= "<td ".$tdtags->[$i+1].">";
		$rv .= ($cols->[$i] eq "" ? "<br>" : $cols->[$i]);
		$rv .= "</td>\n";
		}
	$rv .= "</tr>\n";
	}
return $rv;
}

# theme_ui_radio_columns_row(&columns, &tdtags, checkname, checkvalue)
# Returns HTML for a row in a multi-column table, in which the first
# column is a radio button
sub theme_ui_radio_columns_row
{
local ($cols, $tdtags, $checkname, $checkvalue) = @_;
local $rv;
$rv .= "<tr class='ui_radio_columns'>\n";
$rv .= "<td ".$tdtags->[0].">".
       &ui_oneradio($checkname, $checkvalue, "", 0)."</td>\n";
local $i;
for($i=0; $i<@$cols; $i++) {
	$rv .= "<td ".$tdtags->[$i+1].">";
	$rv .= ($cols->[$i] !~ /\S/ ? "<br>" : $cols->[$i]);
	$rv .= "</td>\n";
	}
$rv .= "</tr>\n";
return $rv;
}

# theme_ui_columns_end()
# Returns HTML to end a table started by ui_columns_start
sub theme_ui_columns_end
{
if ($main::theme_ui_columns_folders || $main::theme_ui_columns_search ||
    $main::theme_ui_columns_filter) {
	return "";
	}
return "</table>\n";
}

# theme_select_all_link(field, form, text)
# Returns nothing, because javascript is assumed not to work
sub theme_select_all_link
{
return undef;
}

# theme_select_invert_link(field, form, text)
# Returns nothing, because javascript is assumed not to work
sub theme_select_invert_link
{
return undef;
}

# theme_ui_hidden_start(title, name, status, url)
# For the iPhone, returns the normal collapsible section. For others, returns
# a link that may halt other output if not open.
sub theme_ui_hidden_start
{
local ($title, $name, $status, $url) = @_;
local $rv;
if (&theme_use_iui()) {
	# Real CSS / javascript collapsing section
	local $openid = "hiddenopener_".$name;
	local $divid = "hiddendiv_".$name;
	local $opencls = $status ? "openerOpen" : "openerClosed";
	local $divcls = $status ? "hiddenOpen" : "hiddenClosed";
	$rv .= "<a href='javascript:openCloseHidden(\"$openid\", \"$divid\")' ".
	       "class='$opencls' id='$openid'>$title</a><br>\n";
	$rv .= "<div class='$divcls' id='$divid'>\n";
	}
else {
	# Fake it by redirecting output to nowhere
	local $nstatus = $status ? 0 : 1;
	print $status ? "-" : "+";
	$rv .= " <a href='$url?$name=$nstatus'>$title</a><br>\n";
	if (!$status) {
		open(NULLFILE, ">$null_file");
		$main::suppressing_hidden_start = select(NULLFILE);
		}
	else {
		$main::suppressing_hidden_start = undef;
		}
	}
return $rv;
}

# theme_ui_hidden_end(name)
sub theme_ui_hidden_end
{
local ($name) = @_;
if (&theme_use_iui()) {
	# Close hiding div
	return "</div>\n";
	}
else {
	# Stop supressing output
	if ($main::suppressing_hidden_start) {
		select($main::suppressing_hidden_start);
		}
	return "";
	}
}

# theme_ui_links_row(&links)
# Returns HTML for a row of links, like select all / invert selection / add..
sub theme_ui_links_row
{
local ($links) = @_;
local @nn = grep { $_ ne "" } @$links;
return @nn ? join(" | ", @nn)."<br>\n" : "";
}

sub theme_ui_yesno_radio
{
local ($name, $value, $yes, $no, $dis) = @_;
$yes = 1 if (!defined($yes));
$no = 0 if (!defined($no));
$value = int($value);
if (&theme_use_iui()) {
	# iPhone-style slider
	local $rv;
	local $tog = $value == $yes ? "true" : "false";
	$rv .= "<div class='row'><div id='${name}_toggle' class='toggle' toggled='$tog' onClick='var h = document.getElementById(\"$name\"); h.value = getAttribute(\"toggled\") == \"true\" ? \"$yes\" : \"$no\";'><span class='thumb'></span><span class='toggleOn'>$text{'yes'}</span><span class='toggleOff'>$text{'no'}</span></div></div>";
	$rv .= "<input type=hidden name=\"".&quote_escape($name)."\" ".
	       "id=\"".&quote_escape($name)."\" ".
	       "value=\"".&quote_escape($value)."\">";
	return $rv;
	}
else {
	# Regular input
	return &ui_radio($name, $value, [ [ $yes, $text{'yes'} ],
					  [ $no, $text{'no'} ] ], $dis);
	}
}

# theme_ui_print_header(subtext, args...)
# If called with "In domain XXX" as the subtext, put it after the title
sub theme_ui_print_header
{
local ($subtext, @args) = @_;
if (!&theme_use_iui()) {
	# Put domain name in title, with [ ]
	local $re = $text{'indom'} ||
		    $virtual_server::text{'indom'};
	$re =~ s/\$1/\(\\S+\)/;
	if ($subtext =~ /$re/) {
		$args[0] .= " [$1]";
		&header(@args);
		return;
		}
	}
# Any domain name is on its own line
&header(@args);
print &ui_post_header($subtext);
}

sub theme_redirect
{
local ($orig, $url) = @_;
if ($module_name eq "virtual-server" &&
    $url =~ /postsave.cgi\?dom=(\d+)/) {
	# Show domain menu after saving
	$url =~ s/\/([^\/]+)\/postsave.cgi/\/index_edit.cgi/g;
	}
elsif ($module_name eq "server-manager" && $0 =~ /save_serv.cgi/) {
	# Show server menu after saving main details
	local $id = $url =~ /id=(\S+)/ ? $1 : $in{'id'};
	if ($id) {
		$url =~ s/\/([^\/]+)\/index.cgi.*/\/index_system.cgi?id=$id/;
		}
	}
elsif ($module_name eq "virtual-server" && $orig eq "" &&
       $url =~ /^((http|https):\/\/([^\/]+))\//) {
	# Show templates page after saving global config
	$url = &theme_use_iui() ? "$1/index.cgi" : "$1/index_templates.cgi";
	}
print "Location: $url\n\n";
}

# For each tab, output just a link
sub theme_ui_tabs_start
{
local ($tabs, $name, $sel, $border) = @_;
if ($module_name eq 'mailbox' && $0 =~ /reply_mail.cgi/) {
	# Special layout for composing email, where we can't use hiding
	$theme_ui_tabs_current = $tabs;
	return undef;
	}
elsif (&theme_use_iui()) {
	# For IUI, show tabs as a spaced row of links
	$main::ui_tabs_selected = $sel;
	local $rv;
	$rv .= "<div class=tabsBody>";
	$rv .= "<table width=100% border=0 cellpadding=0 cellspacing=0 class=tabsTable><tr>\n";
	local $pc = int(100 / scalar(@$tabs));
	foreach my $t (@$tabs) {
		my $c = $t->[0] eq $sel ? "tabsSel" : "tabsUnSel";
		$rv .= "<td class='$c' id='tab_$t->[0]'><a href='' class='tabsLink' onClick='return selectTab(\"$name\", \"$t->[0]\")'>$t->[1]</a></td>\n";
		}
	$rv .= "</tr></table>\n";
	$rv .= &ui_hidden($name, $sel)."\n";
	return $rv;
	}
else {
	# Show list of tabs
	$theme_ui_tabs_current = undef;
	local $rv;
	foreach my $t (@$tabs) {
		$rv .= "&lt;<a href='$t->[2]'>".
		       ($t->[0] eq $sel ? "<b>" : "").
		       $t->[1].
		       ($t->[0] eq $sel ? "</b>" : "").
		       "</a>&gt;\n";
		}
	$rv .= "<br>\n";
	$rv .= &ui_hidden($name, $sel)."\n";
	$main::current_selected_tab{$name} = $sel;
	return $rv;
	}
}

# Doesn't need to return anything for text-mode tabs
sub theme_ui_tabs_end
{
if ($theme_ui_tabs_current) {
	# Compose email form .. so do nothing
	return "";
	}
elsif (&theme_use_iui()) {
	# Close big div for whole tab set
	return "</div>\n";
	}
else {
	return "";
	}
}

# When in text mode, suppress output unless the named tab is selected
sub theme_ui_tabs_start_tab
{
local ($name, $tab) = @_;
if ($theme_ui_tabs_current) {
	# In mode where all tabs are shown, for composing email
	local ($t) = grep { $_->[0] eq $tab } @$theme_ui_tabs_current;
	#print "<b>$t->[1]</b>:\n";
	}
elsif (&theme_use_iui()) {
	# Outputting the tab, but with CSS for hiding
	local $defclass = $tab eq $main::ui_tabs_selected ?
				"tabVisible" : "tabHidden";
	return "<div id='div_$tab' class='$defclass'>\n";
	}
elsif ($main::current_selected_tab{$name} ne $tab) {
	open(NULLFILE, ">$null_file");
	$main::suppressing_tab = select(NULLFILE);
	}
return "";
}

sub theme_ui_tabs_start_tabletab
{
return &theme_ui_tabs_start_tab(@_);
}

# If we are currently suppressing, stop it
sub theme_ui_tabs_end_tab
{
if ($theme_ui_tabs_current) {
	# End of tab in mode where we are showing all
	return "<br>\n";
	}
elsif (&theme_use_iui()) {
	# Close the tab, but with CSS for hiding
	return "</div>\n";
	}
elsif ($main::suppressing_tab) {
	# Stop suppressing output
	select($main::suppressing_tab);
	$main::suppressing_tab = undef;
	}
return "";
}

sub theme_ui_tabs_end_tabletab
{
return &theme_ui_tabs_end_tab(@_);
}

# Generate a simple list instead of a tab of icons
sub theme_icons_table
{
local ($links, $titles, $icons, $cols, $href, $w, $h, $befores, $afters) = @_;
local $i;
print "<ul>\n";
for($i=0; $i<@$links; $i++) {
	print "<li class='iconList'>";
	print $befores->[$i];
	if ($links->[$i]) {
		print "<a href='$links->[$i]' $href class='iconLink'>$titles->[$i]</a>";
		}
	else {
		print $titles->[$i];
		}
	print $afters->[$i];
	if (!&theme_use_iui()) {
		print "<br>\n";
		}
	print "</li>\n";
	}
print "</ul>\n";
}

# Doesn't bother with a grid, just put everything in one column
# (for most devices) or two columns (for iPhone)
sub theme_ui_grid_table
{
local ($elements, $cols, $width, $tds, $tabletags, $title) = @_;
return "" if (!@$elements);
if (&theme_use_iui()) {
	# Two-column grid, if narrow enough .. otherwise, one
	my $maxlen;
	foreach my $e (@$elements) {
		my $he = $e;
		$he =~ s/<[^>]*>//g;
		$maxlen = length($he) if (length($he) > $maxlen);
		}
	$cols = $maxlen > 30 ? 1 : 2;

	# Styled title
	my $rv;
	if (defined($title)) {
		$rv .= "<div class='webminGridBorder'>\n";
		$rv .= "<div class='webminGridHeader'>$title</div>\n";
		}
	else {
		$rv .= "<div class='webminGrid'>\n";
		}

	# Grid body as a table
	$rv .= "<div class='webminGridBody'>\n";
	$rv .= "<table".($width ? " width=$width%" : "").
		        ($tabletags ? " ".$tabletags : "").">\n";
	my $i;
	for($i=0; $i<@$elements; $i++) {
		$rv .= "<tr>" if ($i%$cols == 0);
		$rv .= "<td width=25% valign=top>".$elements->[$i]."</td>\n";
		$rv .= "</tr>" if ($i%$cols == $cols-1);
		}
	if ($i%$cols) {
		while($i%$cols) {
			$rv .= "<td width=25%></td>\n";
			$i++;
			}
		$rv .= "</tr>\n";
		}
	$rv .= "</table></div></div>\n";
	return $rv;
	}
else {
	# Just in one column
	local $rv = "<!--grid-->";
	$rv .= "<b>$title</b><br>\n" if ($title);
	for(my $i=0; $i<@$elements; $i++) {
		$rv .= $elements->[$i]."<br>\n";
		}
	return $rv;
	}
}

sub theme_print_iui_head
{
if (&theme_use_iui()) {
        # CSS and Javascript headers for IUI
	print "<meta name='viewport' content='width=320; ".
	      "initial-scale=1.0; maximum-scale=1.0; user-scalable=0;'/>\n";
	print "<style type='text/css' media='screen'>".
	      "\@import '$gconfig{'webprefix'}/unauthenticated/iui/iui.css';".
	      "</style>\n";
	print "<script type='application/x-javascript' ".
              "src='$gconfig{'webprefix'}/unauthenticated/iui/iui.js'>".
	      "</script>\n";
	print "<link rel='apple-touch-icon' ".
	      "href='$gconfig{'webprefix'}/unauthenticated/iphone-icon.png'>\n";
	}
}

sub theme_header
{
print "<!doctype html public \"-//W3C//DTD HTML 3.2 Final//EN\">\n";
print "<html>\n";
local $os_type = $gconfig{'real_os_type'} || $gconfig{'os_type'};
local $os_version = $gconfig{'real_os_version'} || $gconfig{'os_version'};

# Head section with title
print "<head>\n";
if ($charset) {
	print "<meta http-equiv=\"Content-Type\" ",
	      "content=\"text/html; Charset=$charset\">\n";
	}
&theme_print_iui_head();
if (@_ > 0) {
	# Output page title
	local $title = $_[0];
        if ($gconfig{'showlogin'} && $remote_user) {
        	$title = $remote_user." : ".$title;
		}
        print "<title>$title</title>\n";
	print $_[7] if ($_[7]);
	}
print "</head>\n";

# Start of the body
local $bgcolor = "ffffff";
local $link = "0000ee";
local $text = "000000";
local $dir = $current_lang_info->{'dir'} ? "dir=\"$current_lang_info->{'dir'}\""
					 : "";
if (&theme_use_iui()) {
	print "<body $dir $_[8]>\n";
	}
else {
	print "<body bgcolor=#$bgcolor link=#$link vlink=#$link ".
	      "text=#$text $dir $_[8]>\n";
	}
local $hostname = &get_display_hostname();
local $version = &get_webmin_version();

# These get used by the footer function
$theme_iui_toolbar_title = undef;
$theme_iui_toolbar_index = undef;
$theme_iui_toolbar_button = undef;

if (@_ > 1 && &theme_use_iui()) {
	# For IUI

	# Save entries for toolbar, for rendering in footer
	$theme_iui_toolbar_title = $_[0];

	if (!$_[4] && !$tconfig{'nomoduleindex'} &&
	    $module_name ne "virtual-server" &&
	    $module_name ne "server-manager" &&
	    $module_name ne "mailbox") {
		# Module index
		local $idx = $module_info{'index_link'};
		local $mi = $module_index_link || "/$module_name/$idx";
		local $mt = $module_index_name || $text{'header_module'};
		$theme_iui_toolbar_index = $mi;
		}

	if (ref($_[2]) eq "ARRAY" && !$ENV{'ANONYMOUS_USER'} &&
	    !$tconfig{'nohelp'}) {
		# Help in other module
		$theme_iui_toolbar_button = [ "/help.cgi/$_[2]->[0]/$_[2]->[1]",
					      "Help" ];
		}
	elsif (defined($_[2]) && !$ENV{'ANONYMOUS_USER'} &&
	       !$tconfig{'nohelp'}) {
		# Page help
		$theme_iui_toolbar_button = [
			"/help.cgi/$module_name/$_[2]", "Help" ];
		}

	if ($_[3]) {
		# Module Config
		local %access = &get_module_acl();
		if (!$access{'noconfig'} && !$config{'noprefs'}) {
			local $cprog = $user_module_config_directory ?
					"uconfig.cgi" : "config.cgi";
			local $cname = $cprog eq "uconfig.cgi" ? "Prefs"
							       : "Config";
			$theme_iui_toolbar_button =
			    [ "/$cprog?$module_name", $cname ];
			}
		}

	# Open default div for page text
	if (!$main::theme_iui_no_default_div) {
		print "<div class='panel' selected='true' title='$_[0]'>\n";
		}

	# Below and right-side links
	if ($_[6] || $_[9]) {
		local @linksr = split(/<br>\s*/, $_[6]);
		print "<div class=linksbar>\n";
		if ($_[9]) {
			print "<h1>$_[9]</h1>\n";
			}
		if (@linksr) {
			print "<table width=100%><tr>\n";
			foreach my $l (@linksr) {
				print "<td class=linksrow>$l</td>\n";
				}
			print "</tr></table>\n";
			}
		print "</div>\n";
		}
	}
else {
	# For other mobile browsers
	# Show the title
	print "<center><b>$_[0]</b>";
	print "<br>$_[9]\n" if ($_[9]);
	print "</center>\n";

	# Work out links for top
	local @links;
	if ($ENV{'HTTP_WEBMIN_SERVERS'} && !$tconfig{'framed'}) {
		push(@links, "<a href='$ENV{'HTTP_WEBMIN_SERVERS'}'>".
			     "$text{'header_servers'}</a>");
		}
	if (!$_[5] && !$tconfig{'noindex'} &&
	    $module_name ne "virtual-server" &&
	    $module_name ne "server-manager" &&
	    $module_name ne "mailbox") {
		# Logout or switch user
		local @avail = &get_available_module_infos(1);
		local $nolo = $ENV{'ANONYMOUS_USER'} ||
			      $ENV{'SSL_USER'} || $ENV{'LOCAL_USER'} ||
			      $ENV{'HTTP_USER_AGENT'} =~ /webmin/i;
		if ($gconfig{'gotoone'} && $main::session_id && @avail == 1 &&
		    !$nolo) {
			push(@links, "<a href='$gconfig{'webprefix'}/session_login.cgi?logout=1'>$text{'main_logout'}</a>");
			}
		elsif ($gconfig{'gotoone'} && @avail == 1 && !$nolo) {
			push(@links, "<a href=$gconfig{'webprefix'}/switch_user.cgi>$text{'main_switch'}</a>");
			}
		elsif (!$gconfig{'gotoone'} || @avail > 1) {
			push(@links, "<a href='$gconfig{'webprefix'}/?cat=$module_info{'category'}'>$text{'header_webmin'}</a>");
			}
		}
	if (!$_[4] && !$tconfig{'nomoduleindex'} &&
	    $module_name ne "virtual-server" &&
	    $module_name ne "server-manager" &&
	    $module_name ne "mailbox") {
		# Module index
		local $idx = $module_info{'index_link'};
		local $mi = $module_index_link || "/$module_name/$idx";
		local $mt = $module_index_name || $text{'header_module'};
		push(@links, "<a href=\"$gconfig{'webprefix'}$mi\">$mt</a>");
		}
	if (ref($_[2]) eq "ARRAY" && !$ENV{'ANONYMOUS_USER'} &&
	    !$tconfig{'nohelp'}) {
		# Help in other module
		push(@links, &hlink($text{'header_help'}, $_[2]->[0], $_[2]->[1]));
		}
	elsif (defined($_[2]) && !$ENV{'ANONYMOUS_USER'} &&
	       !$tconfig{'nohelp'}) {
		# Page help
		push(@links, &hlink($text{'header_help'}, $_[2]));
		}
	if ($_[3]) {
		# Module Config
		local %access = &get_module_acl();
		if (!$access{'noconfig'} && !$config{'noprefs'}) {
			local $cprog = $user_module_config_directory ?
					"uconfig.cgi" : "config.cgi";
			push(@links, "<a href=\"$gconfig{'webprefix'}/$cprog?$module_name\">$text{'header_config'}</a>");
			}
		}

	# Print all links as a list
	push(@links, split(/<br>/, $_[6]));
	if (@links) {
		if (!defined(&ui_links_row)) {
			do '../ui-lib.pl';
			}
		print &ui_links_row(\@links),"<p>\n";
		}
	}
}

sub theme_post_init_config
{
if ($module_name eq "virtual-server") {
	# Don't show quotas on Virtualmin menu
	$config{'show_quotas'} = 0;
	}
if (&theme_use_iui()) {
	# Don't limit text box sizes on IUI
	$tconfig{'maxboxwidth'} = undef;
	$tconfig{'maxareawidth'} = undef;
	}
}

# Output text-only selector
sub theme_ui_radio_selector
{
local ($opts, $name, $sel) = @_;
foreach my $o (@$opts) {
	$rv .= &ui_oneradio($name, $o->[0], $o->[1], $sel eq $o->[0])."<br>\n";
	$rv .= $o->[2];
	}
return $rv;
}

sub theme_ui_buttons_start
{
return "";
}

sub theme_ui_buttons_end
{
return "";
}

sub theme_ui_buttons_row
{
local ($script, $label, $desc, $hiddens, $after, $before) = @_;
return "<form action=$script>\n".
       $hiddens.
       ($before ? $before." " : "").
       &ui_submit($label).($after ? " ".$after : "")."<br>\n".
       $desc."<p>\n".
       "</form>\n";
}

sub theme_ui_buttons_hr
{
local ($title) = @_;
local $rv;
$rv .= "<b>$title</b><br>\n" if ($title);
$rv .= "<hr>\n";
return $rv;
}

# theme_ui_opt_textbox(name, value, size, option1, [option2], [disabled?],
#		 [&extra-fields], [max])
# Returns HTML for a text field that is optional
sub theme_ui_opt_textbox
{
local ($name, $value, $size, $opt1, $opt2, $dis, $extra, $max) = @_;
local $rv;
$size = &ui_max_text_width($size);
$rv .= &ui_radio($name."_def", $value eq '' ? 1 : 0,
		 [ [ 1, $opt1 ],
		   [ 0, $opt2 || " " ] ], $dis)."\n";
$rv .= "<input name=\"".&quote_escape($name)."\" ".
       "size=$size value=\"".&quote_escape($value)."\" ".
       ($dis ? "disabled=true" : "").
       ($max ? " maxlength=$max" : "").">\n";
return $rv;
}

# theme_virtualmin_ui_rating_selector(name, value, max, cgi)
sub theme_virtualmin_ui_rating_selector
{
local ($name, $value, $max, $cgi) = @_;
local $rv;
for($i=1; $i<=$max; $i++) {
	local $char = $i <= $value ? "X" : "-";
	if ($cgi) {
		local $cgiv = $cgi;
		$cgiv .= ($cgi =~ /\?/ ? "&" : "?");
		$cgiv .= $name."=".$i;
		$rv .= "<a href='$cgiv' id=$name$i>$char</a>";
		}
	else {
		$rv .= $char;
		}
	}
return $rv;
}

sub theme_ui_submit
{
local ($label, $name, $dis, $tags) = @_;
local $style = &theme_use_iui() ? "style='font-size: 12px'"
				: "style='font-size: 8px'";
return "<input type=submit".
       ($name ne '' ? " name=\"".&quote_escape($name)."\"" : "").
       " value=\"".&quote_escape($label)."\"".
       ($dis ? " disabled=true" : "").
       ($tags ? " ".$tags : "")." ".$style.">\n";
}

# On the mail sending page, use a text box for addresses to save space
sub theme_ui_textarea
{
local ($name, $value, $rows, $cols, $wrap, $dis, $tags) = @_;
if ($module_name eq "mailbox" && $0 =~ /reply_mail.cgi/ &&
    ($name eq "to" || $name eq "cc" || $name eq "bcc")) {
	$value =~ s/\n/ /g;
	return &ui_textbox($name, $value, $cols, $dis, undef, $tags);
	}
else {
	$cols = &ui_max_text_width($cols, 1);
	return "<textarea name=\"".&quote_escape($name)."\" ".
	       "rows=$rows cols=$cols".($wrap ? " wrap=$wrap" : "").
	       ($dis ? " disabled=true" : "").
	       ($tags ? " $tags" : "").">".
	       &html_escape($value).
	       "</textarea>";
	}
}



# Popup buttons don't work
sub theme_modules_chooser_button
{
return undef;
}
sub theme_file_chooser_button
{
return undef;
}
sub theme_user_chooser_button
{
return undef;
}
sub theme_group_chooser_button
{
return undef;
}
sub theme_date_chooser_button
{
return undef;
}
sub theme_address_button
{
return undef;
}

# Function overrides for Read Mail usermin module
sub theme_left_right_align
{
return $_[0]." ".$_[1];
}
sub theme_show_arrows
{
local %ttext = &load_language($current_theme);
if (!@sub) {
	# Get next and previous emails, where they exist
	local $c = &mailbox_folder_size($folder, 1);
	local $prv = $mail->{'sortidx'} == 0 ? 0 : $mail->{'sortidx'}-1;
	local $nxt = $mail->{'sortidx'} == $c-1 ? $c-1 : $mail->{'sortidx'}+1;
	local @beside = &mailbox_list_mails_sorted($prv, $nxt, $folder, 1);

	if ($mail->{'sortidx'} != 0) {
		local $mailprv = $beside[$prv];
		print "<a href='view_mail.cgi?id=",&urlize($mailprv->{'id'}),
		      "&folder=$in{'folder'}&start=$in{'start'}'>",
		      "&lt;$ttext{'mail_next'}</a>";
		}
	else {
		print "&lt;$ttext{'mail_next'}\n";
		}
	print " | ",&text('view_desc', $mail->{'sortidx'}+1,
				       $folder->{'name'})," | ";
	if ($mail->{'sortidx'} < $c-1) {
		local $mailnxt = $beside[$nxt];
		print "<a href='view_mail.cgi?id=",&urlize($mailnxt->{'id'}),
		      "&folder=$in{'folder'}&start=$in{'start'}'>",
		      "$ttext{'mail_prev'}&gt;</a>";
		}
	else {
		print "$ttext{'mail_prev'}&gt;\n";
		}
	}
else {
	print $text{'view_sub'},"\n";
	}
print "<br>\n";
}
sub theme_show_buttons
{
# Show links for common actions on a single mail
local %ttext = &load_language($current_theme);
local @bacts;
local $url = "reply_mail.cgi?id=".&urlize($in{'id'}).
	     "&folder=".&urlize($in{'folder'}).
	     "&body=".&urlize($in{'body'}).
	     "&start=".&urlize($in{'start'});
foreach my $s (@sub) {
	$url .= "&sub=$s";
	}
if ($folder->{'sent'} || $folder->{'drafts'}) {
	push(@bacts, "<a href='$url&enew=1'>$text{'view_enew'}</a>");
	push(@bacts, "<a href='$url&ereply=1'>$text{'view_reply'}</a>");
	push(@bacts, "<a href='$url&erall=1'>$text{'view_reply2'}</a>");
	}
else {
	push(@bacts, "<a href='$url&reply=1'>$text{'view_reply'}</a>");
	push(@bacts, "<a href='$url&rall=1'>$text{'view_reply2'}</a>");
	}
push(@bacts, "<a href='$url&new=1'>$text{'mail_compose'}</a>");
push(@bacts, "<a href='$url&forward=1'>$text{'view_forward'}</a>");
if (!$_[1]) {
	# Show mark buttons, except for current mode
	if (!$folder->{'sent'} && !$folder->{'drafts'}) {
		$m = &get_mail_read($folder, $mail);
		foreach $i (0 .. 2) {
			if ($m != $i) {
				push(@bacts, "<a href='$url&markas$i=1'>".
					     $ttext{'mail_markas'.$i}."</a>");
				}
			}
		}
	}
if (!$_[1]) {
	# Show spam and/or ham report buttons
	if (&can_report_spam($folder) &&
	    $userconfig{'spam_buttons'} =~ /mail/) {
		if ($userconfig{'spam_del'}) {
			push(@bacts, "<a href='$url&razor=1'>$text{'view_razordel'}</a>");
			}
		else {
			push(@bacts, "<a href='$url&razor=1'>$text{'view_razor'}</a>");
			}
		}
	if (&can_report_ham($folder) &&
	    $userconfig{'ham_buttons'} =~ /mail/) {
		if ($userconfig{'white_move'} && $folder->{'spam'}) {
			push(@bacts, "<a href='$url&white=1'>$text{'view_whitemove'}</a>");
			}
		else {
			push(@bacts, "<a href='$url&white=1'>$text{'view_white'}</a>");
			}
		if ($userconfig{'ham_move'} && $folder->{'spam'}) {
			push(@bacts, "<a href='$url&ham=1'>$text{'view_hammove'}</a>");
			}
		else {
			push(@bacts, "<a href='$url&ham=1'>$text{'view_ham'}</a>");
			}
		}
	}
if (@folders > 1) {
	push(@bacts, "<a href='action_mail.cgi?ok1=1&action1=move&folder=$in{'folder'}&start=$in{'start'}&d=$in{'id'}'>$ttext{'view_move'}</a>");
	push(@bacts, "<a href='action_mail.cgi?ok1=1&action1=copy&folder=$in{'folder'}&start=$in{'start'}&d=$in{'id'}'>$ttext{'view_copy'}</a>");
	}
if (!@subs) {
	push(@bacts, "<a href='$url&delete=1'>$text{'view_delete'}</a>");
	}
print "<b>$ttext{'view_actions'}</b> ",
      join(" | ", @bacts),"<br>\n";
}
if ($module_name eq "mailbox" &&
    $0 =~ /((view|reply)_mail.cgi|search_form.cgi)/) {
	# UI overrides for viewing email
	$main::{'left_right_align'} = \&theme_left_right_align;
	$mailbox::{'left_right_align'} = \&theme_left_right_align;
	$main::{'search_link'} = sub { return "" };
	$mailbox::{'search_link'} = sub { return "" };
	$main::{'show_arrows'} = \&theme_show_arrows;
	$mailbox::{'show_arrows'} = \&theme_show_arrows;
	$main::{'show_buttons'} = \&theme_show_buttons;
	$mailbox::{'show_buttons'} = \&theme_show_buttons;

	local %ttext = &load_language($current_theme);
	$text{'view_noheaders'} = $ttext{'view_noheaders'};
	$text{'view_allheaders'} = $ttext{'view_allheaders'};
	$text{'view_raw'} = $ttext{'view_raw'};
	$text{'sform_and'} = $ttext{'search_and'};
	$text{'sform_or'} = $ttext{'search_or'};

	# To supress HTML compose links
	$text{'reply_html0'} = undef;
	$text{'reply_html1'} = undef;

	# Never use HTML editor
	$userconfig{'head_html'} = 0;
	$userconfig{'html_edit'} = 0;
	$userconfig{'view_html'} = 1;

	# Only show one set of send buttons
	$userconfig{'send_buttons'} = 0;
	}

sub theme_virtualmin_ui_show_cron_time
{
local ($name, $job, $offmsg) = @_;
&foreign_require("cron", "cron-lib.pl");
local $rv;
local $mode = !$job ? 0 : $job->{'special'} ? 1 : 2;
local $hidden = $mode == 2 ?
	join(" ", $job->{'mins'}, $job->{'hours'},
		  $job->{'days'}, $job->{'months'}, $job->{'weekdays'}) : "";
return &ui_radio_table($name, $mode,
	 [ $offmsg ? ( [ 0, $offmsg ] ) : ( ),
	   [ 1, $text{'cron_special'},
		   &ui_select($name."_special", $job->{'special'},
		      [ map { [ $_, $cron::text{'edit_special_'.$_} ] }
			    ('hourly', 'daily', 'weekly', 'monthly', 'yearly')
		      ]) ],
	   [ 2, $text{'cron_cron'},
		   &ui_textbox($name."_hidden", $hidden) ],
	 ]);
}

sub theme_use_iui
{
return $ENV{'HTTP_USER_AGENT'} =~ /iPhone|iPod|Android/;
}

sub theme_popup_header
{
print "<!doctype html public \"-//W3C//DTD HTML 3.2 Final//EN\">\n";
print "<html>\n";
print "<head>\n";
&theme_print_iui_head();
print "<title>$_[0]</title>\n";
print $_[1];
print "</head>\n";
local $bgcolor = defined($tconfig{'cs_page'}) ? $tconfig{'cs_page'} :
		 defined($gconfig{'cs_page'}) ? $gconfig{'cs_page'} : "ffffff";
local $link = defined($tconfig{'cs_link'}) ? $tconfig{'cs_link'} :
	      defined($gconfig{'cs_link'}) ? $gconfig{'cs_link'} : "0000ee";
local $text = defined($tconfig{'cs_text'}) ? $tconfig{'cs_text'} : 
	      defined($gconfig{'cs_text'}) ? $gconfig{'cs_text'} : "000000";
local $bgimage = defined($tconfig{'bgimage'}) ? "background=$tconfig{'bgimage'}"
					      : "";
if (&theme_use_iui()) {
	print "<body $_[2]>\n";
	print "<div class='toolbar'>\n";
	print "<h1 id='pageTitle'>$_[0]</h1>\n";
	print "<a id='backButton' class='button' href='#'></a>\n";
	print "</div>\n";
	if (!$main::theme_iui_no_default_div) {
		print "<div class='panel' selected='true' title='$_[0]'>\n";
		}
	}
else {
	print "<body id='popup' bgcolor=#$bgcolor link=#$link vlink=#$link ",
	      "text=#$text $bgimage $tconfig{'inbody'} $_[2]>\n";
	}
}

sub theme_popup_footer
{
if (&theme_use_iui() && !$main::theme_iui_no_default_div) {
	print "</div>\n";
	}
print "</body></html>\n";
}

sub theme_hlink
{
local $mod = $_[2] ? $_[2] : $module_name;
return "<a href='/help.cgi/$mod/$_[1]' target=_new ".
       "class='webminHelpLink'>$_[0]</a>";
}

# Turn off javascript redirects
sub theme_js_redirect
{
return "";
}

# theme_ui_multi_select(name, &values, &options, size, [add-if-missing],
#		        [disabled?], [options-title, values-title], [width])
sub theme_ui_multi_select
{
local ($name, $values, $opts, $size, $missing, $dis,
       $opts_title, $vals_title, $width) = @_;
if (&theme_use_iui()) {
	# For IUI, use checkboxes
	my $rv;
	my %already = map { $_->[0], $_ } @$values;
	if (!$main::theme_ui_multi_select_donejs++) {
		$rv .= &theme_ui_multi_select_javascript();
		}
	local $qname = &quote_escape($name);
	local $js = "onClick='multi_select_change(\"$qname\", form)'";
	foreach my $o (@$opts) {
		$rv .= &ui_checkbox($name."_checkbox", $o->[0], $o->[1],
				    $already{$o->[0]}, $js)."<br>\n";
		delete($already{$o->[0]});
		}
	foreach my $o (values %$already) {
		$rv .= &ui_checkbox($name."_checkbox", $o->[0], $o->[1],
				    1, $js)."<br>\n";
		}
	$rv .= &ui_hidden($name, join("\n", map { $_->[0] } @$values));
	return $rv;
	}
else {
	# The Javascript left/right selector isn't supported, so don't even
	# try to use it.
	return &ui_textarea($name, join("\n", map { $_->[0] } @$values),
			    $size, 30, "off", $dis);
	}
}

sub theme_ui_multi_select_javascript
{
return <<EOF;
<script>
function multi_select_change(name, f)
{
var v = [ ];
var vals = f.elements[name];
for(var i=0; i<f.elements.length; i++) {
	var e = f.elements[i];
	if (e.name == name+"_checkbox" && e.checked) {
		v.push(e.value);
		}
	}
vals.value = v.join("\\n");
}
</script>
EOF
}

# theme_ui_radio_table(name, selected, &rows)
# Returns HTML for a table of radio buttons, each of which has a label and
# some associated inputs to the right.
sub theme_ui_radio_table
{
local ($name, $sel, $rows) = @_;
return "" if (!@$rows);
my $rv;
foreach my $r (@$rows) {
	$rv .= "<b>".&ui_oneradio($name, $r->[0], $r->[1],
				  $r->[0] eq $sel)."</b><br>\n";
	if ($r->[2]) {
		$rv .= "&nbsp;&nbsp;".$r->[2]."<br>\n";
		}
	}
return $rv;
}

1;

