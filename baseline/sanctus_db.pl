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

if ($mode eq "insert") {
  Catalogue::Insert($type, $mysettings);
}
elsif ($mode eq "find") {
  print Catalogue::Find($type, $keyword, $mysettings);
}
elsif ($mode eq "display") {
  print Catalogue::Display($type, $keyword, $mysettings);
}
#CatalogueAction::Insert("Composer", \%LoadSetting::Settings);
