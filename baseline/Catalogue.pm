package Catalogue;

use strict;
use warnings;
use CatalogueUtils;
use TextMatching;

my $LEVEL = 1;

my $MD5_HASH_SIZE = 8;
my $TITLE_MAX_SIZE = 7;
my $CMD_TEXTEDITOR = 'nano';
my $CMD_COPY = 'cp';
my $CMD_MOVE = 'mv';

# Insert an item
# arg1: insert type
# arg2: Setting hash ref
sub Insert {
  my $insert_type = lc(shift);
  my $settings = shift;
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";
  CatalogueUtils::_assert_type($insert_type) or die "Assertion failed!";

  my $filepath = "$dbpath/sanctus_db/catalogue/$insert_type/";
  my $template_file = $filepath . "TEMPLATE";
  my $cache_file = $filepath . "CACHE." . int(rand(100)) . ".cat";
  system("cp", "-f", $template_file, $cache_file);
  system($CMD_TEXTEDITOR, $cache_file);

  while (!CatalogueUtils::_verify_catalogue_file($cache_file, $insert_type)) {
    print("Mandatory fields needs to be filled: ");
    if ($insert_type eq "composer") {
      print( q\"LastName", "FirstName"\ );
    } else {
      print( q\"Title"\ );
    }
    print("\nRe-editing...\n");
    sleep(2);
    system($CMD_TEXTEDITOR, $cache_file);
  }

  my $md5full = CatalogueUtils::_get_file_md5($cache_file);
  my $md5chopped = CatalogueUtils::_get_file_md5($cache_file, $MD5_HASH_SIZE);
  my %catalogue = CatalogueUtils::_read_cat_file_ignore_missing($cache_file);
  my $entryname;

  # Post-processing
  if ($insert_type eq "composer") {
    $entryname = $catalogue{'LastName'};
  } else {
    $entryname = $catalogue{'Title'};
    # Reduce title length to $TITLE_MAX_SIZE
    $entryname = substr($entryname, 0, $TITLE_MAX_SIZE) if length($entryname) > $TITLE_MAX_SIZE;
  }
  
  # Write to catalogue file
  $entryname =~ s/\s/"-"/g;
  my $new_file = $filepath . lc($entryname) . "_" . $md5chopped . ".cat";
  CatalogueUtils::_write_cat_file_field('Code', $md5full, $cache_file);
  system("mv", $cache_file, $new_file) == 0 or die "File conflict detected: $new_file";

  print("Catalogue created: $new_file\n");
}

# Find an entry using an exact keyword
# arg1: entry type
# arg2: keyword
# arg3: Setting hash ref
# Returns the path of the .cat file
sub Find {
  my $find_type = lc(shift);
  my $keyword_str = lc(shift);
  my $settings = shift;
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";

  CatalogueUtils::_assert_type($find_type) or die "Assertion failed!";
  die "Find(\$type, \$keywords, \%settings): keywords must not be empty." if (!$keyword_str =~ /^[A-Za-z]/);

  my @files = glob("$dbpath/sanctus_db/catalogue/$find_type/*.cat");
  my @result;
  for (@files) {
    my $filename = "$_";
    my %catalogue = CatalogueUtils::_read_cat_file($filename);
    if ($find_type eq "composer") {
      my $firstname = $catalogue{'FirstName'};
      my $lastname = $catalogue{'LastName'};
      push(@result, $filename) if (TextMatching::match_composer_name($firstname, $lastname, $keyword_str));
    }
    else {
      my $title = $catalogue{'Title'};
      my $keyword_str_ = $keyword_str =~ s/^\s|\s$//gr;
      $keyword_str_ =~ s/\s{2,}/ /g;
      push(@result, $filename) if ($keyword_str_ eq $title);
    }
  }
  return @result;
}

# Typeless search, work only
# arg1: keyword
# arg2: Setting hash ref
# Returns the path of the .cat file
sub Search {
  my $keyword_str = lc(shift);
  my $settings = shift;
  my @keywords = qw($keyword_str);
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";

  my @arrangement_files = glob("$dbpath/sanctus_db/catalogue/arrangement/*.cat");
  my @collection_files = glob("$dbpath/sanctus_db/catalogue/collection/*.cat");
  my @piece_files = glob("$dbpath/sanctus_db/catalogue/piece/*.cat");
  my @template_files = glob("$dbpath/sanctus_db/catalogue/template/*.cat");
  my @result;

  # Match pieces
  for (@piece_files) {
    my $filename = "$_";
    my %catalogue = CatalogueUtils::_read_cat_file($filename);
    # TODO continue here
  }
}

sub FindAndOption {
  my $find_type = lc(shift);
  my $keyword_str = lc(shift);
  my $settings = shift;
  
  my @found = Find($find_type, $keyword_str, $settings);
  my %candidates;
  foreach (@found) {
    my $filename = "$_";
    my %catfile = CatalogueUtils::_read_cat_file($filename);
    my $name;
    $name = $catfile{'FirstName'} . " " . $catfile{'LastName'} if $find_type eq "composer";
    $name = $catfile{'Title'} . " - " . $catfile{'Composer'} if !($find_type eq "composer");
    $candidates{$name} = $filename;
  }
  my $choice = CatalogueUtils::_prompt_for_choice(\%candidates);
  print STDOUT "Option [d/del/u/h]: ";
  my $option = <STDIN> =~ s/\s//gr;
  if ($option eq "d") {
    my %catfile = CatalogueUtils::_read_cat_file($choice);
    foreach (keys %catfile) {
      print($_, ": ", $catfile{$_}, "\n");
    }
  } elsif ($option eq "del") {
    system('rm', $choice) == 0 or die "Failed to delete: $choice\n";
  } elsif ($option eq "u") {
    system($CMD_TEXTEDITOR, $choice) == 0 or die "Failed to update: $choice\n";
  } elsif ($option eq "h") {
    my %catfile = CatalogueUtils::_read_cat_file($choice);
    #TODO path
    print("Hash: ", $catfile{'Code'}, "\n");
  } else {
    print STDERR "Invalid option!\n";
  }
}

1;