#!/usr/local/bin/perl
# Show all available options for some domain

require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");
&ReadParse();
%text = &load_language($current_theme);

# Find the domain
if (defined($in{'search'})) {
	$d = &virtual_server::get_domain_by("dom", $in{'search'});
	if (!$d) {
		$d = &virtual_server::get_domain_by("user", $in{'search'},
						    "parent", undef);
		}
	$d || &error(&text('edit_esearch', "<tt>$in{'search'}</tt>"));
	}
else {
	$d = &virtual_server::get_domain($in{'dom'});
	}
&virtual_server::can_edit_domain($d) ||
	&error(&text('edit_ecannot', $d->{'dom'}));

&ui_print_header(&virtual_server::domain_in($d),
		 $text{'edit_title'}, "", undef, 0, 1, 1);

# Get all available actions for this domain
@buts = &virtual_server::get_all_domain_links($d);

# Show objects category at top level
my @incat = grep { $_->{'cat'} eq 'objects' } @buts;
foreach my $b (@incat) {
	print "<a href='$b->{'url'}'>$b->{'title'}</a><br>\n";
	}
print "<p>\n";

# Show other categories
print "<dl>\n";
my @cats = &unique(map { $_->{'cat'} } @buts);
foreach my $c (@cats) {
	next if ($c eq 'objects');
	my @incat = grep { $_->{'cat'} eq $c } @buts;
	print "<dt><b>$incat[0]->{'catname'}</b><br>\n";
	print "<dd>";
	foreach my $b (@incat) {
		print "<a href='$b->{'url'}'>$b->{'title'}</a><br>\n";
		}
	}
print "</dl>\n";

&ui_print_footer($in{'search'} ? ( ) : ( "index_list.cgi",
					 $text{'list_return'} ),
		 "/", $text{'index'});

