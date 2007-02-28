#!/usr/local/bin/perl
# Show Webmin modules in some category

require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&ReadParse();
%text = &load_language($current_theme);

@modules = &get_visible_module_infos();
%cats = &list_categories(\@modules);
&ui_print_header(undef, $text{'webmin_title'}, "", undef, 0, 1, 1);

print "<b>",&text('webmin_incat', $cats{$in{'cat'}}),"</b><br>\n";
print "<ul>\n";
foreach $m (sort { lc($a->{'desc'}) cmp lc($b->{'desc'}) } @modules) {
	if ($m->{'category'} eq $in{'cat'}) {
		print "<li><a href='$m->{'dir'}/'>$m->{'desc'}</a><br>\n";
		}
	}
print "</ul>\n";

&ui_print_footer("/", $text{'index'});

