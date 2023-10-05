#!/usr/bin/perl
use strict;
use warnings;
use File::Basename;
use lib dirname (__FILE__);

use LoadSetting;

if ($#ARGV >= 1){
  print "Invalid arguments, please use --help.\n";
  exit 0;
}

my $HELPMSG = '
  Usage:
    sanctus_db_init.pl [DB_PATH]
  
  If DB_PATH is not provided, the program will load from setting.
  If the setting file does not exist neither, nothing will be done.

';

my @ComposerTemplate = qw(LastName FirstName FullName Years Style OpusSystem WikiLink ImslpLink);
my @PieceTemplate = qw(Title Subtitle Subsubtitle Dedication ComposedYear Composer Opus Editor Edition EditedYear Engraver Instrument Level);
my @CollectionTemplate = qw(Title Subtitle Subsubtitle Dedication ComposedYear Composer Opus Editor Edition EditedYear Engraver Instrument);
my @ArrangementTemplate = qw(Title Subtitle Subsubtitle Dedication ComposedYear Composer Opus Arranger ArrangedYear Editor Edition EditedYear Engraver ForInstrument OriginalInstrument);
my @TemplateTemplate = qw(Title Subtitle Subsubtitle Dedication Composer Editor Edition EditedYear Engraver Instrument);


# BEGIN PROCEDURE
my $param = shift;

if (defined $param and ($param eq '--help' or $param eq '-h')) {
  print $HELPMSG;
}
elsif (defined $param and ! -d $param) {
  print "The path you provided does not exist or is not valid: $param \n";
}
elsif (defined $param and -d $param) {
  create_db($param);
}
else {
  LoadSetting::load;
  my $dbpath = $LoadSetting::Settings{'DBPATH'} or die "Failed to load setting";
  create_db($dbpath) or die "DBPATH is invalid or occupied: $dbpath";
}

# END PROCEDURE

# Create directories and template
sub create_db {
  my $dbpath = shift;
  mkdir("$dbpath/sanctus_db");
  
  mkdir("$dbpath/sanctus_db/composer");
  make_entry_template("$dbpath/sanctus_db/composer/.template", \@ComposerTemplate);

  mkdir("$dbpath/sanctus_db/piece");
  make_entry_template("$dbpath/sanctus_db/piece/.template", \@PieceTemplate);

  mkdir("$dbpath/sanctus_db/collection");
  make_entry_template("$dbpath/sanctus_db/collection/.template", \@CollectionTemplate);

  mkdir("$dbpath/sanctus_db/arrangement");
  make_entry_template("$dbpath/sanctus_db/arrangement/.template", \@ArrangementTemplate);

  mkdir("$dbpath/sanctus_db/template");
  make_entry_template("$dbpath/sanctus_db/template/.template", \@TemplateTemplate);
}

# Write template files
# Arg1: template path
# Arg2: reference to array
sub make_entry_template {
  my $fpath = $_[0];
  my $Template = $_[1];
  open(FH, '>', $fpath) or die $!;
  for (@$Template) {
    print FH "$_: \n";
  }
  close(FH);
}