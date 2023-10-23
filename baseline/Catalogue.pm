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
  $entryname =~ s/\s/\-/g;
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
      #my $opus = $catalogue{'Opus'}; #TODO

      my $keyword_str_ = $keyword_str =~ s/^\s|\s$//gr;
      $keyword_str_ =~ s/\s{2,}/ /g;
      push(@result, $filename) if ($title =~ /$keyword_str_/i);
    }
  }
  return @result;
}

# List all index by type
# arg1: type (composer/piece/arrrangement/template)
# arg2: Setting hash ref
sub List {
  my $ls_type = lc(shift);
  my $settings = shift;
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";

  CatalogueUtils::_assert_type($ls_type) or die "Assertion failed!";
  my @files = glob("$dbpath/sanctus_db/catalogue/$ls_type/*.cat");
  my @result;
  for (@files) {
    my $filename = "$_";
    push(@result, $filename);
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
  my @keywords_title = qw($keyword_str);
  my @keywords_name = qw($keyword_str);
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";

  my @arrangement_files = glob("$dbpath/sanctus_db/catalogue/arrangement/*.cat");
  my @collection_files = glob("$dbpath/sanctus_db/catalogue/collection/*.cat");
  my @piece_files = glob("$dbpath/sanctus_db/catalogue/piece/*.cat");
  my @template_files = glob("$dbpath/sanctus_db/catalogue/template/*.cat");

  my @composer_files = glob("$dbpath/sanctus_db/catalogue/composer/*.cat");
  my @work_files = push(@arrangement_files, @collection_files, @piece_files, @template_files);
  my @result;

  # Match composer first
  for (@composer_files) {
    my $filename = "$_";
    my %catalogue = CatalogueUtils::_read_cat_file($filename);
    foreach (@keywords_name) {
      my $match = TextMatching::match_composer_name($catalogue{'FirstName'}, $catalogue{'LastName'}, $_);
      # Separate the list, make two lists by composer name and work title
      shift(@keywords_title) if $match;
      shift(@keywords_name) if ! $match;
    }
  }

  #TODO continue here
}

# Run a soubroutine (find, list, ...) and get all found results
# Prompt the user with list of choices
# arg1: action
# arg2: type to find
# arg3: keyword (can be a random string if not needed)
# arg4: setting hash, passed by ref
sub ActionAndOption {
  my $action = lc(shift);
  my $find_type = lc(shift);
  my $keyword_str = lc(shift);
  my $settings = shift;
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";
  
  my @found;
  if ($action eq "find") {
    @found = &Find($find_type, $keyword_str, $settings);
  } elsif ($action eq "list") {
    @found = &List($find_type, $settings);
  } else {
    print STDERR qq/Invalild action "$action"\n/;
  }
  my %candidates;

  if (!@found) {
    print(qq/No $find_type found for keyword "$keyword_str"\n/);
    return 0;
  }

  foreach (@found) {
    my $filename = "$_";
    my %catfile = CatalogueUtils::_read_cat_file($filename);
    my $name;
    $name = $catfile{'FirstName'} . " " . $catfile{'LastName'} if $find_type eq "composer";
    $name = $catfile{'Title'} . " - " . $catfile{'Composer'} if !($find_type eq "composer");
    $candidates{$name} = $filename;
  }
  my $choice = CatalogueUtils::_prompt_for_choice(\%candidates);
  return 0 unless $choice;

  # Choose options: p(rint) del(ete) u(pdate) open
  print STDOUT "Option [p/del/u/open]: ";
  my $option = <STDIN> =~ s/\s//gr;
  if ($option eq "p") {
    my %catfile = CatalogueUtils::_read_cat_file_ignore_missing($choice) or die "Failed to read. ";
    foreach (keys %catfile) {
      print STDOUT $_, ": ", $catfile{$_}, "\n";
    }
  }
  elsif ($option eq "del") {
    system('rm', $choice) == 0 or die "Failed to delete: $choice\n";
  }
  elsif ($option eq "u") {
    system($CMD_TEXTEDITOR, $choice) == 0 or die "Failed to update: $choice\n";
  }
  elsif ($option eq "open") {
    my %catfile = CatalogueUtils::_read_cat_file($choice);
    my $hash = $catfile{'Code'};

    if ($find_type eq "composer") {
      print STDOUT "Code: ", $hash, "\n";
    }
    else {
      my $path = "$dbpath/sanctus_db/partition/$find_type";
      my @results = CatalogueUtils::_find_dir($hash, $path);
      my $location;
      if (!@results) {
        system('mkdir', '-p', "$path"."/"."$hash") == 0 or die "Failed to create directory!\n";
        $location = "$path"."/"."$hash";
      } else {
        $location = $results[0];
      }
      print STDOUT "Location: ", $location, "\n";
    }
  }
  else {
    print STDERR "Invalid option!\n";
    return 0;
  }
  return 1;
}

1;