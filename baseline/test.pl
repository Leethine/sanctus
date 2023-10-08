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
print("### Test case 1 ###\n");
LoadSetting::Load;
for (keys %LoadSetting::Settings) {
  print("$_ : $LoadSetting::Settings{$_}\n");
}

#Catalogue::Insert("Composer", \%LoadSetting::Settings);
my $cachefile = "/home/lizian/Music/dbtest/sanctus_db/catalogue/composer/CACHE_95.cat";

print("\n### Test case 2 ###\n");
my %s1 = CatalogueUtils::_read_cat_file($cachefile);
for (keys %s1) {
  print("$_ : $s1{$_}\n");
}

print("\n### Test case 3 ###\n");
my %s2 = CatalogueUtils::_read_cat_file_ignore_missing($cachefile);
for (keys %s2) {
  print("$_ : $s2{$_}\n");
}

#CatalogueUtils::_write_cat_file_field("Code", "BACH_zeuoghzeuoth", $cachefile);

print("\n### Test case 4 ###\n");
print CatalogueUtils::_get_file_md5($cachefile), "\n";
print CatalogueUtils::_get_file_md5($cachefile, 5), "\n";

Catalogue::Insert("Composer", \%LoadSetting::Settings);