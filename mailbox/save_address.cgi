#!/usr/local/bin/perl
# Update, delete or create one address

require './mailbox-lib.pl';
&ReadParse();
%ttext = &load_language($current_theme);
if (!$in{'new'}) {
	@addrs = &list_addresses();
	($addr) = grep { $_->[2] eq $in{'idx'} } @addrs;
	$addr || &error($ttext{'address_egone'});
	}
&error_setup($ttext{'address_err'});

if ($in{'delete'}) {
	# Just delete it
	&delete_address($addr->[2]);
	}
else {
	# Validate inputs
	$in{'email'} =~ /^\S+\@\S+$/ || &error($ttext{'address_eemail'});

	if ($in{'new'}) {
		&create_address($in{'email'}, $in{'real'}, $in{'from'});
		}
	else {
		&modify_address($addr->[2],
				$in{'email'}, $in{'real'}, $in{'from'});
		}
	}
&redirect("list_addresses.cgi");

