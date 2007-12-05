#!/usr/local/bin/perl
# Redirect to delete_mail.cgi with correct params

require './mailbox-lib.pl';
&ReadParse();
@d = split(/\0/, $in{'d'});
%ttext = &load_language($current_theme);

if ($in{'action'} eq 'move' || $in{'action'} eq 'copy') {
	# Show dest form
	&ui_print_header(undef, $ttext{'action_title'.$in{'action'}}, "");

	print &ui_form_start("delete_mail.cgi", "post");
	print &ui_hidden("folder", $in{'folder'});
	print &ui_hidden("start", $in{'start'});
	foreach $d (@d) {
		print &ui_hidden("d", $d);
		}
	print &ui_hidden($in{'action'}."1", 1);

	# Source folder
	@folders = &list_folders_sorted();
	($folder) = grep { $_->{'index'} == $in{'folder'} } @folders;
	print &ui_table_row($ttext{'action_src'},
			    $folder->{'name'});

	# Dest folder
	@mfolders = grep { $_ ne $folder && !$_->{'nowrite'} } @folders;
	print &ui_table_row($ttext{'action_dest'},
			    &folder_select(\@mfolders, under, "mfolder1"));

	print &ui_table_row($ttext{'action_sel'}, scalar(@d));

	print &ui_table_end();
	print &ui_form_end([ [ undef, $ttext{'action_'.$in{'action'}} ] ]);

	&ui_print_footer("index.cgi?folder=$in{'folder'}&start=$in{'start'}",
			 $text{'index_return'});
	}
else {
	# Just redirect
	&redirect("delete_mail.cgi?".$in{'action'}."=1".
		  "&folder=".$in{'folder'}.
		  "&mod=".$in{'mod'}.
		  join("", map { "&d=$_" } @d));
	}

