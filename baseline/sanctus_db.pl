#!/usr/bin/perl

# Global loads
use strict;
use warnings;
use File::Basename;
use lib dirname (__FILE__);

# Sanctus modules
use LoadSetting;

LoadSetting::load;

print %LoadSetting::Settings;
