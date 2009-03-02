#!/usr/local/bin/perl
# Show all new featurs

require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");

&ui_print_header(undef, $text{'newfeatures_title'}, "", undef, 0, 1, 1);

$newhtml = &virtual_server::get_new_features_html();
print $newhtml;

&ui_print_footer("/", $text{'index'});

