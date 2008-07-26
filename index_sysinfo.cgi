#!/usr/local/bin/perl
# Show system or account information

$trust_unknown_referers = 1;
require './web-lib.pl';
&init_config();
require './ui-lib.pl';
&foreign_require("virtual-server", "virtual-server-lib.pl");
%text = &load_language($current_theme);

&ui_print_header(undef, $text{'sysinfo_title'}, "", undef, 0, 1, 1);
$info = &virtual_server::get_collected_info();

if (!&virtual_server::reseller_admin()) {
	# Show system info
	print &ui_table_start($text{'sysinfo_systemheader'}, "width=100%", 2);

	# Hostname
	print &ui_table_row($text{'sysinfo_host'},
		    &get_system_hostname());

	# OS
	print &ui_table_row($text{'sysinfo_os'},
		    $gconfig{'os_version'} eq '*' ?
		      $gconfig{'real_os_type'} :
		      "$gconfig{'real_os_type'} $gconfig{'real_os_version'}");

	# Webmin and Virtualmin versions
	print &ui_table_row($text{'sysinfo_webmin'},
		    &get_webmin_version());
	print &ui_table_row($text{'sysinfo_virtualmin'},
		    $virtual_server::module_info{'version'});

	# Server time
	$tm = localtime(time());
	print &ui_table_row($text{'sysinfo_time'}, $tm);
	}

if (&virtual_server::master_admin()) {
	# CPU load
	if ($info->{'load'}) {
		@c = @{$info->{'load'}};
		print &ui_table_row($text{'sysinfo_cpu'},
			    &text('sysinfo_load', @c));
		}

	# Running processes
	if ($info->{'procs'}) {
		print &ui_table_row($text{'sysinfo_procs'}, $info->{'procs'});
		}

	# Real and virtual memory use
	if ($info->{'mem'}) {
		@m = @{$info->{'mem'}};
		if (@m && $m[0]) {
			print &ui_table_row($text{'sysinfo_real'},
			    &text('sysinfo_used',
				  &nice_size($m[0]*1024),
				  &nice_size(($m[0]-$m[1])*1024)));
			}
		if (@m && $m[2]) {
			print &ui_table_row($text{'sysinfo_virt'},
			    &text('sysinfo_used',
				  &nice_size($m[2]*1024),
				  &nice_size(($m[2]-$m[3])*1024)));
			}
		}

	# Disk space on local drives
	if ($info->{'disk_total'}) {
		print &ui_table_row(&text('sysinfo_disk'),
			&text('sysinfo_used', &nice_size($info->{'disk_total'}),
				    &nice_size($info->{'disk_total'} -
					       $info->{'disk_free'})));
		}
	print &ui_table_end();

	# Show status of feature servers
	if ($info->{'startstop'} && &virtual_server::can_stop_servers()) {
		print &ui_table_start($text{'sysinfo_statusheader'},
				      "width=100%", 2);
		@ss = @{$info->{'startstop'}};
		foreach $status (@ss) {
			local @msgs = ( 
			  !$status->{'status'} ?
			   "<font color=#ff0000>$text{'sysinfo_down'}</font>" :
			   "<font color=#00aa00>$text{'sysinfo_up'}</font>" );
			if ($status->{'status'}) {
				# Show stop and restart links
				push(@msgs, "<a href='virtual-server/stop_feature.cgi?feature=$status->{'feature'}'>$text{'sysinfo_stop'}</a>");
				push(@msgs, "<a href='virtual-server/restart_feature.cgi?feature=$status->{'feature'}'>$text{'sysinfo_restart'}</a>");
				}
			else {
				# Show start link
				push(@msgs, "<a href='virtual-server/start_feature.cgi?feature=$status->{'feature'}'>$text{'sysinfo_start'}</a>");
				}
			print &ui_table_row($status->{'name'},
					    &ui_links_row(\@msgs));
			}
		print &ui_table_end();
		}
	}
