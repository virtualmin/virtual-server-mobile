#!/usr/local/bin/perl
# Display address users or groups

require './mailbox-lib.pl';
&ReadParse();
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
# XXX

print &ui_tabs_end_tab();
print &ui_tabs_start_tab("mode", "groups");

# Show list of groups
# XXX

print &ui_tabs_end_tab();
print &ui_tabs_end(1);

&ui_print_footer("", $text{'mail_return'});

