package Catalogue;

use strict;
use warnings;

my $LEVEL = 1;

# arg1: insert type
# arg2: Setting hash ref
sub Insert {
  my $insert_type = lc(shift);
  my $settings = shift;
  my $dbpath = $settings->{'DBPATH'} or die "DBPATH not defined";
  
  #my $anticonflict = int(rand(100));
  my $template_file = "$dbpath/sanctus_db/catalogue/$insert_type/TEMPLATE";
  my $newfile = "$dbpath/sanctus_db/catalogue/$insert_type/CACHE.cat";
  system("cp", $template_file, $newfile);
  system("nano", $newfile);
  _insertion_post_processing($newfile);
}

# Remove comments from file
# arg1: filepath
sub _insertion_post_processing {

}

sub _generic_update {
}

sub _generic_delete {
}

1;