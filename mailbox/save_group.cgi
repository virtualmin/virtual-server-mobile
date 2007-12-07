#!/usr/local/bin/perl
# Update, delete or create one address group

require './mailbox-lib.pl';
&ReadParse();
%ttext = &load_language($current_theme);
if (!$in{'new'}) {
	@addrs = &list_address_groups();
	($addr) = grep { $_->[2] eq $in{'idx'} } @addrs;
	$addr || &error($ttext{'group_egone'});
	}
&error_setup($ttext{'group_err'});

if ($in{'delete'}) {
	# Just delete it
	&delete_address_group($addr->[2]);
	}
else {
	# Validate inputs
	$in{'name'} =~ /\S/ || &error($ttext{'address_ename'});
	@email = grep { /\S/ } split(/\r?\n/, $in{'email'});
	@email || &error($ttext{'address_eemail'});
	$email = join(", ", @email);

	if ($in{'new'}) {
		&create_address_group($in{'name'}, $email);
		}
	else {
		&modify_address_group($addr->[2], $in{'name'}, $email);
		}
	}
&redirect("list_addresses.cgi?mode=groups");

