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
	      &html_escape($a->[0]),"</a>\n";
	print &compose_link($a->[0], $a->[1]),"<br>\n";
	print "<b>$ttext{'address_name'}</b> ",
	      $a->[1] =~ /\S/ ? &html_escape($a->[1])
			      : "<i>$ttext{'address_none'}</i>","\n";
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
@gaddrs = &list_address_groups();
print "$text{'address_gdesc'}<p>\n";
foreach $a (grep { defined($_->[2]) } @gaddrs) {
	print "<a href='edit_group.cgi?idx=$a->[2]'>",
	      &html_escape($a->[0]),"</a>\n";
	print &compose_link($a->[0]),"<br>\n";
	@mems = &split_addresses($a->[1]);
	@mems = map { $_->[1] ? &html_escape($_->[1]) : &html_escape($_->[0]) }
		    @mems;
	if (@mems > 3) {
		$text{'address_more'} = $ttext{'address_more'};
		@mems = ( @mems[0..2], &text('address_more', @mems-3) );
		}
	print "<b>$ttext{'address_mems'}</b> ",
	      join(", ", @mems),"<br>\n";
	}
print "<p>\n";

# Show link to add a group
print &ui_links_row([
	"<a href='edit_group.cgi?new=1'>$text{'address_gadd'}</a>" ]);

print &ui_tabs_end_tab();
print &ui_tabs_end(1);

&ui_print_footer("", $text{'mail_return'});

sub compose_link
{
local ($addr, $name) = @_;
if ($name) {
	$addr = "$name <$addr>";
	}
return "<a href='reply_mail.cgi?new=1&to=".&urlize($addr)."'>".
       "<img src=images/mail-small.gif alt='(New..)' border=0></a>";
}

