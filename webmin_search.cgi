#!/usr/local/bin/perl
# Search Webmin modules and help pages and text and config.info, and output
# in IUI-friendly format

$trust_unknown_referers = 1;
use WebminCore;
&init_config();
do 'webmin-search-lib.pl';
&ReadParse();

$prod = &get_product_name();
$ucprod = ucfirst($prod);
$main::theme_iui_no_default_div = 1; 
$title = &text('wsearch_title', $ucprod);
&ui_print_header(undef, $title, "");

# Validate search text
$re = $in{'search'};
if ($re !~ /\S/) {
	&error($text{'wsearch_esearch'});
	}
$re =~ s/^\s+//;
$re =~ s/\s+$//;

# Do the search
@rv = &search_webmin($re);

# Show in table
if (@rv) {
	print "<ul id='main' title='$title' selected='true'>\n";

	foreach my $r (@rv) {
		$hi = &highlight_text($r->{'text'}, 40);

		# Work out a link for each result
		$link = $r->{'link'};
		if (@{$r->{'cgis'}}) {
			($cmod, $cpage) = split(/\//, $r->{'cgis'}->[0]);
			($cpage, $cargs) = split(/\?/, $cpage);
                        $ctitle = &cgi_page_title($cmod, $cpage) || $cpage;
			if ($r->{'mod'}->{'installed'}) {
				$cargs ||= &cgi_page_args($cmod, $cpage);
				}
			else {
				# For modules that aren't installed, linking
				# to a CGI is likely useless
				$cargs ||= "none";
				}
			if ($cargs ne "none") {
				$cargs = "?".$cargs if ($cargs ne '' &&
							$cargs !~ /^(\/|%2F)/);
				$link = "$cmod/$cpage$cargs";
				}
			}
		$link ||= $r->{'mod'}->{'dir'}.'/';
		$link =~ s/#.*$//;	# IUI doesn't like hash in links
		print "<li><a href='$link' target=_self>$hi</a></li>\n";
		}
	print "</ul>\n";
	}
else {
	print "<div id='none' class='panel' selected='true' title='$title'>\n";
	print "<b>",&text('wsearch_enone',
		"<tt>".&html_escape($re)."</tt>"),"</b><p>\n";
	print "</div>\n";
	}

&ui_print_footer("", $text{'index_return'});


