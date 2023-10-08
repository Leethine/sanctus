package Catalogue;

use strict;
use warnings;

use CatalogueUtils;

my $LEVEL = 1;

my $MD5_HASH_SIZE = 8;
my $TITLE_MAX_SIZE = 7;
my $CMD_TEXTEDITOR = 'nano';
my $CMD_COPY = 'cp';
my $CMD_MOVE = 'mv';

# Insert composer
# arg1: insert type
# arg2: Setting hash ref
sub Insert {
  my $insert_type = lc(shift);
  my $settings = shift;
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";
  CatalogueUtils::_assert_type($insert_type);

  my $filepath = "$dbpath/sanctus_db/catalogue/$insert_type/";
  my $template_file = $filepath . "TEMPLATE";
  my $cache_file = $filepath . "CACHE.cat";
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
  }
  else {
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

sub Display {
  my $search_type = lc(shift);
  my $settings = shift;
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";
  CatalogueUtils::_assert_type($search_type);

  my $filepath = "$dbpath/sanctus_db/catalogue/$search_type/";
}

sub Find {
}

sub Update {
}

sub Delete {
}

sub _prompt_for_choice {
}

sub _prompt_for_display {
}

1;