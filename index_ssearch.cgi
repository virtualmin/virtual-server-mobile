#!/usr/local/bin/perl
# Show result of search on some VM2 systems

$trust_unknown_referers = 1;
require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&foreign_require("server-manager", "server-manager-lib.pl");
%text = &load_language($current_theme);
&ReadParse();

# Find by domain name or username
$s = $in{'search'};
@allservers = &server_manager::list_available_managed_servers_sorted();
@servers = grep { $_->{'host'} eq $s } @allservers;
if (!@servers) {
	@servers = grep { $_->{'host'} =~ /\Q$s\E/i } @allservers;
	}
if (@servers == 1) {
	# Found one .. go right to it
	&redirect("index_system.cgi?id=$servers[0]->{'id'}&search=1");
	return;
	}

if (@servers) {
	$theme_iui_no_default_div = 1;
	}
&ui_print_header(undef, $text{'ssearch_title'}, "", undef, 0, 1, 1);

if (@servers) {
	# Show as list
	print "<ul title='$text{'ssearch_title'}' selected=true>\n";
	foreach my $s (@servers) {
		print "<li><a href='index_system.cgi?id=$s->{'id'}' ",
		      "target=_self>$s->{'host'}</a></li>\n";
		}
	print "</ul>\n";
	}
else {
	# No results
	print &text('ssearch_none', "<i>".&html_escape($s)."</i>"),"<p>\n";
	}

&ui_print_footer("/", $text{'index'});
