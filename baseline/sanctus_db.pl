#!/usr/bin/perl

# Global loads
use strict;
use warnings;
use warnings 'all';
use File::Basename;
use lib dirname (__FILE__);

# Sanctus modules
use LoadSetting;
use CatalogueAction;
use CatalogueKeeper;

# Load settings
LoadSetting::Load;

#CatalogueAction::Insert("Composer", \%LoadSetting::Settings);
