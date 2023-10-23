#!/usr/bin/perl

# Global loads
use strict;
use warnings;
use warnings 'all';
use File::Basename;
use lib dirname (__FILE__);

# Sanctus modules
use LoadSetting;
use Catalogue;

# Load settings
LoadSetting::Load;
my $mysettings = \%LoadSetting::Settings;

my $mode = lc(shift);
my $type = lc(shift);
my $keyword = lc(shift);

if ($mode eq "add") {
  Catalogue::Insert($type, $mysettings);
}
elsif ($mode eq "insert") {
  Catalogue::Insert($type, $mysettings);
}
elsif ($mode eq "find") {
  Catalogue::ActionAndOption("find", $type, $keyword, $mysettings);
}
elsif ($mode eq "findall") {
  Catalogue::ActionAndOption("list", $type, "list all", $mysettings);
}
else {
  print STDERR "Invalid option: $mode \n";
}