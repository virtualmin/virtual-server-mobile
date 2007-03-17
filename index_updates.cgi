#!/usr/local/bin/perl
# Show a list of packages available for update

require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");
&foreign_require("security-updates", "security-updates-lib.pl");
%text = &load_language($current_theme);

&ui_print_header(undef, $text{'updates_title'}, "", undef, 0, 1, 1);

@poss = &security_updates::list_possible_updates(2);
if (@poss) {
	print &ui_form_start("security-updates/update.cgi");
	print $text{'updates_avail'},"<p>\n";
	print "<ul>\n";
	foreach $p (@poss) {
		print "<li>$p->{'name'} $p->{'version'}<br>$p->{'desc'}<br>\n";
		print &ui_hidden("u", $p->{'name'}),"\n";
		}
	print "</ul>\n";
	print &ui_form_end([ [ undef, $text{'updates_ok'} ] ]);
	}
else {
	print "<b>$text{'updates_none'}</b><p>\n";
	}

&ui_print_footer("/", $text{'index'});
