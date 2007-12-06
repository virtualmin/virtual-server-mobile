#!/usr/local/bin/perl
# Mobile version of mail list

require './mailbox-lib.pl';
&ReadParse();
%ttext = &load_language($current_theme);

&open_dsn_hash();

@folders = &list_folders_sorted();
if (defined($in{'id'})) {
	# Folder ID specified .. convert to index
	$idf = &find_named_folder($in{'id'}, \@folders);
	$in{'folder'} = $idf->{'index'} if ($idf);
	}
elsif (!defined($in{'folder'}) && $userconfig{'default_folder'}) {
	# No folder specified .. find the default by preferences
	$df = &find_named_folder($userconfig{'default_folder'}, \@folders);
	$in{'folder'} = $df->{'index'} if ($df);
	}
# Get the folder by index
($folder) = grep { $_->{'index'} == $in{'folder'} } @folders;

# Show page header
print "Refresh: $userconfig{'refresh'}\r\n"
	if ($userconfig{'refresh'});
($qtotal, $qcount, $totalquota, $countquota) = &get_user_quota();
if ($totalquota) {
	push(@topright, &text('mail_quota', &nice_size($qtotal),
				     &nice_size($totalquota)));
	}
if (($folder->{'type'} == 2 || $folder->{'type'} == 4) &&
    $folder->{'mode'} == 3 && defined($folder->{'user'}) &&
    !$folder->{'autouser'}) {
	push(@topright, "<a href='inbox_logout.cgi?folder=$folder->{'index'}'>".
			($folder->{'type'} == 2 ? $text{'mail_logout'}
						: $text{'mail_logout2'}).
			"</a>");
	}
&ui_print_header(undef, &text('index_title', $folder->{'name'}), "", undef,
		 1, 1, 0, join("<br>", @topright));
print &check_clicks_function();

# Check if this is a POP3 or IMAP inbox with no login set
if (($folder->{'type'} == 2 || $folder->{'type'} == 4) &&
    $folder->{'mode'} == 3 && !$folder->{'autouser'} && !$folder->{'user'}) {
	print &ui_form_start("inbox_login.cgi", "post");
	print &ui_hidden("folder", $folder->{'index'}),"\n";
	print &ui_table_start(
	      $folder->{'type'} == 2 ? $text{'mail_loginheader'}
				     : $text{'mail_loginheader2'}, undef, 2);
	print &ui_table_row(undef, &text('mail_logindesc',
					 "<tt>$folder->{'server'}</tt>"), 2);

	print &ui_table_row($text{'mail_loginuser'},
			    &ui_textbox("user", $remote_user, 30));
	print &ui_table_row($text{'mail_loginpass'},
			    &ui_password("pass", $remote_pass, 30));

	print &ui_table_end();
	print &ui_form_end([ [ "login", $text{'mail_login'} ] ]);

	&ui_print_footer("/", $text{'index'});
	exit;
	}

# Work out start from jump page
$perpage = $folder->{'perpage'} || $userconfig{'perpage'} || 20;
if ($in{'jump'} =~ /^\d+$/ && $in{'jump'} > 0) {
	$in{'start'} = ($in{'jump'}-1)*$perpage;
	}

# View mail in sort order
@mail = &mailbox_list_mails_sorted(
		int($in{'start'}), int($in{'start'})+$perpage-1,
	        $folder, 1, \@error);
if ($in{'start'} >= @mail && $in{'jump'}) {
	# Jumped too far!
	$in{'start'} = @mail - $perpage;
	@mail = &mailbox_list_mails_sorted(int($in{'start'}),
					   int($in{'start'})+$perpage-1,
					   $folder, 1, \@error);
	}

# Show page flipping arrows
&show_arrows();

# Work out displayed range
$start = int($in{'start'});
$end = $in{'start'}+$perpage-1;
$end = scalar(@mail)-1 if ($end >= scalar(@mail));

