#!/usr/local/bin/perl
# Show a list of all virtual servers, with links to manage each

$trust_unknown_referers = 1;
require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");

&ui_print_header(undef, $text{'list_title'}, "", undef, 0, 1, 1);

@alldoms = &virtual_server::list_domains();
@doms = &virtual_server::list_visible_domains();
if (@doms) {
	# Show domains
	print "<ul>\n";
	foreach my $d (sort { lc($a->{'dom'}) cmp lc($b->{'dom'}) } @doms) {
		print "<li>",
		      ($d->{'disabled'} ? "<i>" : ""),
		      "<a href='index_edit.cgi?dom=$d->{'id'}'>",
		      &virtual_server::show_domain_name($d),"</a>",
		      ($d->{'disabled'} ? "</i>" : ""),
		      "<br>\n";
		}
	print "</ul>\n";
	}
elsif (@alldoms) {
	# User cannot edit any!
	print $text{'list_noedit'},"<p>\n";
	}
else {
	# None defined yet
	print $text{'list_none'},"<p>\n";
	}

&ui_print_footer("/", $text{'index'});
