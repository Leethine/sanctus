package LoadSetting;

use strict;
use warnings;

my $LEVEL = 1;

our %Settings;

sub Load {
  my $home = $ENV{'HOME'};
  my $pwd = $ENV{'PWD'};
  my $filename0 = shift;

  $filename0 = "$home/.local/etc/sanctus/settings.txt" if !defined $filename0;
  my $filename1 = "$home/.local/etc/sanctus/settings.txt";
  my $filename2 = "/etc/sanctus/settings.txt";
  my $filename3 = "$pwd/settings.txt";

  for (($filename0, $filename1, $filename2, $filename3)) {
    if (-f "$_") {
      open(FH, '<', "$_") or die "Error while opening the config file: $_";
      while(<FH>){
        my @pair = split(':', "$_");
        continue if !@pair;
        my $key = $pair[0] =~ s/\s//gr;
        my $val = $pair[1] =~ s/\s//gr;
        $val =~ s|\$PWD|$pwd|;
        $val =~ s|\$HOME|$home|;
        $Settings{$key} = $val if (defined $key and defined $val and $key ne "" and $val ne "");
      }
      close(FH);
    }
  }
}

1;