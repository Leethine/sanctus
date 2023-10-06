#!/usr/bin/perl

# Global loads
use strict;
use warnings;
use warnings 'all';
use File::Basename;
use lib dirname (__FILE__);

# Sanctus modules
use LoadSetting;
use CatalogueUtils;
use Catalogue;

# Load settings
LoadSetting::Load;
#print %LoadSetting::Settings;

#CatalogueAction::Insert("Composer", \%LoadSetting::Settings);
#CatalogueAction::_insertion_post_processing("/home/lizian/Music/dbtest/sanctus_db/catalogue/composer/CACHE_95.cat");

my %s = CatalogueKeeper::_read_cat_file("/home/lizian/Music/dbtest/sanctus_db/catalogue/composer/CACHE_95.cat");
for (keys %s) {
  print("$_ : $s{$_}\n");
}