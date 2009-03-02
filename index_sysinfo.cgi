#!/usr/local/bin/perl
# Show system or account information

$trust_unknown_referers = 1;
require 'virtual-server-mobile/virtual-server-mobile-lib.pl';
$theme_iui_fieldset_table = 1;

# Work out which modules we have
$prod = &get_product_name();
if ($prod eq 'webmin' && &foreign_available("virtual-server")) {
	$hasvirt = 1;
	&foreign_require("virtual-server", "virtual-server-lib.pl");
	$info = &virtual_server::get_collected_info();
	}
if ($prod eq 'webmin' && &foreign_available("server-manager")) {
	$hasvm2 = 1;
	&foreign_require("server-manager", "server-manager-lib.pl");
	}
if ($prod eq 'usermin' && &foreign_available("mailbox")) {
	$hasmail = 1;
	}

&ui_print_header(undef, $text{'sysinfo_title'}, "", undef, 0, 1, 1);

# Show general system info
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
if ($hasvirt) {
	print &ui_table_row($text{'sysinfo_virtualmin'},
		    $virtual_server::module_info{'version'});
	}
if ($hasvm2) {
	print &ui_table_row($text{'sysinfo_vm2'},
		    $server_manager::module_info{'version'});
	}
%current_theme_info = &get_theme_info($current_theme);
print &ui_table_row($text{'sysinfo_theme'},
	    $current_theme_info{'version'});

# Server time
$tm = localtime(time());
print &ui_table_row($text{'sysinfo_time'}, &make_date(time()));

# Virtualmin master admin info, such as system load
if ($hasvirt && &virtual_server::master_admin()) {
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
	}
print &ui_table_end();

# Show status of feature servers
if ($hasvirt && &virtual_server::master_admin()) {
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

# Domain owner information
if ($hasvirt && !&virtual_server::reseller_admin() &&
	        !&virtual_server::master_admin()) {
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
if ($hasvirt) {
	@doms = grep { &virtual_server::can_edit_domain($_) }
		     &virtual_server::list_domains();
	}
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
	foreach my $f ("doms", "dns", "web", "ssl", "mail",
		       "dbs", "users", "aliases") {
		local $cur = int($fcount{$f});
		local ($extra, $reason, $max) =
			&virtual_server::count_feature($f);
		print &ui_table_row($text{'sysinfo_f'.$f},
			$extra < 0 ? $cur : &text('sysinfo_out', $cur, $max));
		}
	print &ui_table_end();
	}

# Quota using for all or reseller-owned domains
if ($hasvirt &&
    (&virtual_server::master_admin() || &virtual_server::reseller_admin()) &&
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
			  $q->[2] ? &text('sysinfo_qused',
					  &nice_size($q->[1]+$q->[3]),
					  &nice_size($q->[2]))
				  : &nice_size($q->[1]+$q->[3]));
			}
		print &ui_table_end();
		}
	}

# Show feature-specific program info
if ($hasvirt &&
    &virtual_server::master_admin() && &virtual_server::can_view_sysinfo() &&
    $info->{'progs'}) {
	@info = @{$info->{'progs'}};
	print &ui_table_start($text{'sysinfo_sysinfoheader'}, "width=100%", 2);
	for($i=0; $i<@info; $i++) {
		print &ui_table_row($info[$i]->[0], $info[$i]->[1]);
		}
	print &ui_table_end();
	}

# Show VM2 systems
if ($hasvm2) {
	@servers = &server_manager::list_available_managed_servers();

	local %statuscount = ( );
	local %managercount = ( );
	foreach my $s (@servers) {
		$statuscount{$s->{'status'}}++;
		$managercount{$s->{'manager'}}++;
		}

	# Status grid
	my @tds = ( "width=40% align=left", "width=10% align=left",
		    "width=40% align=left", "width=10% align=left" );
	print &ui_table_start($text{'sysinfo_vm2statuses'}, "width=100%", 2);
	my @grid = ( );
	foreach $st (reverse(@server_manager::server_statuses)) {
		local $fk = { 'status' => $st->[0] };
		if ($statuscount{$st->[0]}) {
			print &ui_table_row(
				&server_manager::describe_status($fk, 1),
				int($statuscount{$st->[0]}));
			}
		}
	print &ui_table_end();

	# Types grid
	print &ui_table_start($text{'sysinfo_vm2types'},
			      "width=100%", 2);
	@grid = ( );
	foreach $mg (@server_manager::server_management_types) {
		$tfunc = "server_manager::type_".$mg."_desc";
		print &ui_table_row(&$tfunc(), int($managercount{$mg}));
		}
	print &ui_table_end();
	}

&ui_print_footer("/", $text{'index'});

