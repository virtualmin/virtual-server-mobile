#!/usr/local/bin/perl
# Show all available options for some system

$trust_unknown_referers = 1;
require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&foreign_require("server-manager", "server-manager-lib.pl");
&ReadParse();
&load_theme_library();
%text = &load_language($current_theme);

# Get and check
$s = &server_manager::get_managed_server_by("id", $in{'id'});
$s || &error($text{'system_egone'});
&server_manager::can_action_error($s);

# Show page title. In IUI mode, there is no default <div> (since we generate
# a list below), and no system name (since it is in the menu list)
$theme_iui_no_default_div = 1;
&ui_print_header(&theme_use_iui() ? undef : server_manager::server_in($s),
		 $text{'system_title'}, "", undef, 0, 1, 1);

# Get all available actions for this server
@buts = &server_manager::get_server_actions($s);
my @cats = &unique(map { $_->{'cat'} } @buts);

if (&theme_use_iui()) {
	# Show as IUI category and link menus
	print "<ul id='system' title='$text{'system_title'}' ",
	      "selected='true'>\n";
	print "<li>",&server_manager::server_in($s),"</li>\n";

	# Menus for categories, with no-category links at top level
	foreach my $c (@cats) {
		my @incat = grep { $_->{'cat'} eq $c } @buts;
		if (!$c) {
			foreach my $b (@incat) {
				$url = &system_action_url($b, $s);
				print "<li><a href='$url' ",
				      "target=_self>$b->{'desc'}</a></li>\n";
				}
			}
		else {
			print "<li><a href='#systemcat_$c'>",
			      $server_manager::text{'cat_'.$c}."</a></li>\n";
			}
		}
	print "</ul>\n";

	# Lists for categories
	foreach my $c (@cats) {
		next if (!$c);
		my @incat = grep { $_->{'cat'} eq $c } @buts;
		print "<ul id='systemcat_$c' title='",
		      $server_manager::text{'cat_'.$c},"'>\n";
		foreach my $b (@incat) {
			$url = &system_action_url($b, $s);
			print "<li><a href='$url' ",
			      "target=_self>$b->{'desc'}</a></li>\n";
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
	foreach my $b (@incat) {
		print "<a href='$b->{'url'}'>$b->{'title'}</a><br>\n";
		}
	print "<p>\n";

	# Show other categories
	print "<dl>\n";
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
	}


# Returns a link for some VM2 action
sub system_action_url
{
local ($b, $s) = @_;
if ($b->{'link'} =~ /\//) {
	return $b->{'link'};
	}
elsif ($b->{'link'}) {
	return "/server-manager/$b->{'link'}";
	}
else {
	return "/server-manager/save_serv.cgi?id=$s->{'id'}&$b->{'id'}=1";
	}
}

