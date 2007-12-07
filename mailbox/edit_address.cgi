#!/usr/local/bin/perl
# Display one address to edit or create

require './mailbox-lib.pl';
&ReadParse();
%ttext = &load_language($current_theme);
if ($in{'new'}) {
	&ui_print_header(undef, $ttext{'address_create'}, "");
	}
else {
	&ui_print_header(undef, $ttext{'address_edit'}, "");
	@addrs = &list_addresses();
	($addr) = grep { $_->[2] eq $in{'idx'} } @addrs;
	}

print &ui_form_start("save_address.cgi", "post");
print &ui_hidden("new", $in{'new'});
print &ui_hidden("idx", $in{'idx'});
print &ui_table_start($ttext{'address_header'}, undef, 2);

# Email address
print &ui_table_row($ttext{'address_email'},
		    &ui_textbox("email", $addr->[0], 40));

# Real name
print &ui_table_row($ttext{'address_real'},
		    &ui_textbox("real", $addr->[1], 40));

# From mode
print &ui_table_row($ttext{'address_from'},
		    &ui_select("from", $addr->[3],
			       [ [ 0, $text{'no'} ],
				 [ 1, $text{'yes'} ],
				 [ 2, $text{'address_yd'} ] ]));

print &ui_table_end();
if ($in{'new'}) {
	print &ui_form_end([ [ undef, $text{'create'} ] ]);
	}
else {
	print &ui_form_end([ [ undef, $text{'save'} ],
			     [ "delete", $text{'delete'} ] ]);
	}

&ui_print_footer("list_addresses.cgi", $ttext{'address_return'});