# Buttons at top
print &ui_form_start("action_mail.cgi", "post");
print &ui_hidden("folder", $folder->{'index'});
print &ui_hidden("mod", &modification_time($folder));
print &ui_hidden("start", $in{'start'});
if ($userconfig{'top_buttons'} && @mail) {
	&text_mailbox_buttons(1, \@folders, $folder, \@mail);
	}

# Show sort links
$showto = $folder->{'show_to'};
$showfrom = $folder->{'show_from'};
if (@mail) {
	@sortlinks = ( );
	if ($showfrom) {
		push(@sortlinks, &text_sort_link($text{'mail_from'}, "from"));
		}
	if ($showto) {
		push(@sortlinks, &text_sort_link($text{'mail_to'}, "to"));
		}
	push(@sortlinks, &text_sort_link($text{'mail_date'}, "date"));
	push(@sortlinks, &text_sort_link($text{'mail_size'}, "size"));
	if ($folder->{'spam'}) {
		push(@sortlinks, &text_sort_link($text{'mail_level'},
					         "x-spam-status"));
		}
	push(@sortlinks, &text_sort_link($text{'mail_subject'}, "subject"));
	($sortfield, $sortdir) = &get_sort_field($folder);
	if ($sortfield) {
		# Show un-sort link
		push(@sortlinks, "<a href='sort.cgi?folder=$folder->{'index'}&start=$start'>$ttext{'mail_nosort'}</a>");
		}
	print "<b>$ttext{'mail_sortby'}</b>\n",
	      join(" | ", grep { $_ } @sortlinks),"<p>\n";
	}
if (@error) {
	print "<b><font color=#ff0000>\n";
	print &text('mail_err', $error[0] == 0 ? $error[1] :
			      &text('save_elogin', $error[1])),"\n";
	print "</font></b>\n";
	}

# Construct a block for each email
for(my $i=$start; $i<=$end; $i++) {
	local ($bs, $be);
	$m = $mail[$i];
	$mid = $m->{'header'}->{'message-id'};
	$r = &get_mail_read($folder, $m);
	if ($r == 2) {
		# Special
		($bs, $be) = ("<b><i>", "</i></b>");
		}
	elsif ($r == 0) {
		# Unread
		($bs, $be) = ("<b>", "</b>");
		}
	&notes_decode($m, $folder);
	local $idx = $m->{'idx'};
	local $id = $m->{'id'};
	local @cols;

	# Checkbox for deleting
	if (&editable_mail($m)) {
		print &ui_checkbox("d", $id, "", 0);
		}

	# From and To addresses, with links
	if ($showfrom) {
		print "<b>$text{'mail_from'}</b>: " if ($showto);
		print $bs.&view_mail_link($folder, $id, $in{'start'},
                                      $m->{'header'}->{'from'}).$be."<br>\n";
		}
	if ($showto) {
		print "<b>$text{'mail_to'}</b>: " if ($showfrom);
		print $bs.&view_mail_link($folder, $id, $in{'start'},
		      $m->{'header'}->{'to'}).$be."<br>\n";
		}

	# Subject column, with read/special icons
	local @icons = &message_icons($m, $folder->{'sent'}, $folder);
	if ($m->{'header'}->{'subject'} =~ /\S/ || @icons) {
		print &simplify_subject($m->{'header'}->{'subject'}).
		      join("", @icons)."<br>\n";
		}

	# Date and size 
	print "<b>$text{'mail_date'}</b>: ".
	      &simplify_date($m->{'header'}->{'date'})."\n";
	print "<b>$text{'mail_size'}</b>: ".
	      &nice_size($m->{'size'}, 1024)."\n";

	# Spam score
	if ($folder->{'spam'} &&
	    $m->{'header'}->{'x-spam-status'} =~ /(hits|score)=([0-9\.]+)/) {
		print "<b>$text{'mail_score'}</b> : ".$2."\n";
		}
	print "<br>\n";

	&update_delivery_notification($mail[$i], $folder);

	# Show part of the body too
	if ($userconfig{'show_body'}) {
		&parse_mail($m);
		local $data = &mail_preview($m);
                if ($data) {
			print "<i>".&html_escape($data)."</i><br>\n";
                        }
		}
	}
