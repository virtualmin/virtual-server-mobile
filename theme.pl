# Theme-level UI override functions

# Disable buttons on edit_domain page
$main::basic_virtualmin_domain = 1;

# Disable other links on virtualmin module main page
$main::basic_virtualmin_menu = 1;

sub theme_ui_post_header
{
local ($text) = @_;
local $rv;
if ($text) {
	$rv .= "<b>$text</b><p>\n";
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
local $count = 0;
for($i=0; $i+1<@_; $i+=2) {
	local $url = $_[$i];
	if ($url ne '/' || !$tconfig{'noindex'}) {
		if ($url eq '/') {
			$url = "/?cat=$module_info{'category'}";
			}
		elsif ($url eq '' && $module_name eq 'virtual-server' ||
		       $url eq '/virtual-server/') {
			# Don't bother with virtualmin menu
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
		$url = "$gconfig{'webprefix'}$url" if ($url =~ /^\//);
		print "&nbsp;|\n" if ($count++);
		print "&nbsp;<a href=\"$url\">",&text('main_return', $_[$i+1]),"</a>\n";
		}
	}
print "<br>\n";
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
$rv .= "<font size=+1>$heading</font><br>\n" if (defined($heading));
$rv .= "<hr>\n";
$main::ui_table_cols = 2;
$main::ui_table_pos = 0;
return $rv;
}

# theme_ui_table_end()
# The end of a table started by ui_table_start
sub theme_ui_table_end
{
return "<hr>\n";
}


# theme_ui_table_row(label, value, [cols], [&td-tags])
# Returns HTML for a row in a table started by ui_table_start, with a 1-column
# label and 1+ column value.
sub theme_ui_table_row
{
local ($label, $value, $cols) = @_;
local $rv;
$rv .= "<b>$label</b><br>\n" if (defined($label));
#$rv .= "&nbsp;&nbsp;" if (defined($label) &&
#			  $value !~ /^\s*<table/ &&
#			  $value !~ /^\s*<!--grid/);
$rv .= "$value<br>\n";
return $rv;
}

# theme_ui_hidden_table_start
# Just outputs a normal table start, as mobile browsers don't support CSS
sub theme_ui_hidden_table_start
{
local ($heading, $tabletags, $cols, $name, $status) = @_;
return &theme_ui_table_start($heading, $tabletags, $cols);
}

# theme_ui_columns_start(&headings, [width-percent], [noborder], [&tdtags], [heading])
# Returns HTML for a multi-column table, with the given headings
sub theme_ui_columns_start
{
local ($heads, $width, $noborder, $tdtags, $heading) = @_;
local $rv;
$rv .= "<table".($noborder ? "" : " border").
		(defined($width) ? " width=$width%" : "").">\n";
if ($heading) {
	$rv .= "<font size=+1>$heading</font><br>\n";
	}
$rv .= "<tr>\n";
local $i;
for($i=0; $i<@$heads; $i++) {
	$rv .= "<th ".$tdtags->[$i]."><b>".
	       ($heads->[$i] eq "" ? "<br>" : $heads->[$i])."</b></th>\n";
	}
$rv .= "</tr>\n";
return $rv;
}

# theme_ui_columns_row(&columns, &tdtags)
# Returns HTML for a row in a multi-column table
sub theme_ui_columns_row
{
local ($cols, $tdtags) = @_;
local $rv;
$rv .= "<tr>\n";
local $i;
for($i=0; $i<@$cols; $i++) {
	$rv .= "<td ".$tdtags->[$i].">".
	       ($cols->[$i] eq "" ? "<br>" : $cols->[$i])."</td>\n";
	}
$rv .= "</tr>\n";
return $rv;
}

# theme_ui_columns_header(&columns, &tdtags)
# Returns HTML for a row in a multi-column table, with a header background
sub theme_ui_columns_header
{
local ($cols, $tdtags) = @_;
local $rv;
$rv .= "<tr>\n";
local $i;
for($i=0; $i<@$cols; $i++) {
	$rv .= "<th ".$tdtags->[$i]."><b>".
	       ($cols->[$i] eq "" ? "<br>" : $cols->[$i])."</b></th>\n";
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
$rv .= "<tr>\n";
$rv .= "<td ".$tdtags->[0].">".
       &ui_checkbox($checkname, $checkvalue, undef, $checked)."</td>\n";
local $i;
for($i=0; $i<@$cols; $i++) {
	$rv .= "<td ".$tdtags->[$i+1].">";
	$rv .= ($cols->[$i] eq "" ? "<br>" : $cols->[$i]);
	$rv .= "</td>\n";
	}
$rv .= "</tr>\n";
return $rv;
}

# theme_ui_radio_columns_row(&columns, &tdtags, checkname, checkvalue)
# Returns HTML for a row in a multi-column table, in which the first
# column is a radio button
sub theme_ui_radio_columns_row
{
local ($cols, $tdtags, $checkname, $checkvalue) = @_;
local $rv;
$rv .= "<tr>\n";
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

# theme_ui_links_row(&links)
# Returns HTML for a row of links, like select all / invert selection / add..
sub theme_ui_links_row
{
local ($links) = @_;
local @nn = grep { $_ ne "" } @$links;
return @nn ? join(" | ", @nn)."<br>\n" : "";
}

# theme_ui_print_header(subtext, args...)
# If called with "In domain XXX" as the subtext, put it after the title
sub theme_ui_print_header
{
local ($subtext, @args) = @_;
local $re = $text{'indom'} ||
	    $virtual_server::text{'indom'};
$re =~ s/\$1/\(\\S+\)/;
if ($subtext =~ /$re/) {
	$args[0] .= " [$1]";
	&header(@args);
	}
else {
	&header(@args);
	print &ui_post_header($subtext);
	}
}

sub theme_redirect
{
local ($orig, $url) = @_;
if ($module_name eq "virtual-server" &&
    $url =~ /postsave.cgi\?dom=(\d+)/) {
	$url =~ s/\/([^\/]+)\/postsave.cgi/\/index_edit.cgi/g;
	}
print "Location: $url\n\n";
}

# For each tab, output just a link
sub theme_ui_tabs_start
{
local ($tabs, $name, $sel, $border) = @_;
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

# Doesn't need to return anything for text-mode tabs
sub theme_ui_tabs_end
{
return "";
}

# When in text mode, suppress output unless the named tab is selected
sub theme_ui_tabs_start_tab
{
local ($name, $tab) = @_;
if ($main::current_selected_tab{$name} ne $tab) {
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
if ($main::suppressing_tab) {
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
	print "<li>";
	print $befores->[$i];
	if ($links->[$i]) {
		print "<a href='$links->[$i]' $href>$titles->[$i]</a>";
		}
	else {
		print $titles->[$i];
		}
	print $afters->[$i];
	print "<br>\n";
	}
print "</ul>\n";
}

# Doesn't bother with a grid, just put everything in one column
sub theme_ui_grid_table
{
local ($elements, $cols, $width, $tds) = @_;
return "" if (!@$elements);
local $rv = "<!--grid-->";
for(my $i=0; $i<@$elements; $i++) {
	$rv .= $elements->[$i]."<br>\n";
	}
return $rv;
}

sub theme_header
{
print "<!doctype html public \"-//W3C//DTD HTML 3.2 Final//EN\">\n";
print "<html>\n";
local $os_type = $gconfig{'real_os_type'} ? $gconfig{'real_os_type'}
					  : $gconfig{'os_type'};
local $os_version = $gconfig{'real_os_version'} ? $gconfig{'real_os_version'}
					        : $gconfig{'os_version'};
print "<head>\n";
if ($charset) {
	print "<meta http-equiv=\"Content-Type\" ",
	      "content=\"text/html; Charset=$charset\">\n";
	}
if (@_ > 0) {
	local $title = $_[0];
        if ($gconfig{'showlogin'} && $remote_user) {
        	$title = $remote_user." : ".$title;
		}
        print "<title>$title</title>\n";
	print $_[7] if ($_[7]);
	}
print "</head>\n";
local $bgcolor = "ffffff";
local $link = "0000ee";
local $text = "000000";
local $dir = $current_lang_info->{'dir'} ? "dir=\"$current_lang_info->{'dir'}\""
					 : "";
print "<body bgcolor=#$bgcolor link=#$link vlink=#$link text=#$text $dir $_[8]>\n";
local $hostname = &get_display_hostname();
local $version = &get_webmin_version();
if (@_ > 1) {
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
	    $module_name ne "virtual-server") {
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
	    $module_name ne "virtual-server") {
		local $idx = $module_info{'index_link'};
		local $mi = $module_index_link || "/$module_name/$idx";
		local $mt = $module_index_name || $text{'header_module'};
		push(@links, "<a href=\"$gconfig{'webprefix'}$mi\">$mt</a>");
		}
	if (ref($_[2]) eq "ARRAY" && !$ENV{'ANONYMOUS_USER'} &&
	    !$tconfig{'nohelp'}) {
		push(@links, &hlink($text{'header_help'}, $_[2]->[0], $_[2]->[1]));
		}
	elsif (defined($_[2]) && !$ENV{'ANONYMOUS_USER'} &&
	       !$tconfig{'nohelp'}) {
		push(@links, &hlink($text{'header_help'}, $_[2]));
		}
	if ($_[3]) {
		local %access = &get_module_acl();
		if (!$access{'noconfig'} && !$config{'noprefs'}) {
			local $cprog = $user_module_config_directory ?
					"uconfig.cgi" : "config.cgi";
			push(@links, "<a href=\"$gconfig{'webprefix'}/$cprog?$module_name\">$text{'header_config'}</a>");
			}
		}
	push(@links, split(/<br>/, $_[6]));
	if (@links) {
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

1;

