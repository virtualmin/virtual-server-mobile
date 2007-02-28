#!/usr/local/bin/perl
# Show a list of all virtual servers, with links to manage each

require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");
%text = &load_language($current_theme);

&ui_print_header(undef, $text{'list_title'}, "", undef, 0, 1, 1);

@alldoms = &virtual_server::list_domains();
@doms = grep { &virtual_server::can_edit_domain($_) } @alldoms;
if (@doms) {
	# Show domains
	print "<ul>\n";
	foreach my $d (sort { lc($a->{'dom'}) cmp lc($b->{'dom'}) } @doms) {
		#$prog = &virtual_server::can_config_domain($d) ?
		#		"edit_domain.cgi" : "view_domain.cgi";
		print "<li><a href='index_edit.cgi?dom=$d->{'id'}'>$d->{'dom'}</a>\n";
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