print "<p>\n" if (@mail);

# Buttons at end of form
&text_mailbox_buttons(2, \@folders, $folder, \@mail);
print &ui_form_end();

if ($userconfig{'arrows'}) {
	# Show page flipping arrows
	print "<br>\n";
	&show_arrows();
	}

# Other actions
@oacts = ( );

# Address book button
if (!$main::mailbox_no_addressbook_button) {
	push(@oacts, "<a href='list_addresses.cgi'>".
		     "$ttext{'mail_addresses'}</a>");
	}

# Folder management button
if (!$main::mailbox_no_folder_button) {
	if ($config{'mail_system'} == 4) {
		push(@oacts, "<a href='list_ifolders.cgi'>".
			     "$ttext{'mail_folders'}</a>");
		}
	else {
		push(@oacts, "<a href='list_folders.cgi'>".
			     "$ttext{'mail_folders'}</a>");
		}
	}

# Sig editor
if (&get_signature_file()) {
	push(@oacts, "<a href='edit_sig.cgi'>$ttext{'mail_sig'}</a>");
	}

# Show button to delete all mail in folder
if (@mail && ($folder->{'trash'} || $userconfig{'show_delall'})) {
	push(@oacts, "<a href='delete_mail.cgi?folder=$folder->{'index'}".
		     "&all=1&delete=1'>".
		     ($folder->{'trash'} ? $text{'mail_deltrash'}
                                         : $text{'mail_delall'})."</a>");
	}

if (@oacts) {
	print "<b>$ttext{'mail_oacts'}</b> ",
	      join(" | ", @oacts),"<p>\n";
	}

# Show search / jump actions
if (@mail) {
	$jumpform = (@mail > $perpage);
	if ($folder->{'searchable'}) {
		# Simple search
		$ssform = &ui_form_start("mail_search.cgi");
		$ssform .= &ui_hidden("folder", $folder->{'index'});
		$ssform .= &ui_hidden("simple", 1);
		$ssform .= &ui_submit($text{'mail_search2'});
		$ssform .= &ui_textbox("search", undef, 20);
		$ssform .= &ui_form_end();
		print $ssform;

		# Advanced search
		print &ui_form_start("search_form.cgi").
		      &ui_hidden("folder", $folder->{'index'}).
		      &ui_submit($text{'mail_advanced'}, "advanced").
		      &ui_form_end();
		}

	if ($folder->{'spam'} && $folder->{'searchable'}) {
		# Spam level search
		print &ui_form_start("mail_search.cgi").
		      &ui_hidden("folder", $folder->{'index'}).
		      &ui_hidden("spam", 1).
		      &ui_submit($text{'mail_search3'}).
		      &ui_textbox("score", undef, 5).
		      &ui_form_end();
		}
	if ($jumpform) {
		# Show page jump form
		print &ui_form_start("index.cgi").
		      &ui_hidden("folder", $folder->{'index'}).
		      &ui_submit($text{'mail_jump'}).
		      &ui_textbox("jump", int($in{'start'} / $perpage)+1, 3).
				  " $text{'mail_of'} ".
			          (int(@mail / $perpage)+1).
		      &ui_form_end();
		}
	}

&ui_print_footer("/", $text{'index'});
&pop3_logout();

