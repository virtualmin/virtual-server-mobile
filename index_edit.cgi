#!/usr/local/bin/perl
# Show all available options for some domain

$trust_unknown_referers = 1;
require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");
&ReadParse();
&load_theme_library();
%text = &load_language($current_theme);

# Find the domain
if ($in{'dom'}) {
	$d = &virtual_server::get_domain($in{'dom'});
	}
else {
	&error($text{'edit_enone'});
	}
&virtual_server::can_edit_domain($d) ||
	&error(&text('edit_ecannot', $d->{'dom'}));

# Show page title. In IUI mode, there is no default <div> (since we generate
# a list below), and no domain name (since it is in the menu list)
$theme_iui_no_default_div = 1;
&ui_print_header(&theme_use_iui() ? undef : &virtual_server::domain_in($d),
		 $text{'edit_title'}, "", undef, 0, 1, 1);

# Get all available actions for this domain
@buts = &virtual_server::get_all_domain_links($d);
my @incat = grep { $_->{'cat'} eq 'objects' } @buts;
my @cats = &unique(map { $_->{'cat'} } @buts);

if (&theme_use_iui()) {
	# Show as IUI category and link menus
	print "<ul id='edit' title='$text{'edit_title'}' selected='true'>\n";

	print "<li>",&virtual_server::domain_in($d),"</li>\n";

	# Objects category first, at top level
	foreach my $b (@incat) {
		print "<li><a href='$b->{'url'}' target=_self>$b->{'title'}</a></li>\n";
		}

	# Menus for other categories
	foreach my $c (@cats) {
		next if ($c eq 'objects');
		my @incat = grep { $_->{'cat'} eq $c } @buts;
		print "<li><a href='#editcat_$c'>$incat[0]->{'catname'}</a></li>\n";
		}

	print "</ul>\n";

	# Lists for other categories
	foreach my $c (@cats) {
		next if ($c eq 'objects');
		my @incat = grep { $_->{'cat'} eq $c } @buts;
		print "<ul id='editcat_$c' title='$incat[0]->{'catname'}'>\n";
		foreach my $b (@incat) {
			print "<li><a href='$b->{'url'}' target=_self>$b->{'title'}</a></li>\n";
			}
		print "</ul>\n";
		}

	if ($in{'main'}) {
		# IUI will provide a nice back link
		&ui_print_footer();
		}
	else {
		# Need to create one
		&ui_print_footer("/", "Index");
		}
	}
else {
	# Show all one one page, for other mobile browsers

	# Show objects category at top level
	print "<ul>\n";
	foreach my $b (@incat) {
		print "<li><a href='$b->{'url'}'>$b->{'title'}</a><br>\n";
		}
	print "<p>\n";

	# Show other categories
	foreach my $c (@cats) {
		next if ($c eq 'objects');
		my @incat = grep { $_->{'cat'} eq $c } @buts;
		print "<li><b>$incat[0]->{'catname'}</b><br>\n";
		print "<ul>";
		foreach my $b (@incat) {
			print "<li><a href='$b->{'url'}'>$b->{'title'}</a><br>\n";
			}
		print "</ul>\n";
		}
	print "</ul>\n";

	&ui_print_footer($in{'search'} ? ( ) : ( "index_list.cgi",
						 $text{'list_return'} ),
			 "/", $text{'index'});
	}


