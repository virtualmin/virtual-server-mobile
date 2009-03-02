#!/usr/local/bin/perl
# Show a list of all VM2 systems, with links to manage each

$trust_unknown_referers = 1;
require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
&foreign_require("server-manager", "server-manager-lib.pl");

&ui_print_header(undef, $text{'slist_title'}, "", undef, 0, 1, 1);

@allservers = &server_manager::list_managed_servers();
@servers = &server_manager::list_managed_servers_sorted();
if (@servers) {
	# Show servers
	print "<ul>\n";
	foreach my $s (@servers) {
		print "<li><a href='index_system.cgi?id=$s->{'id'}'>",
			$s->{'host'},"</a>\n";
		}
	print "</ul>\n";
	}
elsif (@allservers) {
	# User cannot edit any!
	print $text{'slist_noedit'},"<p>\n";
	}
else {
	# None defined yet
	print $text{'slist_none'},"<p>\n";
	}

&ui_print_footer("/", $text{'index'});
