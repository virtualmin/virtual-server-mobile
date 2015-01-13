#!/usr/local/bin/perl
# Show system or account information

use strict;
use warnings;
our $trust_unknown_referers = 1;
require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
our $theme_iui_fieldset_table = 1;
our (%text);
my $bar_width = 300;

my @info = &list_combined_system_info();

&ui_print_header(undef, $text{'sysinfo_title'}, "", undef, 0, 1, 1);

# Links appear at the bottom of the page
my @links = grep { $_->{'type'} eq 'link' } @info;
@info = grep { $_->{'type'} ne 'link' } @info;

foreach my $info (@info) {
	if ($info->{'type'} eq 'warning') {
		# An alert message .. skip it, since the first page shows them
		next;
		}
	else {
		my $open = defined($info->{'open'}) ? $info->{'open'} : 1;
		print &ui_hidden_table_start($info->{'desc'}, "width=600", 2,
					     $info->{'module'}.$info->{'id'},
					     $open);
		if ($info->{'type'} eq 'table') {
			# A table of various labels and values
                        if ($info->{'header'}) {
                                print &ui_table_row(
                                        undef, $info->{'header'}, 4);
                                }
			foreach my $t (@{$info->{'table'}}) {
				my $chart = "";
				if ($t->{'chart'}) {
					$chart = &make_bar_chart(
							$t->{'chart'});
					$chart = "<br>".$chart;
					}
				print &ui_table_row($t->{'desc'},
						    $t->{'value'}.$chart);
				}
			}
		elsif ($info->{'type'} eq 'chart') {
			# A table of graphs
			my $ctable;
                        if ($info->{'header'}) {
                                $ctable .= $info->{'header'}."<br>\n";
                                }
			foreach my $t (@{$info->{'chart'}}) {
				$ctable .= $t->{'desc'}."<br>\n";
				$ctable .= &make_bar_chart($t->{'chart'})." ".
					   $t->{'value'}."<br>\n";
				}
			print &ui_table_row(undef, $ctable, 2);
			}
		elsif ($info->{'type'} eq 'html') {
			# A chunk of HTML
			print &ui_table_row(undef, $info->{'html'}, 2);
			}
		print &ui_hidden_table_end();
		print "<p>\n";
		}
	}

if (@links) {
	my @tlinks = map { $_->{'link'} } @links;
	my @ttitles = map { $_->{'desc'} } @links;
	my @ticons = map { undef } @links;
	print &icons_table(\@tlinks, \@ttitles, \@ticons);
        }

&ui_print_footer("/", $text{'index'});

# bar_chart_three(total, used1, used2, used3)
# Returns HTML for a bar chart of three values, stacked
sub bar_chart_three
{
my ($total, $used1, $used2, $used3) = @_;
my $rv;
my $w1 = int($bar_width*$used1/$total)+1;
my $w2 = int($bar_width*$used2/$total);
my $w3 = int($bar_width*$used3/$total);
$rv .= sprintf "<img src=images/red.gif width=%s height=10>", $w1;
$rv .= sprintf "<img src=images/purple.gif width=%s height=10>", $w2;
$rv .= sprintf "<img src=images/blue.gif width=%s height=10>", $w3;
$rv .= sprintf "<img src=images/grey.gif width=%s height=10>",
	$bar_width - $w1 - $w2 - $w3;
return $rv;
}

sub make_bar_chart
{
my ($c) = @_;
my @c = @$c;
if (@c == 2) {
	return &bar_chart_three(
		$c[0], $c[1], 0, $c[0]-$c[1]);
	}
else {
	return &bar_chart_three(
		$c[0], $c[1], $c[2],
		$c[0]-$c[1]-$c[2]);
	}
}

