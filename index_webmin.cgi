#!/usr/local/bin/perl
# Show Webmin modules in some category

require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
&ReadParse();

@cats = &get_visible_modules_categories();
($c) = grep { $_->{'code'} eq $in{'cat'} } @cats;
&ui_print_header(undef, $text{'webmin_title'}, "", undef, 0, 1, 1);

print "<b>",&text('webmin_incat', $c->{'desc'}),"</b><br>\n";
print "<ul>\n";
foreach $m (@{$c->{'modules'}}) {
	print "<li><a href='$m->{'dir'}/'>$m->{'desc'}</a><br>\n";
	}
print "</ul>\n";

&ui_print_footer("/", $text{'index'});