# show_arrows()
# Prints HTML for previous/next page arrows (text only)
sub show_arrows
{
# Show left arrow to go to start of folder
if ($in{'start'}) {
	printf "<a href='index.cgi?start=%d&folder=%d'>%s</a>\n",
		0, $in{'folder'}, "&lt;&lt;";
	}
else {
	print "&lt;&lt;\n";
	}

# Show left arrow to decrease start
if ($in{'start'}) {
	printf "<a href='index.cgi?start=%d&folder=%d'>%s</a>\n",
		$in{'start'}-$perpage, $in{'folder'}, "&lt;$ttext{'mail_next'}";
	}
else {
	print "&lt;$ttext{'mail_next'}\n";
	}

local $s = $in{'start'}+1;
local $e = $in{'start'}+$perpage;
$e = scalar(@mail) if ($e > @mail);
$text{'mail_pos'} = $ttext{'mail_pos'};
$text{'mail_none'} = $ttext{'mail_none'};
if (@mail) {
	print " | ",&text('mail_pos', $s, $e, scalar(@mail))," | ";
	}
else {
	print " | ",&text('mail_none')," | ";
	}
print "\n";

# Show right arrow to increase start
if ($in{'start'}+$perpage < @mail) {
	printf "<a href='index.cgi?start=%d&folder=%d'>%s</a>\n",
		$in{'start'}+$perpage, $in{'folder'}, "$ttext{'mail_prev'}&gt;";
	}
else {
	print "$ttext{'mail_prev'}&gt;\n";
	}

# Show right arrow to go to end
if ($in{'start'}+$perpage < @mail) {
	printf "<a href='index.cgi?start=%d&folder=%d'>%s</a>\n",
		int((scalar(@mail)-$perpage-1)/$perpage + 1)*$perpage,
		$in{'folder'}, "&gt;&gt;";
	}
else {
	print "&gt;&gt;";
	}

if ($folder->{'msg'}) {
	print "<br>$folder->{'msg'}\n";
	}
print "<p>\n";
}

sub text_sort_link
{
local ($title, $field) = @_;
local ($sortfield, $sortdir) = &get_sort_field($folder);
local $dir = $sortfield eq $field ? !$sortdir : 0;
if ($folder->{'sortable'}) {
        return ($sortfield eq $field ? "<i>" : "").
	       ("<a href='sort.cgi?field=$field&dir=$dir&folder=$folder->{'index'}&start=$in{'start'}'>$title</a>").
	       ($sortfield eq $field ? "</i>" : "");
        }
else {
	return undef;
        }
}

# text_mailbox_buttons(number, &folders, current-folder, &mail)
# Prints HTML for buttons to appear above or below a mail list
sub text_mailbox_buttons
{
local ($num, $folders, $folder, $mail) = @_;
local $spacer = "&nbsp;\n";

# Build actions menu
local @acts;
push(@acts, [ "new", $text{'mail_compose'} ]);
if (@mail) {
	push(@acts, [ "forward", $text{'mail_forward'} ]);
	foreach my $i (0 .. 2) {
		push(@acts, [ "markas".$i, $ttext{'mail_markas'.$i} ]);
		}
	}
if (@mail && @$folders > 1) {
	push(@acts, [ "move", $ttext{'mail_move'} ]);
	push(@acts, [ "copy", $ttext{'mail_copy'} ]);
	}
if (@mail) {
	push(@acts, [ "delete", $text{'mail_delete'} ]);
	}
if (@mail && (&can_report_spam($folder) &&
    	      $userconfig{'spam_buttons'} =~ /list/ || $folder->{'spam'})) {
	push(@acts, [ "delete", $text{'mail_black'} ]);
	if ($userconfig{'spam_del'}) {
		push(@acts, [ "razor", $text{'view_razordel'} ]);
		}
	else {
		push(@acts, [ "razor", $text{'view_razor'} ]);
		}
	}

# Whitelist / report ham
if (@mail && (&can_report_ham($folder) &&
	      $userconfig{'ham_buttons'} =~ /list/ ||
	      $folder->{'spam'})) {
	if ($userconfig{'white_move'} && $folder->{'spam'}) {
		push(@acts, [ "white", $text{'mail_whitemove'} ]);
		}
	else {
		push(@acts, [ "white", $text{'mail_white'} ]);
		}
	if ($userconfig{'ham_move'} && $folder->{'spam'}) {
		push(@acts, [ "ham", $text{'view_hammove'} ]);
		}
	else {
		push(@acts, [ "ham", $text{'view_ham'} ]);
		}
	}

# Actions menu
print "<b>$ttext{'mail_actions'}</b>\n";
print &ui_select("action".$num, undef, \@acts);
print &ui_submit($ttext{'mail_ok'}, "ok".$num),"<br>\n";
}


