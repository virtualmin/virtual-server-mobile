#!/usr/local/bin/perl
# Show result of search on some servers

$trust_unknown_referers = 1;
require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");
&ReadParse();

# Find by domain name or username
$s = $in{'search'};
$s =~ s/^\s+//; $s =~ s/\s+$//;
@alldoms = &virtual_server::list_visible_domains();
@doms = grep { $_->{'dom'} eq $s ||
	       !$_->{'parent'} && $_->{'user'} eq $s } @alldoms;
if (!@doms) {
	@doms = grep { $_->{'dom'} =~ /\Q$s\E/i ||
		       !$_->{'parent'} && $_->{'user'} =~ /\Q$s\E/i } @alldoms;
	}
if (@doms == 1) {
	# Found one .. go right to it
	&redirect("index_edit.cgi?dom=$doms[0]->{'id'}&search=1");
	return;
	}

if (@doms) {
	$main::theme_iui_no_default_div = 1;
	}
&ui_print_header(undef, $text{'search_title'}, "", undef, 0, 1, 1);

if (@doms) {
	# Show as list
	print "<ul title='$text{'search_title'}' selected=true>\n";
	foreach my $d (sort { lc($a->{'dom'}) cmp lc($b->{'dom'}) }
			    @doms) {
		print "<li>",
		      "<a href='index_edit.cgi?dom=$d->{'id'}' target=_self ",
		      ($d->{'disabled'} ? "style='font-style:italic'" : ""),
		      ">",&virtual_server::show_domain_name($d),"</a>",
		      "</li>\n";
		}
	print "</ul>\n";
	}
else {
	# No results
	print &text('search_none', "<i>".&html_escape($s)."</i>"),"<p>\n";
	}

&ui_print_footer("/", $text{'index'});