elsif (!&virtual_server::reseller_admin()) {
	# Show domain owner info about his server
	$d = &virtual_server::get_domain_by("user", $remote_user, "parent", "");
	print &ui_table_row($text{'sysinfo_dom'},
			    $d->{'dom'});

	# Domain's quota and limit
	if (&virtual_server::has_home_quotas()) {
		$homesize = &virtual_server::quota_bsize("home");
		$mailsize = &virtual_server::quota_bsize("mail");
		($home, $mail, $db) = &virtual_server::get_domain_quota($d, 1);
		$usage = $home*$homesize + $mail*$mailsize + $db;
		$limit = $d->{'quota'}*$homesize;
		print &ui_table_row($text{'sysinfo_quota'},
			$limit ? &text('sysinfo_of', &nice_size($usage),
						   &nice_size($limit))
			       : &nice_size($usage));
		}

	# Domain's bandwidth limit
	if ($virtual_server::config{'bw_active'} && $d->{'bw_limit'}) {
		# Bandwidth usage and limit
		print &ui_table_row($text{'sysinfo_bw'},
		   &text('sysinfo_of', &nice_size($d->{'bw_usage'}),
			&virtual_server::text(
			'edit_bwpast_'.$virtual_server::config{'bw_past'},
			&nice_size($d->{'bw_limit'}),
			$virtual_server::config{'bw_period'})));
		}

	print &ui_table_end();
	}

# Show domain and feature counts
@doms = grep { &virtual_server::can_edit_domain($_) }
	     &virtual_server::list_domains();
if (@doms) {
	print &ui_table_start($text{'sysinfo_virtheader'},
			      "width=100%", 2);
	%fcount = map { $_, 0 } @virtual_server::features;
	$fcount{'doms'} = 0;
	foreach my $d (@doms) {
		$fcount{'doms'}++;
		foreach my $f (@virtual_server::features) {
			$fcount{$f}++ if ($d->{$f});
			}
		my @dbs = &virtual_server::domain_databases($d);
		$fcount{'dbs'} += scalar(@dbs);
		my @users = &virtual_server::list_domain_users($d, 0, 1, 1, 1);
		$fcount{'users'} += scalar(@users);
		my @aliases = &virtual_server::list_domain_aliases($d, 1);
		$fcount{'aliases'} += scalar(@aliases);
		}

	# Show counts for features, including maxes
	my $i = 0;
	print "<table>\n";
	foreach my $f ("doms", "dns", "web", "ssl", "mail",
		       "dbs", "users", "aliases") {
		local $cur = int($fcount{$f});
		local ($extra, $reason, $max) =
			&virtual_server::count_feature($f);
		print "<tr> <td><b>",$text{'sysinfo_f'.$f},"</b>\n";
		print "<td>",($extra < 0 ? $cur : &text('sysinfo_out', $cur, $max)),"</td> </tr>\n";
		}
	print "</table>\n";
	print &ui_table_end();
	}

if ((&virtual_server::master_admin() || &virtual_server::reseller_admin()) &&
    &virtual_server::has_home_quotas()) {
	# Show quota usage
	$homesize = &virtual_server::quota_bsize("home");
	$mailsize = &virtual_server::quota_bsize("mail");

	# Work out quotas
	foreach my $d (@doms) {
		# If this is a parent domain, sum up quotas
		if (!$d->{'parent'} && &virtual_server::has_home_quotas()) {
			local ($home, $mail, $dbusage) =
				&virtual_server::get_domain_quota($d, 1);
			local $usage = $home*$homesize +
				       $mail*$mailsize;
			$limit = $d->{'quota'}*$homesize;
			push(@quota, [ $d, $usage, $limit, $dbusage ]);
			}
		}

	if (@quota) {
		# Show disk usage by various domains
		@quota = sort { $b->[1] <=> $a->[1] } @quota;
		if (@quota > 10) {
			@quota = @quota[0..9];
			print &ui_table_start($text{'sysinfo_quota10header'},
					      "width=100%", 2);
			}
		else {
			print &ui_table_start($text{'sysinfo_quotaheader'},
					      "width=100%", 2);
			}
		foreach my $q (@quota) {
			print &ui_table_row($q->[0]->{'dom'},
			  &text($q->[2] ? 'sysinfo_qout' : 'sysinfo_qunlimit',
				&nice_size($q->[1]), &nice_size($q->[3]),
				&nice_size($q->[2])));
			}
		print &ui_table_end();
		}
	}

if (&virtual_server::master_admin() && &virtual_server::can_view_sysinfo() &&
    $info->{'progs'}) {
	# Show feature-specific program info
	@info = @{$info->{'progs'}};
	print &ui_table_start($text{'sysinfo_sysinfoheader'}, "width=100%", 2);
	print "<table>\n";
	for($i=0; $i<@info; $i++) {
		print "<tr> <td><b>$info[$i]->[0]</b></td>\n";
		print "<td>$info[$i]->[1]</td> </tr>\n";
		}
	print "<table>\n";
	print &ui_table_end();
	}

&ui_print_footer("/", $text{'index'});

