# Functions for mobile theme CGIs

eval "use WebminCore;";
if ($@) {
	do '../web-lib.pl';
	do '../ui-lib.pl';
	}
&init_config();
%text = &load_language($current_theme);
#&load_theme_library();

sub theme_use_iui
{
return $ENV{'HTTP_USER_AGENT'} =~ /iPhone|iPod|Android|Pre|Pixi\/|Nintendo/;
}

1;

