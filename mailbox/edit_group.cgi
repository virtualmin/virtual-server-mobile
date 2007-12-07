#!/usr/local/bin/perl
# Display one group to edit or create

require './mailbox-lib.pl';
&ReadParse();
%ttext = &load_language($current_theme);
if ($in{'new'}) {
	&ui_print_header(undef, $ttext{'group_create'}, "");
	}
else {
	&ui_print_header(undef, $ttext{'group_edit'}, "");
	@addrs = &list_address_groups();
	($addr) = grep { $_->[2] eq $in{'idx'} } @addrs;
	}

print &ui_form_start("save_group.cgi", "post");
print &ui_hidden("new", $in{'new'});
print &ui_hidden("idx", $in{'idx'});
print &ui_table_start($ttext{'group_header'}, undef, 2);

# Nickname
print &ui_table_row($ttext{'group_name'},
		    &ui_textbox("name", $addr->[0], 40));

# Recipients
print &ui_table_row($ttext{'group_emails'},
    &ui_textarea("email", join("\n", map { $_->[2] }
				&split_addresses($addr->[1])), 5, 40));

print &ui_table_end();
if ($in{'new'}) {
	print &ui_form_end([ [ undef, $text{'create'} ] ]);
	}
else {
	print &ui_form_end([ [ undef, $text{'save'} ],
			     [ "delete", $text{'delete'} ] ]);
	}

&ui_print_footer("list_addresses.cgi?mode=groups", $ttext{'address_return2'});

