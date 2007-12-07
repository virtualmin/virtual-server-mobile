#!/usr/local/bin/perl
# Display address users or groups

require './mailbox-lib.pl';
&ReadParse();
%ttext = &load_language($current_theme);
&ui_print_header(undef, $text{'address_title'}, "");

# Start tabs for users and groups
$prog = "list_addresses.cgi?mode=";
print &ui_tabs_start([ [ "users", $text{'address_users'}, $prog."users" ],
                       [ "groups", $text{'address_groups'}, $prog."groups" ] ],
                     "mode", $in{'mode'} || "users", 1);

# Show list of addresses
print &ui_tabs_start_tab("mode", "users");
@addrs = &list_addresses();
print "$text{'address_desc'}<p>\n";
foreach $a (grep { defined($_->[2]) } @addrs) {
	print "<a href='edit_address.cgi?idx=$a->[2]'>",
	      &html_escape($a->[0]),"</a><br>\n";
	print "<b>$ttext{'address_name'}</b> ",&html_escape($a->[1]),"\n";
	print "<b>$ttext{'address_type'}</b> ",
	      $ttext{'address_type'.int($a->[3])},"<br>\n";
	}
print "<p>\n";

# Show link to add an address
print &ui_links_row([
	"<a href='edit_address.cgi?new=1'>$text{'address_add'}</a>" ]);

print &ui_tabs_end_tab();
print &ui_tabs_start_tab("mode", "groups");

# Show list of groups
# XXX
print "<p>\n";

print &ui_tabs_end_tab();
print &ui_tabs_end(1);

&ui_print_footer("", $text{'mail_return'});

