#!/usr/local/bin/perl
# Show global server config settings

require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");
&ReadParse();
%text = &load_language($current_theme);
&virtual_server::can_edit_templates() || &error($text{'templates_ecannot'});

&ui_print_header(undef, $text{'templates_title'}, "", undef, 0, 1, 1);

($tlinks, $ttitles) = &virtual_server::get_template_pages();
print "<ul>\n";
for($i=0; $i<@$tlinks; $i++) {
	$link = $tlinks->[$i];
	$link = "virtual-server/$link" if ($link !~ /\//);
	print "<li><a href='$link'>",
	      "$ttitles->[$i]</a><br>\n";
	}
print "<li><a href='config.cgi?virtual-server'>",
      "$text{'header_config'}</a><br>\n";
print "<li><a href='virtual-server/check.cgi'>$text{'templates_check'}</a><br>\n";

&ui_print_footer("/", $text{'index'});
