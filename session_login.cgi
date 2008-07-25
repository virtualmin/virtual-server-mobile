#!/usr/local/bin/perl
# Show a simple login form for mobile browsers

$pragma_no_cache = 1;
#$ENV{'MINISERV_INTERNAL'} || die "Can only be called by miniserv.pl";
require './web-lib.pl';
require './ui-lib.pl';
&init_config();
&load_theme_library();

# Set testing cookie
&ReadParse();
$sec = uc($ENV{'HTTPS'}) eq 'ON' ? "; secure" : "";
&get_miniserv_config(\%miniserv);
$sidname = $miniserv{'sidname'} || "sid";
print "Set-Cookie: banner=0; path=/$sec\r\n" if ($gconfig{'loginbanner'});
print "Set-Cookie: $sidname=x; path=/$sec\r\n" if ($in{'logout'});
print "Set-Cookie: testing=1; path=/$sec\r\n";

# Page title
$title = &theme_use_iui() ? $text{'session_header'} : undef;
&ui_print_unbuffered_header(undef, $title, undef, undef, undef, 1, 1, undef,
	undef, "onLoad='document.forms[0].pass.value = \"\"; ".
	       "document.forms[0].user.focus()'");

# Show any error message
if (defined($in{'failed'})) {
	print &ui_subheading($text{'session_failed'});
	}
elsif ($in{'logout'}) {
	print &ui_subheading($text{'session_logout'});
	}
elsif ($in{'timed_out'}) {
	print &ui_subheading(&text('session_timed_out',
				   int($in{'timed_out'}/60)));
	}

print "$text{'session_prefix'}\n";
print &ui_form_start("$gconfig{'webprefix'}/session_login.cgi", "post");
print &ui_hidden("page", $in{'page'});

# Start of table for form
print &ui_table_start(&theme_use_iui() ? undef : $text{'session_header'},
	undef, 2);

if ($gconfig{'realname'}) {
	$host = &get_display_hostname();
	}
else {
	$host = $ENV{'HTTP_HOST'};
	$host =~ s/:\d+//g;
	$host = &html_escape($host);
	}
print &ui_table_row(undef, 
      &text($gconfig{'nohostname'} ? 'session_mesg2' : 'session_mesg',
	    "<tt>$host</tt>"), 2);

print &ui_table_row($text{'session_user'},
	&ui_textbox("user", $in{'failed'}, 20));

print &ui_table_row($text{'session_pass'},
	&ui_password("pass", undef, 20));

print &ui_table_row(" ",
	&ui_checkbox("save", 1, $text{'session_save'}, 1));

print &ui_table_end();
print &ui_form_end([ [ undef, $text{'session_login'} ] ]);

print "$text{'session_postfix'}\n";

&ui_print_footer();

