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
@buts = &virtual_server::get_domain_actions($d);
if (&virtual_server::can_config_domain($d)) {
	print "<a href='virtual-server/edit_domain.cgi?dom=$d->{'id'}'>$text{'edit_edit'}</a><br>\n";
	}
else {
	print "<a href='virtual-server/view_domain.cgi?dom=$d->{'id'}'>$text{'edit_view'}</a><br>\n";
	}

# Show objects category at top level
my @incat = grep { $_->{'cat'} eq 'objects' } @buts;
foreach my $b (@incat) {
	$url =
	 "virtual-server/$b->{'page'}?dom=$d->{'id'}&".
	 join("&", map { $_->[0]."=".&urlize($_->[1]) }
		       @{$b->{'hidden'}});
	print "<a href='$url'>$b->{'title'}</a><br>\n";
	}
print "<p>\n";

# Show other categories
print "<dl>\n";
my @cats = &unique(map { $_->{'cat'} } @buts);
foreach my $c (@cats) {
	next if ($c eq 'objects');
	my @incat = grep { $_->{'cat'} eq $c } @buts;
	print "<dt><b>",$virtual_server::text{'cat_'.$c},"</b><br>\n";
	print "<dd>";
	foreach my $b (@incat) {
		$url =
		 "virtual-server/$b->{'page'}?dom=$d->{'id'}&".
		 join("&", map { $_->[0]."=".&urlize($_->[1]) }
			       @{$b->{'hidden'}});
		print "<a href='$url'>$b->{'title'}</a><br>\n";
		}
	}

# Feature and plugin links
@links = &virtual_server::feature_links($d);
my @cats = &unique(map { $_->{'cat'} } @links);
foreach my $c (@cats) {
	my @incat = grep { $_->{'cat'} eq $c } @links;
	print "<dt><b>",$virtual_server::text{'cat_'.$c},"</b><br>\n";
	print "<dd>";
	foreach my $l (sort { $a->{'desc'} cmp $b->{'desc'} } @incat) {
		print "<a href='$l->{'mod'}/$l->{'page'}'>",
		      "$l->{'desc'}</a><br>\n";
		}
	}

# Custom links for this domain
@cl = defined(&virtual_server::list_visible_custom_links) ?
	&virtual_server::list_visible_custom_links($d) : ( );
if (@cl) {
	@linkcats = &unique(map { $_->{'cat'} } @cl);
	foreach my $lc (@linkcats) {
		@catcl = grep { $_->{'cat'} eq $lc } @cl;
		$catdesc = $catcl[0]->{'catname'} || $text{'edit_customlinks'};
		print "<dt><b>$catdesc</b><br>\n";
		print "<dd>";
		foreach $l (@catcl) {
			print "<a href='$l->{'url'}'>$l->{'desc'}</a><br>\n";
			}
		}
	}
print "</dl>\n";

&ui_print_footer($in{'search'} ? ( ) : ( "index_list.cgi",
					 $text{'list_return'} ),
		 "/", $text{'index'});

